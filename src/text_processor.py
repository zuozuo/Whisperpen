from rich.console import Console
import ollama
import time

console = Console()

class TextProcessor:
    def __init__(self):
        self.model = "qwen2.5:32b"
        self._ensure_model_available()
        
    def _ensure_model_available(self):
        """确保模型已经下载"""
        try:
            # 检查模型是否存在
            ollama.list()
        except Exception as e:
            console.print("[yellow]正在下载 Qwen 模型，这可能需要一些时间...[/yellow]")
            try:
                ollama.pull(self.model)
            except Exception as e:
                console.print(f"[red]模型下载失败: {str(e)}[/red]")
                raise
    
    def enhance_text(self, text: str) -> str:
        """使用 Ollama 增强文本"""
        try:
            # 去除重复的文本
            text = self._remove_duplicates(text)
            
            prompt = f"""
将以下中文文本翻译成英文，要求：
1. 使用简单直白的表达
2. 保持原意
3. 去除不必要的修饰
4. 只返回翻译结果，不要解释

原文：{text}
"""
            
            console.print("[yellow]正在调用 Ollama 进行文本增强...[/yellow]")
            
            # 重试机制
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = ollama.chat(
                        model=self.model,
                        messages=[{
                            'role': 'user',
                            'content': prompt
                        }],
                        stream=False,
                        options={
                            'num_predict': 100,
                            'top_k': 50,
                            'top_p': 0.95,
                            'repeat_penalty': 1.1,
                        }
                    )
                    
                    enhanced_text = response['message']['content'].strip()
                    
                    # 如果返回内容包含解释性文字，尝试提取实际翻译部分
                    if 'Translation:' in enhanced_text:
                        enhanced_text = enhanced_text.split('Translation:')[1].strip()
                    
                    if not enhanced_text:
                        raise Exception("AI 增强返回空结果")
                        
                    return enhanced_text
                    
                except Exception as e:
                    if attempt < max_retries - 1:
                        console.print(f"[yellow]AI 增强失败，正在重试 ({attempt + 1}/{max_retries})...[/yellow]")
                        time.sleep(1)
                    else:
                        raise
            
        except Exception as e:
            console.print(f"[red]AI 增强失败: {str(e)}[/red]")
            # 如果增强失败，返回原文
            return text
    
    def _remove_duplicates(self, text: str) -> str:
        """去除文本中的重复部分"""
        # 分词并去除重复
        words = text.split()
        unique_words = []
        for word in words:
            if not unique_words or word != unique_words[-1]:
                unique_words.append(word)
        return ''.join(unique_words)