# Broken Speech & Multilingual Handling System

## نظام معالجة الكلام المكسور ومتعدد اللغات

This repository provides a comprehensive solution for handling broken speech and multilingual text processing issues in language models.

## Overview | نظرة عامة

When working with speech-to-text systems or multilingual language models, several problems can occur:

- **Broken/Fragmented Speech**: Text that is split into incomplete pieces
- **Missing Spaces**: Words concatenated without proper spacing
- **Mixed Languages**: Content switching between multiple languages without clear boundaries
- **Corrupted Text**: Punctuation issues, encoding problems, or malformed input
- **RTL/LTR Mixing**: Right-to-left and left-to-right text mixed together

This system addresses all these issues with specialized modules.

## Modules | الوحدات

### 1. Speech Processor (`speech_processor.py`)

The core module for processing broken or fragmented speech input across multiple languages.

**Features:**
- Language script detection (Arabic, Latin, Cyrillic, CJK, Devanagari)
- Text segmentation by language
- Spacing normalization
- Speech reconstruction from broken input

**Usage:**

```python
from speech_processor import process_broken_speech

# Process broken speech
result = process_broken_speech("فقط سوال لا تبني هل هنالك مستودعات")

print(result['reconstructed'])  # Normalized text
print(result['is_multilingual'])  # Check if multiple languages
print(result['fragments'])  # Language-segmented fragments
```

### 2. Multilingual Text Repair (`text_repair.py`)

Advanced text repair system for handling corrupted multilingual content.

**Features:**
- Script boundary detection
- Punctuation normalization
- Word break repair
- RTL/LTR text handling
- Whitespace normalization

**Usage:**

```python
from text_repair import repair_multilingual_text

# Repair broken text
result = repair_multilingual_text("HelloWorldهذا عربيMoreText")

print(result['repaired'])  # Fixed text
print(result['changes'])  # List of repairs made
print(result['confidence'])  # Confidence score
```

### 3. Language Detection (`language_detector.py`)

Sophisticated language detection for multilingual and mixed-language content.

**Features:**
- Support for 12+ language scripts
- Multilingual content analysis
- Text direction detection (RTL/LTR)
- Segment-by-segment language identification

**Usage:**

```python
from language_detector import detect_language

# Detect languages in text
result = detect_language("This is English وهذا نص عربي and more English")

print(result['primary_language'])  # Main language
print(result['is_multilingual'])  # True/False
print(result['languages'])  # All detected languages
print(result['text_direction'])  # 'ltr', 'rtl', or 'mixed'
```

### 4. Speech Fragment Reconstructor (`fragment_reconstructor.py`)

Reconstructs coherent text from fragmented or broken speech input.

**Features:**
- Fragment classification (complete, partial, corrupted)
- Speech disfluency removal
- Intelligent fragment merging
- Multiple reconstruction strategies

**Usage:**

```python
from fragment_reconstructor import reconstruct_speech

# Reconstruct from broken text
result = reconstruct_speech("فقط سوال ... لا تبني ... هل هنالك مستودعات")

print(result['reconstructed'])  # Coherent text
print(result['confidence'])  # Reconstruction confidence

# Or from pre-split fragments
fragments = ["The beginning...", "...the middle...", "...and end."]
result = reconstruct_speech("", fragments=fragments)
```

## Complete Pipeline Example | مثال كامل

Here's how to use all modules together for comprehensive text processing:

```python
from speech_processor import SpeechProcessor
from text_repair import MultilingualTextRepairer
from language_detector import LanguageDetector
from fragment_reconstructor import SpeechFragmentReconstructor

# Initialize all processors
speech_proc = SpeechProcessor()
text_repairer = MultilingualTextRepairer()
lang_detector = LanguageDetector()
reconstructor = SpeechFragmentReconstructor()

# Input: Broken multilingual text
broken_text = "فقط سوال لا تبنيهل هنالك   مستودعات...English text  وهذا عربي"

# Step 1: Detect languages
lang_result = lang_detector.analyze_multilingual_content(broken_text)
print(f"Languages detected: {[l.language for l in lang_result.languages]}")

# Step 2: Repair text issues
repair_result = text_repairer.repair_text(broken_text)
print(f"Repaired: {repair_result.repaired}")

# Step 3: Reconstruct speech fragments
recon_result = reconstructor.smart_reconstruct(repair_result.repaired)
print(f"Reconstructed: {recon_result['reconstructed']}")

# Step 4: Process with speech processor
final_result = speech_proc.reconstruct_broken_speech(recon_result['reconstructed'])
print(f"Final output: {final_result['reconstructed']}")
print(f"Is multilingual: {final_result['is_multilingual']}")
```

## Supported Languages | اللغات المدعومة

The system supports detection and processing for:

- **Arabic** (العربية) - RTL
- **English/Latin scripts** - LTR
- **Russian/Cyrillic** (Русский) - LTR
- **Chinese** (中文) - LTR
- **Japanese** (日本語) - LTR (Hiragana, Katakana, Kanji)
- **Korean** (한국어) - LTR
- **Hebrew** (עברית) - RTL
- **Greek** (Ελληνικά) - LTR
- **Hindi/Devanagari** (हिन्दी) - LTR
- **Thai** (ไทย) - LTR
- **Bengali** (বাংলা) - LTR
- And more...

## Common Use Cases | حالات الاستخدام الشائعة

### 1. Fixing Speech-to-Text Output

```python
# STT often produces fragmented output
stt_output = "um... so... like... the answer is... you know... forty two"

from fragment_reconstructor import reconstruct_speech
result = reconstruct_speech(stt_output)
# Output: "the answer is forty two"
```

### 2. Processing Mixed-Language Social Media Content

```python
# Social media often mixes languages
tweet = "Excited about this! متحمس جداً #AI #الذكاء_الاصطناعي"

from speech_processor import process_broken_speech
result = process_broken_speech(tweet)
# Properly segments and normalizes mixed content
```

### 3. Cleaning Corrupted Chat Messages

```python
# Chat messages may have spacing/encoding issues
message = "HelloWorldهذا نص مكسورMoreText...!!!"

from text_repair import repair_multilingual_text
result = repair_multilingual_text(message)
# Output: Properly spaced and punctuated text
```

### 4. Reconstructing Incomplete Transcriptions

```python
# Audio transcription may be incomplete
fragments = [
    "The patient complained of...",
    "...headache and nausea...",
    "...for the past three days"
]

from fragment_reconstructor import reconstruct_speech
result = reconstruct_speech("", fragments=fragments)
# Output: Complete coherent sentence
```

## Technical Details | التفاصيل التقنية

### Architecture

The system is designed with modularity in mind:

```
Input Text
    ↓
Language Detection → Identify scripts and languages
    ↓
Text Repair → Fix spacing, punctuation, boundaries
    ↓
Fragment Reconstruction → Merge fragments, remove disfluencies
    ↓
Speech Processing → Final normalization and segmentation
    ↓
Clean Output
```

### Performance Considerations

- **No external dependencies**: Uses only Python standard library
- **Fast processing**: Regex-based pattern matching for speed
- **Low memory footprint**: Streaming processing where possible
- **Unicode-aware**: Proper handling of all Unicode scripts

### Confidence Scoring

Each module provides confidence scores to indicate reliability:

- **0.9-1.0**: High confidence, minimal changes needed
- **0.7-0.9**: Good confidence, standard repairs applied
- **0.5-0.7**: Moderate confidence, significant repairs made
- **<0.5**: Low confidence, review recommended

## Installation | التثبيت

No installation required! All modules use Python standard library only.

Simply copy the Python files to your project:

```bash
# Clone the repository
git clone https://github.com/devesash91-dev/ccw.git

# Run examples
cd ccw
python speech_processor.py
python text_repair.py
python language_detector.py
python fragment_reconstructor.py
```

## Requirements | المتطلبات

- Python 3.7 or higher
- No external dependencies

## API Reference | مرجع API

### SpeechProcessor

```python
class SpeechProcessor:
    def detect_language_script(text: str) -> LanguageScript
    def segment_by_language(text: str) -> List[SpeechFragment]
    def normalize_spacing(text: str) -> str
    def reconstruct_broken_speech(text: str) -> Dict
    def fix_common_corruption(text: str) -> str
```

### MultilingualTextRepairer

```python
class MultilingualTextRepairer:
    def detect_script(char: str) -> Optional[str]
    def add_script_boundaries(text: str) -> str
    def fix_rtl_ltr_mixing(text: str) -> str
    def repair_word_breaks(text: str) -> str
    def normalize_punctuation(text: str) -> str
    def repair_text(text: str, aggressive: bool) -> RepairResult
```

### LanguageDetector

```python
class LanguageDetector:
    def detect_scripts(text: str) -> Dict[str, int]
    def get_primary_script(text: str) -> Optional[str]
    def segment_by_script(text: str) -> List[Dict]
    def analyze_multilingual_content(text: str) -> MultilingualAnalysis
    def get_text_direction(text: str) -> str
```

### SpeechFragmentReconstructor

```python
class SpeechFragmentReconstructor:
    def classify_fragment(text: str) -> str
    def remove_disfluencies(text: str) -> str
    def merge_fragments(fragments: List[Fragment]) -> str
    def reconstruct_from_fragments(fragments: List[str]) -> ReconstructionResult
    def reconstruct_broken_speech(text: str) -> ReconstructionResult
    def smart_reconstruct(text: str) -> Dict
```

## Contributing | المساهمة

Contributions are welcome! Please feel free to submit a Pull Request.

## License | الترخيص

This project is open source and available under the MIT License.

## Contact | التواصل

For questions or issues, please open an issue on GitHub.

---

## Answer to Original Question | الإجابة على السؤال الأصلي

**السؤال**: "هل هنالك مستودعات تعالج مشاكل كسر الكلام و تعدد اللغات من النموذج اذا الكلام مكسور"

**الجواب**: نعم! هذا المستودع (`ccw`) يقدم حلاً شاملاً لمعالجة:

1. **الكلام المكسور**: نظام إعادة بناء النصوص المجزأة
2. **تعدد اللغات**: كشف ومعالجة أكثر من 12 لغة
3. **النصوص التالفة**: إصلاح المسافات وعلامات الترقيم
4. **النصوص المختلطة**: معالجة النصوص التي تحتوي على عدة لغات

جميع الوحدات متوفرة وجاهزة للاستخدام في هذا المستودع.

**Answer**: Yes! This repository (`ccw`) provides a comprehensive solution for handling:

1. **Broken Speech**: Fragment reconstruction system
2. **Multilingual Content**: Detection and processing of 12+ languages
3. **Corrupted Text**: Repair of spacing and punctuation issues
4. **Mixed Text**: Processing of multi-language content

All modules are available and ready to use in this repository.
