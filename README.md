# WhisperPen

语音转文字增强工具，支持离线语音识别和 AI 文本优化。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)

## 功能特点

- 离线语音识别 (Whisper)
- AI 文本增强 (Qwen)
- 中英互译
- 降噪处理
- 智能缓存
- 剪贴板集成

## 快速开始

### 环境要求

- Python 3.8+
- FFmpeg
- Ollama

### 安装

```bash
# 安装 FFmpeg
brew install ffmpeg  # macOS
apt install ffmpeg   # Ubuntu/Debian
choco install ffmpeg # Windows

# 安装依赖
pip install -r requirements.txt

# 安装 Qwen 模型
ollama pull qwen2.5:32b
```

### 使用

```bash
# 单次识别
python -m src.main

# 后台监听模式（使用唤醒词"小王小王"）
python -m src.main -b

# 持续监听模式
python -m src.main -c
```

## 项目结构

```
WhisperPen/
├── src/          # 源代码
├── tests/        # 测试代码
├── config/       # 配置文件
├── data/         # 数据文件
└── docs/         # 文档
```

## 文档

- [设计文档](docs/design_doc.md)
- [更新日志](docs/changelog.md)
- [API文档](docs/api.md)

## 作者

- Name: Zorro
- Email: zzhatzzh@gmail.com
- Github: [@zuozuo](https://github.com/zuozuo)

## 许可证

MIT License 