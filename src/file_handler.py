from rich.console import Console
from rich.panel import Panel
from rich.table import Table
import pyperclip
from datetime import datetime
import os
from pathlib import Path

console = Console()

class FileHandler:
    def __init__(self):
        # 使用当前目录作为基础路径
        self.base_dir = Path.cwd()
        self.file_path = self.base_dir / "whisperpen.md"
    
    def save_and_copy(self, original_text: str, enhanced_text: str):
        """保存原始文本和增强文本，并复制增强文本到剪贴板"""
        try:
            # 创建漂亮的输出
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("Original", style="cyan", width=40)
            table.add_column("Enhanced", style="green", width=40)
            table.add_row(original_text, enhanced_text)
            
            # 显示到控制台
            console.print("\n")
            console.print(Panel(table, title="Recognition Results"))
            
            # 保存到文件
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = f"""
## {timestamp}

### Original Text
{original_text}

### Enhanced Text
{enhanced_text}

---
"""
            
            # 确保文件存在
            if not self.file_path.exists():
                self.file_path.touch()
            
            # 写入文件
            with open(self.file_path, "a", encoding="utf-8") as f:
                f.write(content)
            
            # 复制到剪贴板
            try:
                pyperclip.copy(enhanced_text)
                console.print(f"[blue]已保存到 {self.file_path} 并复制到剪贴板[/blue]")
            except Exception as e:
                console.print(f"[yellow]复制到剪贴板失败，但文件已保存到 {self.file_path}[/yellow]")
                
        except Exception as e:
            raise Exception(f"保存文件失败: {str(e)}") 