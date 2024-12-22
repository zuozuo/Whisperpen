# WhisperPen

WhisperPen is an advanced command-line tool that converts speech to enhanced text using AI. It combines OpenAI's Whisper model for accurate speech recognition with Ollama's Qwen 2.5 32B model for professional text enhancement and translation.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

## ✨ Features

- **Offline Speech Recognition** using OpenAI's Whisper model
- **AI-Powered Enhancement** with Qwen 2.5 32B
- **Intelligent Translation** from Chinese to English
- **Noise Reduction** with advanced audio preprocessing
- **Smart Caching** for improved performance
- **Automatic File Management** and clipboard integration

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- FFmpeg installed on your system
- Ollama with Qwen 2.5 32B model
- System requirements for PyAudio

### Installation

1. Install FFmpeg:
```bash
# On macOS
brew install ffmpeg

# On Ubuntu/Debian
sudo apt-get install ffmpeg

# On Windows
choco install ffmpeg
```

2. Clone the repository:
```bash
git clone https://github.com/zuozuo/whisperpen.git
cd whisperpen
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Ollama and the Qwen model:
```bash
ollama pull qwen2.5:32b
```

### Usage

Basic usage:
```bash
# 单次识别
python main.py

# 持续监听模式
python main.py --continuous
# 或
python main.py -c
```

With custom options:
```bash
python main.py --model "qwen2.5:32b" --output "custom_output.md"
```

## 🛠 Technical Details

- Speech recognition using Whisper base model
- CPU-optimized PyTorch configuration
- FFmpeg for audio processing
- Audio preprocessing with scipy
- Text enhancement via Ollama API
- Configuration caching for optimization
- Rich CLI interface for better UX

## 📝 Documentation

For detailed documentation, please see:
- [Design Document](design_doc.md)
- [Changelog](changelog.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 👤 Author

- Name: Zorro
- Email: zzhatzzh@gmail.com
- Github: [@zuozuo](https://github.com/zuozuo)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 