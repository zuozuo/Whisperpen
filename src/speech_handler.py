import speech_recognition as sr
from rich.console import Console
import numpy as np
from scipy.signal import butter, lfilter
import json
import os
from pathlib import Path
import time
import whisper
import tempfile
import soundfile as sf
import warnings
import torch
import hashlib
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

console = Console()

class SpeechHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # 基础配置
        self.recognizer.pause_threshold = 1.0
        self.recognizer.phrase_threshold = 0.3
        self.recognizer.non_speaking_duration = 0.5
        
        # 设置动态能量阈值
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.dynamic_energy_adjustment_damping = 0.15
        self.recognizer.dynamic_energy_ratio = 1.5
        self.recognizer.energy_threshold = 3000
        
        # 检查 ffmpeg
        self._check_ffmpeg()
        
        # 模型缓存路径
        self.cache_dir = Path.home() / '.whisperpen' / 'model_cache'
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # 延迟加载模型
        self.whisper_model = None
        
        # 读取缓存的噪音配置
        self.config_file = Path.home() / '.whisperpen_config.json'
        self.load_cached_config()
        
        # 初始化两个模型用于快速/精确识别
        self.whisper_model_fast = None  # tiny model for quick recognition
        self.whisper_model_accurate = None  # medium model for accurate recognition
        
        # 设置并行处理
        self.executor = ThreadPoolExecutor(max_workers=2)
    
    def _check_ffmpeg(self):
        """检查并安装 ffmpeg"""
        try:
            import subprocess
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            console.print("[red]未检测到 ffmpeg，请安装后重试[/red]")
            console.print("[yellow]在 macOS 上可以使用以下命令安装：[/yellow]")
            console.print("[blue]brew install ffmpeg[/blue]")
            raise Exception("请先安装 ffmpeg")
    
    def load_cached_config(self):
        """加载缓存的噪音配置"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    if config.get('last_update_time', 0) > time.time() - 3600:
                        self.recognizer.energy_threshold = config.get('energy_threshold', 3000)
                        console.print("[blue]已加载缓存的噪音配置[/blue]")
                        return True
        except Exception:
            pass
        return False
    
    def save_config(self):
        """保存噪音配置"""
        try:
            config = {
                'energy_threshold': self.recognizer.energy_threshold,
                'last_update_time': time.time()
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception:
            pass
    
    def _apply_noise_reduction(self, audio_data):
        """应用降噪处理"""
        y = np.frombuffer(audio_data.frame_data, dtype=np.int16)
        
        # 1. 音量归一化
        y = y.astype(np.float32)
        y = y / np.max(np.abs(y))
        
        # 2. 带通滤波（保留人声频率范围）
        nyq = 22050 / 2
        low = 100 / nyq  # 降低低频截止，保留更多人声
        high = 8000 / nyq  # 提高高频截止，保留更多细节
        b, a = butter(6, [low, high], btype='band')  # 提高滤波器阶数
        filtered_data = lfilter(b, a, y)
        
        # 3. 重新归一化并转换回 int16
        filtered_data = filtered_data * 32767
        audio_data.frame_data = filtered_data.astype(np.int16).tobytes()
        return audio_data
    
    def quick_ambient_check(self, source):
        """快速环境检查"""
        # 读取一小段音频来预热
        source.stream.read(int(source.SAMPLE_RATE * 0.5))
    
    def _convert_audio_to_wav(self, audio_data):
        """将音频数据转换为临时WAV文件"""
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_wav:
            # 将音频数据写入WAV文件
            sf.write(
                temp_wav.name,
                np.frombuffer(audio_data.frame_data, dtype=np.int16),
                audio_data.sample_rate,
                format='WAV',
                subtype='PCM_16'
            )
            return temp_wav.name
    
    def _load_model(self, model_name="medium"):
        """优化的模型加载"""
        if model_name == "tiny" and self.whisper_model_fast:
            return self.whisper_model_fast
        if model_name == "medium" and self.whisper_model_accurate:
            return self.whisper_model_accurate
            
        cache_file = self.cache_dir / f"whisper_{model_name}_cache.pt"
        
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")
                model = whisper.load_model(
                    model_name,
                    device="cpu" if not torch.cuda.is_available() else "cuda",
                    download_root=str(self.cache_dir)
                )
                
                # 应用量化优化
                if not torch.cuda.is_available():
                    model = torch.quantization.quantize_dynamic(
                        model, {torch.nn.Linear}, dtype=torch.qint8
                    )
                
                if model_name == "tiny":
                    self.whisper_model_fast = model
                else:
                    self.whisper_model_accurate = model
                    
                return model
                
        except Exception as e:
            console.print(f"[red]模型 {model_name} 加载失败: {str(e)}[/red]")
            raise
    
    def _transcribe_with_model(self, model, audio_path, **kwargs):
        """使用指定模型进行转写"""
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", category=UserWarning)
                result = model.transcribe(
                    audio_path,
                    language='zh',
                    task='transcribe',
                    fp16=torch.cuda.is_available(),
                    no_speech_threshold=0.6,
                    logprob_threshold=-1.0,
                    compression_ratio_threshold=2.4,
                    **kwargs
                )
            return result['text'].strip()
        except Exception as e:
            console.print(f"[red]转写失败: {str(e)}[/red]")
            return None
    
    def record_and_transcribe(self) -> dict:
        """优化的录音和转写过程"""
        try:
            # 延迟加载模型
            if self.whisper_model_fast is None:
                console.print("[yellow]正在加载快速识别模型...[/yellow]")
                self._load_model("tiny")
            if self.whisper_model_accurate is None:
                console.print("[yellow]正在加载精确识别模型...[/yellow]")
                self._load_model("medium")

            with sr.Microphone(sample_rate=44100) as source:
                try:
                    # 增加环境噪音调整时间
                    console.print("[yellow]正在快速检查环境...[/yellow]")
                    self.quick_ambient_check(source)
                    console.print("[green]开始录音，请说话...[/green]")
                    
                    # 调整录音参数
                    audio = self.recognizer.listen(
                        source,
                        timeout=15,
                        phrase_time_limit=60,
                    )
                    
                    audio = self._apply_noise_reduction(audio)
                    console.print("[yellow]正在识别...[/yellow]")
                    
                    temp_wav = self._convert_audio_to_wav(audio)
                    
                    try:
                        # 并行运行快速和精确识别
                        future_fast = self.executor.submit(
                            self._transcribe_with_model,
                            self.whisper_model_fast,
                            temp_wav,
                            temperature=0.0,
                            best_of=1
                        )
                        
                        future_accurate = self.executor.submit(
                            self._transcribe_with_model,
                            self.whisper_model_accurate,
                            temp_wav,
                            temperature=0.0,
                            best_of=5,
                            beam_size=5,
                            condition_on_previous_text=True,
                            initial_prompt="这是一段中文语音。"
                        )
                        
                        # 首先检查快速识别结果
                        try:
                            text_fast = future_fast.result(timeout=3)
                            if text_fast and len(text_fast) > 10 and not any(char.isascii() for char in text_fast):
                                console.print("[green]快速识别完成[/green]")
                                return {
                                    'original': text_fast,
                                    'type': 'fast'
                                }
                        except Exception as e:
                            console.print("[yellow]快速识别失败，等待精确识别...[/yellow]")
                        
                        # 等待精确识别结果
                        try:
                            text_accurate = future_accurate.result(timeout=10)
                            if text_accurate:
                                return {
                                    'original': text_accurate,
                                    'type': 'accurate'
                                }
                        except Exception as e:
                            raise Exception(f"精确识别失败: {str(e)}")
                        
                        raise Exception("未能识别到有效内容")
                        
                    finally:
                        # 清理临时文件
                        try:
                            if os.path.exists(temp_wav):
                                os.unlink(temp_wav)
                        except Exception:
                            pass
                        
                except Exception as e:
                    raise Exception(f"录音或识别错误: {str(e)}")
                
        except Exception as e:
            raise Exception(f"系统错误: {str(e)}")