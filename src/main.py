from rich.console import Console
from src.speech_handler import SpeechHandler
from src.text_processor import TextProcessor
from src.file_handler import FileHandler
from src.wake_detector import WakeDetector
import click
import signal
import sys

console = Console()

def handle_exit(signum, frame):
    """处理退出信号"""
    console.print("\n👋 感谢使用 WhisperPen")
    sys.exit(0)

@click.command()
@click.option('--background', '-b', is_flag=True, help='后台监听模式（使用唤醒词"小王小王"）')
@click.option('--continuous', '-c', is_flag=True, help='持续监听模式（无需唤醒词）')
def main(background: bool, continuous: bool):
    """WhisperPen - 语音转文字增强工具"""
    # 注册信号处理
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    try:
        console.print("🎤 WhisperPen 已启动")
        
        speech_handler = SpeechHandler()
        text_processor = TextProcessor()
        file_handler = FileHandler()
        wake_detector = WakeDetector()
        
        if background:
            # 后台监听模式（使用唤醒词）
            wake_detector.start()
            while True:
                try:
                    wake_detector.wait_for_wake()
                    console.print("[yellow]请说话...[/yellow]")
                    process_speech(speech_handler, text_processor, file_handler)
                    console.print("[blue]处理完成，重新进入后台监听[/blue]")
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    console.print(f"[red]系统错误: {str(e)}[/red]")
                    continue
        elif continuous:
            # 持续监听模式（无需唤醒词）
            console.print("[yellow]持续监听模式已启动，按 Ctrl+C 退出[/yellow]")
            while True:
                try:
                    process_speech(speech_handler, text_processor, file_handler)
                except KeyboardInterrupt:
                    break
                except Exception as e:
                    console.print(f"[red]系统错误: {str(e)}[/red]")
                    continue
        else:
            # 单次识别模式
            process_speech(speech_handler, text_processor, file_handler)
                
    except KeyboardInterrupt:
        console.print("\n👋 感谢使用 WhisperPen")
    except Exception as e:
        console.print(f"[red]程序错误: {str(e)}[/red]")

def process_speech(speech_handler, text_processor, file_handler):
    """处理单次语音识别"""
    # 获取语音输入
    result = speech_handler.record_and_transcribe()
    original_text = result['original']
    recognition_type = result['type']
    
    # 显示识别类型
    type_msg = "快速识别" if recognition_type == 'fast' else "精确识别"
    console.print(f"[yellow]使用{type_msg}完成[/yellow]")
    
    # AI 增强
    console.print("[yellow]正在进行 AI 增强...[/yellow]")
    enhanced_text = text_processor.enhance_text(original_text)
    
    # 保存和显示结果
    file_handler.save_and_copy(original_text, enhanced_text)

if __name__ == "__main__":
    main() 