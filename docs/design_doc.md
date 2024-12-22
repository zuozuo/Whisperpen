# WhisperPen Design Document

## Project Overview

WhisperPen is a command-line tool that leverages speech recognition and AI to convert spoken words into enhanced text. It combines OpenAI's Whisper model for accurate speech recognition with Ollama's Qwen 2.5 32B model for text enhancement.

## User Requirements

### Primary Requirements
1. Speech Recognition
   - Accept voice input from users
   - Convert speech to text accurately
   - Support Chinese language input
   - Translate to English
   - Support wake word detection
     - Wake word: "小王小王"
     - Background listening
     - Low resource usage
     - Quick response time

2. AI Enhancement
   - Use local Ollama platform
   - Utilize Qwen 2.5 32B model
   - Enhance text quality
   - Maintain professional tone

3. Output Management
   - Save to whisperpen.md
   - Auto-copy to clipboard
   - Support multiple outputs

### Enhanced Requirements
1. Improved Recognition
   - Offline processing
   - Noise reduction
   - Better accuracy
   - Fast response time

2. Performance Optimization
   - Configuration caching
   - Quick environment check
   - Efficient resource usage
   - Temporary file management

## Technical Implementation

### Component Architecture
1. Speech Handler (`speech_handler.py`)
   ```python
   class SpeechHandler:
       def __init__(self):
           # Initialize Whisper model
           # Configure audio settings
           # Setup noise reduction
   ```

2. Text Processor (`text_processor.py`)
   ```python
   class TextProcessor:
       def __init__(self):
           # Initialize Qwen model
           # Configure processing parameters
   ```

3. File Handler (`file_handler.py`)
   ```python
   class FileHandler:
       def __init__(self):
           # Setup file management
           # Configure clipboard
   ```

4. Wake Word Detector (`wake_detector.py`)
   ```python
   class WakeDetector:
       def __init__(self):
           # Initialize PocketSphinx
           # Configure wake word model
           # Setup background listening
   ```

### Processing Pipeline
1. Audio Capture
   - Sample rate: 44100Hz
   - Bit depth: 16-bit
   - Channel: Mono
   - Noise reduction: Butterworth filter
   - Preprocessing: scipy signal processing
   - Volume normalization: Required
   - Signal-to-noise ratio: Needs improvement

2. Wake Word Detection
   - Engine: PocketSphinx
   - Wake word: "小王小王"
   - Mode: Background listening
   - Resource usage: Minimal
   - Response time: < 0.5s
   - States:
     - Sleeping (waiting for wake word)
     - Waking (transitioning)
     - Active (listening for commands)
     - Processing (handling input)

3. Speech Recognition
   - Model: OpenAI Whisper base
   - Model size: Upgrade to medium/large for better accuracy
   - Language: Chinese
   - Format: WAV
   - Mode: Offline processing
   - Initial prompt: Add language context
   - Temperature: Lower for more accurate results
   - Model Loading:
     - Cache model to disk
     - Lazy loading strategy
     - Optimize memory usage
     - Support model quantization
   - Performance Optimization:
     - Model quantization (int8)
     - Batch processing
     - Smaller model for initial pass
     - Parallel processing
     - GPU acceleration if available

4. Text Enhancement
   - Model: qwen2.5:32b
   - Task: Translation + Enhancement
   - Context: Professional
   - API: Ollama local deployment

5. Output Management
   - Format: Markdown
   - Location: whisperpen.md
   - Clipboard: Automatic
   - Cache: Configuration persistence
   - Display Format:
     - Show original recognition
     - Show enhanced version
     - Use rich formatting
     - Support comparison view

## Quality Assurance

1. Performance Metrics
   - Recognition accuracy > 95%
   - Processing time < 5s
   - Memory usage < 4GB

2. Error Handling
   - Audio capture failures
   - Recognition errors
   - Model loading issues
   - File system errors

3. User Experience
   - Clear progress indicators
   - Helpful error messages
   - Intuitive interface

## Future Enhancements

1. Planned Features
   - Multiple language support
   - Custom model selection
   - Batch processing
   - Configuration UI

2. Technical Debt
   - Code optimization
   - Test coverage
   - Documentation
   - Performance monitoring

## Version Control

All changes must be documented in:
1. changelog.md - Feature and requirement changes
2. README.md - User-facing documentation
3. This design document - Technical specifications