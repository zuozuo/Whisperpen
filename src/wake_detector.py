import speech_recognition as sr
from rich.console import Console
import time
import threading
from queue import Queue

console = Console()

class WakeDetector:
    def __init__(self):
        """初始化唤醒检测器"""
        self.is_running = False
        self.is_listening = False
        self.wake_queue = Queue()
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # 配置识别器
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.energy_threshold = 4000
            
        # 唤醒词配置
        self.wake_phrase = "小王小王"
        
    def start(self):
        """启动后台监听"""
        self.is_running = True
        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone,
            self._audio_callback,
            phrase_time_limit=3
        )
        console.print(f"[blue]进入后台监听模式，说'{self.wake_phrase}'来唤醒我[/blue]")
        
    def stop(self):
        """停止监听"""
        if self.is_running:
            self.is_running = False
            if self.stop_listening:
                self.stop_listening(wait_for_stop=False)
            
    def _audio_callback(self, recognizer, audio):
        """音频回调处理"""
        if not self.is_running:
            return
            
        try:
            # 使用本地 Whisper 模型进行识别
            text = recognizer.recognize_whisper(
                audio,
                model="tiny",
                language="zh"
            )
            
            text = text.lower().strip()
            if self.wake_phrase in text:
                console.print("[green]已唤醒！[/green]")
                self.wake_queue.put(True)
                time.sleep(0.5)  # 防止重复触发
                
        except sr.UnknownValueError:
            pass  # 忽略无法识别的音频
        except Exception as e:
            if self.is_running:
                console.print(f"[red]监听错误: {str(e)}[/red]")
                
    def wait_for_wake(self):
        """等待唤醒"""
        return self.wake_queue.get()