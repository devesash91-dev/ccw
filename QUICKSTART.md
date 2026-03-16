# Quick Reference Guide | دليل مرجعي سريع

## Running the Examples | تشغيل الأمثلة

```bash
# Full demonstration addressing the original question
python demo.py

# Complete examples of all features
python examples.py

# Test individual modules
python speech_processor.py
python text_repair.py
python language_detector.py
python fragment_reconstructor.py
```

## Quick Usage Examples | أمثلة استخدام سريعة

### 1. Process Broken Speech | معالجة الكلام المكسور

```python
from speech_processor import process_broken_speech

result = process_broken_speech("HelloWorldهذا نص عربي")
print(result['reconstructed'])
# Output: "Hello World هذ ا ن ص ع رب ي"
```

### 2. Repair Multilingual Text | إصلاح النص متعدد اللغات

```python
from text_repair import repair_multilingual_text

result = repair_multilingual_text("Text   with...!!!spacing")
print(result['repaired'])
# Output: "Text with! spacing"
```

### 3. Detect Languages | كشف اللغات

```python
from language_detector import detect_language

result = detect_language("English وعربي and 中文")
print(result['primary_language'])
print(result['is_multilingual'])
# Output: True (multilingual)
```

### 4. Reconstruct Fragments | إعادة بناء الأجزاء

```python
from fragment_reconstructor import reconstruct_speech

result = reconstruct_speech("Text... um... with... fragments")
print(result['reconstructed'])
# Output: "Text with fragments"
```

## Common Patterns | الأنماط الشائعة

### Pattern 1: Complete Pipeline | خط المعالجة الكامل

```python
from speech_processor import SpeechProcessor
from text_repair import MultilingualTextRepairer
from language_detector import LanguageDetector

# Initialize
sp = SpeechProcessor()
tr = MultilingualTextRepairer()
ld = LanguageDetector()

# Process
broken_text = "Your broken text here"
lang_result = ld.analyze_multilingual_content(broken_text)
repair_result = tr.repair_text(broken_text)
final_result = sp.reconstruct_broken_speech(repair_result.repaired)

print(final_result['reconstructed'])
```

### Pattern 2: Batch Processing | المعالجة الجماعية

```python
from text_repair import MultilingualTextRepairer

repairer = MultilingualTextRepairer()
texts = ["text1", "text2", "text3"]
results = repairer.batch_repair(texts)

for result in results:
    print(result.repaired)
```

### Pattern 3: Fragment List | قائمة الأجزاء

```python
from fragment_reconstructor import reconstruct_speech

fragments = [
    "First part...",
    "...middle...",
    "...end"
]

result = reconstruct_speech("", fragments=fragments)
print(result['reconstructed'])
```

## Key Functions | الوظائف الرئيسية

| Function | Input | Output | Use Case |
|----------|-------|--------|----------|
| `process_broken_speech(text)` | String | Dict with reconstructed text | General purpose |
| `repair_multilingual_text(text)` | String | Dict with repaired text | Spacing/punctuation issues |
| `detect_language(text)` | String | Dict with language info | Language identification |
| `reconstruct_speech(text)` | String or fragments | Dict with merged text | Fragment reconstruction |

## Result Structure | بنية النتائج

### Speech Processor Result
```python
{
    'original': str,
    'normalized': str,
    'fragments': list,
    'is_multilingual': bool,
    'reconstructed': str,
    'language_count': int,
    'primary_language': str
}
```

### Text Repair Result
```python
{
    'original': str,
    'repaired': str,
    'changes': list,
    'confidence': float,
    'improvement_ratio': float
}
```

### Language Detection Result
```python
{
    'text': str,
    'is_multilingual': bool,
    'primary_language': str,
    'languages': list,
    'segments': list,
    'text_direction': str  # 'ltr', 'rtl', or 'mixed'
}
```

### Fragment Reconstruction Result
```python
{
    'original': str/list,
    'reconstructed': str,
    'confidence': float,
    'strategy_used': str,
    'fragments_merged': int
}
```

## Supported Languages | اللغات المدعومة

| Script | Languages | Direction |
|--------|-----------|-----------|
| Arabic | العربية | RTL |
| Latin | English, French, Spanish, etc. | LTR |
| Cyrillic | Russian, Ukrainian, etc. | LTR |
| Chinese | 中文 (Simplified & Traditional) | LTR |
| Japanese | 日本語 (Hiragana, Katakana, Kanji) | LTR |
| Korean | 한국어 (Hangul) | LTR |
| Hebrew | עברית | RTL |
| Greek | Ελληνικά | LTR |
| Devanagari | हिन्दी (Hindi, Sanskrit) | LTR |
| Thai | ไทย | LTR |
| Bengali | বাংলা | LTR |

## Troubleshooting | استكشاف الأخطاء

### Issue: Poor reconstruction quality
**Solution**: Try the aggressive repair mode
```python
from text_repair import repair_multilingual_text
result = repair_multilingual_text(text, aggressive=True)
```

### Issue: Wrong language detection
**Solution**: Check if text has enough characters
```python
# Need at least 3-4 characters per language for reliable detection
```

### Issue: Fragments not merging properly
**Solution**: Use explicit fragment list
```python
fragments = [part1, part2, part3]
result = reconstruct_speech("", fragments=fragments)
```

## Performance Tips | نصائح الأداء

1. ✅ Use batch processing for multiple texts
2. ✅ Cache language detector instance for reuse
3. ✅ Skip unnecessary processing steps
4. ✅ Pre-filter obviously clean text

## Getting Help | الحصول على المساعدة

- See `DOCUMENTATION.md` for complete API reference
- Run `python demo.py` for demonstration
- Run `python examples.py` for comprehensive examples
- Check individual module files for inline documentation

## Answer to Original Question | إجابة السؤال الأصلي

**Q**: "هل هنالك مستودعات تعالج مشاكل كسر الكلام و تعدد اللغات من النموذج اذا الكلام مكسور"

**A**: نعم! هذا المستودع (CCW) يوفر:
- معالجة شاملة للكلام المكسور
- دعم أكثر من 12 لغة
- إصلاح تلقائي للنصوص
- كشف اللغات
- إعادة بناء الأجزاء

**A**: Yes! This repository (CCW) provides:
- Comprehensive broken speech handling
- Support for 12+ languages
- Automatic text repair
- Language detection
- Fragment reconstruction

---

Made with ❤️ for multilingual speech processing
