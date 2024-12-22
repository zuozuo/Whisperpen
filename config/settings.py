"""WhisperPen 配置文件"""
from pathlib import Path

# 基础路径
BASE_DIR = Path(__file__).parent.parent
SRC_DIR = BASE_DIR / 'src'
DATA_DIR = BASE_DIR / 'data'
CACHE_DIR = Path.home() / '.whisperpen'

# Whisper 配置
WHISPER_CONFIG = {
    'fast_model': 'tiny',
    'accurate_model': 'medium',
    'language': 'zh',
    'sample_rate': 44100,
}

# Ollama 配置
OLLAMA_CONFIG = {
    'model': 'qwen2.5:32b',
    'options': {
        'num_predict': 100,
        'top_k': 50,
        'top_p': 0.95,
        'repeat_penalty': 1.1,
    }
}

# 音频处理配置
AUDIO_CONFIG = {
    'sample_rate': 44100,
    'bit_depth': 16,
    'channels': 1,
    'noise_reduction': {
        'low_freq': 100,
        'high_freq': 8000,
        'filter_order': 6,
    }
}

# 文件配置
FILE_CONFIG = {
    'output_file': 'whisperpen.md',
    'config_file': CACHE_DIR / 'config.json',
    'model_cache': CACHE_DIR / 'models',
} 