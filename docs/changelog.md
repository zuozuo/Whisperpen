# Changelog

All notable changes to WhisperPen will be documented in this file.

## [0.2.1] - 2024-03-19 15:10

### Technical Requirements
- FFmpeg dependency requirement identified
- PyTorch CPU optimization needed
- Warning suppression for better UX
- CUDA support consideration

### Implementation Changes
- Added FFmpeg dependency check
- Optimized PyTorch for CPU usage
- Implemented warning management
- Added CUDA device detection
- Enhanced error messaging

### Technical Improvements
- Added FFmpeg version checking
- Implemented PyTorch CPU optimization
- Added warning suppression system
- Improved error handling and user feedback

## [0.2.0] - 2024-03-19 14:35

### New Requirements
- Multiple language support requirement
  - Need for processing various input languages
  - Support for different output languages
- Output flexibility requirement
  - Support for multiple output formats
  - Configurable output locations
- Performance requirements
  - Offline processing capability
  - Enhanced noise reduction
  - Faster response times
  - Better resource utilization

### Major Changes
- Speech Recognition Engine Update
  - Replaced Google Speech Recognition with OpenAI's Whisper
  - Implemented offline processing capability
  - Added support for multiple languages
  - Improved Chinese language recognition accuracy
  - Integrated advanced noise reduction

- Performance Optimizations
  - Implemented configuration caching system
  - Developed quick environment check mechanism
  - Added efficient temporary file management
  - Optimized audio preprocessing pipeline
  - Reduced startup and processing times

### Technical Improvements
- Audio Processing
  - Added WAV file conversion for Whisper compatibility
  - Implemented scipy-based audio preprocessing
  - Integrated Butterworth filter for noise reduction
  - Optimized sample rate and bit depth handling

- System Architecture
  - Modularized code structure
  - Improved error handling system
  - Enhanced user feedback mechanisms
  - Added configuration persistence
  - Implemented resource cleanup

## [0.1.0] - 2024-03-19 11:20

### Initial Features
- Core Functionality
  - Basic speech to text conversion using Google Speech API
  - Integration with Ollama's Qwen 2.5 32B model
  - Chinese to English translation capability
  - Markdown file output support
  - Clipboard integration for easy access

- User Interface
  - Command-line interface with rich formatting
  - Progress indicators and status messages
  - Error reporting and handling

### Requirements Evolution
1. Initial Requirements Phase
   - Basic speech to text functionality
   - AI-powered text enhancement
   - Chinese to English translation
   - File saving capability
   - Clipboard integration

2. User Feedback Phase
   - Improved recognition accuracy needed
   - Offline processing capability requested
   - Faster response times required
   - Better noise handling demanded
   - Multiple language support desired

### Known Issues
- Limited language support
- Online-only speech recognition
- Basic noise handling
- Performance bottlenecks

## [0.2.2] - 2024-03-19 15:45

### Speech Recognition Improvements
- Upgraded to Whisper medium model
- Enhanced audio preprocessing
  - Improved volume normalization
  - Better frequency filtering
  - Increased filter order
- Optimized recognition parameters
  - Added beam search
  - Reduced temperature
  - Added language context
  - Improved candidate selection

### Technical Optimizations
- Improved signal-to-noise ratio
- Enhanced audio preprocessing pipeline
- Added volume normalization
- Optimized model parameters

## [0.2.3] - 2024-03-19 16:15

### Performance Improvements
- Model Loading Optimization
  - Implemented model caching
  - Added lazy loading strategy
  - Optimized memory usage
  - Improved loading progress feedback

### Technical Enhancements
- Added model cache management
- Implemented memory optimization
- Enhanced progress reporting
- Improved error handling for model loading

## [0.2.4] - 2024-03-19 16:45

### Performance Optimization
- Recognition Speed Improvements
  - Added dual-model strategy (fast/accurate)
  - Implemented parallel processing
  - Added model quantization
  - Optimized recognition parameters

### Technical Improvements
- Added int8 quantization for CPU
- Implemented parallel recognition
- Added fast recognition fallback
- Optimized model selection strategy

## [0.2.5] - 2024-03-19 17:00

### Output Improvements
- Added dual text display
  - Show original recognition text
  - Show AI enhanced version
- Enhanced output format
  - Added rich table display
  - Improved markdown formatting
  - Added timestamps to entries

### User Experience
- Added recognition type indicator
- Improved console output formatting
- Enhanced file output structure
- Better progress feedback

## [0.2.6] - 2024-03-19 17:30

### Bug Fixes
- Fixed file saving issues
  - Added proper file path handling
  - Improved error messages
  - Added file existence check
- Fixed Ollama API issues
  - Updated API call parameters
  - Switched to chat endpoint
  - Improved error handling

### Improvements
- Better file path management
- Enhanced error reporting
- Improved user feedback
- Added file location display

## [0.2.7] - 2024-03-19 18:00

### Bug Fixes
- Fixed Ollama model name
  - Updated to correct model name "qwen2.5:32b"
  - Added model availability check
  - Implemented automatic model download
- Fixed text duplication
  - Added duplicate text removal
  - Improved text processing
  - Enhanced recognition parameters

### Improvements
- Added retry mechanism for AI enhancement
- Improved error handling and recovery
- Enhanced text preprocessing
- Better user feedback for model status

## [0.2.8] - 2024-03-19 18:15

### Feature Updates
- Added operation modes
  - Single recognition mode (default)
  - Continuous listening mode (optional)
- Enhanced CLI interface
  - Added command line options
  - Improved mode selection
  - Better user guidance

### User Experience
- Clearer operation modes
- Added mode indicators
- Improved exit handling
- Enhanced command help

## [0.2.9] - 2024-03-19 18:30

### Content Improvements
- Simplified translation output
  - More concise responses
  - Removed unnecessary explanations
  - Direct translation results
  - Cleaner text format

### Prompt Optimization
- Updated prompt template
  - Added clarity requirements
  - Emphasized simplicity
  - Removed verbose instructions
  - Better result extraction

## [0.3.0] - 2024-03-19 19:00

### Bug Fixes
- Fixed module import issues
  - Added __init__.py files
  - Updated import statements
  - Fixed module paths

### Project Structure
- Improved Python package structure
  - Added proper module initialization
  - Fixed module discovery
  - Enhanced import organization

## [0.4.0] - 2024-03-19 19:30

### New Features
- Added wake word detection
  - Background listening mode
  - Wake word: "小王小王"
  - Low resource usage
  - Quick response time

### Technical Improvements
- Added PocketSphinx integration
- Implemented background processing
- Added state management
- Enhanced user feedback

## [0.4.1] - 2024-03-19 20:00

### Technical Changes
- Changed wake word detection implementation
  - Switched from PocketSphinx to SpeechRecognition
  - Using Whisper for wake word detection
  - Improved reliability and accuracy
  - Simplified installation process

### Improvements
- Better background listening
- More reliable wake word detection
- Reduced resource usage
- Easier setup process

## [0.4.2] - 2024-03-19 20:15

### User Interface
- Added multiple operation modes
  - Single recognition (default)
  - Background mode with wake word (-b)
  - Continuous mode without wake word (-c)

### Improvements
- Clearer command line options
- Better mode descriptions
- Enhanced user guidance
- Improved help messages