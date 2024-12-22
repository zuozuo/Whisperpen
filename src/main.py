from rich.console import Console
from src.speech_handler import SpeechHandler
from src.text_processor import TextProcessor
from src.file_handler import FileHandler
import click

console = Console()

@click.command()
@click.option('--continuous', '-c', is_flag=True, help='持续监听模式')
def main(continuous: bool):
    """WhisperPen - 语音转文字增强工具"""
    try:
        console.print("🎤 WhisperPen 已启动")
        
        speech_handler = SpeechHandler()
        text_processor = TextProcessor()
        file_handler = FileHandler()
        
        if continuous:
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
            process_speech(speech_handler, text_processor, file_handler)
                
    except KeyboardInterrupt:
        console.print("\n👋 感谢使用 WhisperPen")
    except Exception as e:
        console.print(f"[red]程序错误: {str(e)}[/red]")

def process_speech(speech_handler, text_processor, file_handler):
    """处理单次语���识别"""
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