#!/usr/bin/env python3
"""
Comprehensive Examples and Test Cases
Demonstrates the usage of all broken speech handling modules
"""

import sys
from speech_processor import SpeechProcessor, process_broken_speech
from text_repair import MultilingualTextRepairer, repair_multilingual_text
from language_detector import LanguageDetector, detect_language
from fragment_reconstructor import SpeechFragmentReconstructor, reconstruct_speech


def print_section(title):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f" {title}")
    print("="*70 + "\n")


def example_1_basic_speech_processing():
    """Example 1: Basic broken speech processing"""
    print_section("Example 1: Basic Speech Processing")

    test_cases = [
        "فقط سوال لا تبني هل هنالك مستودعات",
        "This is Englishهذا عربيand more text",
        "HelloWorld   this   is    broken...text",
    ]

    for i, text in enumerate(test_cases, 1):
        print(f"Test {i}: {text}")
        result = process_broken_speech(text)
        print(f"Reconstructed: {result['reconstructed']}")
        print(f"Is Multilingual: {result['is_multilingual']}")
        print(f"Primary Language: {result['primary_language']}")
        print(f"Language Count: {result['language_count']}")
        print()


def example_2_text_repair():
    """Example 2: Multilingual text repair"""
    print_section("Example 2: Multilingual Text Repair")

    test_cases = [
        ("Arabic spacing", "فقط سوال لا تبنيهل هنالك"),
        ("Mixed no spaces", "HelloWorldهذا عربيMoreText"),
        ("Punctuation issues", "This is broken...!!!And has   issues???"),
        ("RTL/LTR mixing", "Englishنص عربيMoreEnglish"),
        ("CamelCase", "thisIsBrokenTextThatNeedsSpaces"),
    ]

    for name, text in test_cases:
        print(f"{name}: {text}")
        result = repair_multilingual_text(text)
        print(f"Repaired: {result['repaired']}")
        print(f"Changes: {', '.join(result['changes'])}")
        print(f"Confidence: {result['confidence']:.2%}")
        print()


def example_3_language_detection():
    """Example 3: Language detection"""
    print_section("Example 3: Language Detection")

    test_cases = [
        ("Pure Arabic", "فقط سوال لا تبني هل هنالك مستودعات تعالج مشاكل"),
        ("Mixed EN/AR", "This is English وهذا نص عربي and more English"),
        ("Multiple languages", "English Русский العربية 中文 한국어"),
        ("Pure English", "This is only English text for testing"),
        ("Mixed with numbers", "Version 2.0 يدعم اللغة العربية fully"),
    ]

    for name, text in test_cases:
        print(f"{name}: {text}")
        result = detect_language(text)
        print(f"Primary: {result['primary_language']}")
        print(f"Multilingual: {result['is_multilingual']}")
        print(f"Direction: {result['text_direction']}")
        print(f"Languages detected: {len(result['languages'])}")
        for lang in result['languages']:
            print(f"  - {lang['language']}: {lang['confidence']:.1%} "
                  f"({lang['character_count']} chars)")
        print()


def example_4_fragment_reconstruction():
    """Example 4: Speech fragment reconstruction"""
    print_section("Example 4: Speech Fragment Reconstruction")

    # Test individual fragmented strings
    test_cases = [
        ("Arabic fragments", "فقط سوال ... لا تبني ... هل هنالك مستودعات"),
        ("With disfluencies", "This is um... like broken text... you know... needs fixing"),
        ("Multiple spaces", "Text with    excessive     spacing    issues"),
        ("Mixed fragments", "English text   وهذا نص عربي   more English"),
    ]

    for name, text in test_cases:
        print(f"{name}: {text}")
        result = reconstruct_speech(text)
        print(f"Reconstructed: {result['reconstructed']}")
        print(f"Confidence: {result['confidence']:.2%}")
        print(f"Strategy: {result['strategy_used']}")
        print()

    # Test with explicit fragments
    print("Explicit fragment list:")
    fragments = [
        "The beginning of a sentence...",
        "...the middle part continues...",
        "...and finally the end."
    ]
    print(f"Fragments: {fragments}")
    result = reconstruct_speech("", fragments=fragments)
    print(f"Reconstructed: {result['reconstructed']}")
    print(f"Confidence: {result['confidence']:.2%}")
    print()


def example_5_complete_pipeline():
    """Example 5: Complete processing pipeline"""
    print_section("Example 5: Complete Processing Pipeline")

    # Initialize all processors
    speech_proc = SpeechProcessor()
    text_repairer = MultilingualTextRepairer()
    lang_detector = LanguageDetector()
    reconstructor = SpeechFragmentReconstructor()

    # Complex broken multilingual text
    broken_text = "فقط سوال لا تبنيهل هنالك   مستودعات...English text  وهذا عربيmore text"

    print(f"Original broken text:\n{broken_text}\n")

    # Step 1: Detect languages
    print("Step 1: Language Detection")
    lang_result = lang_detector.analyze_multilingual_content(broken_text)
    print(f"Languages: {[l.language for l in lang_result.languages]}")
    print(f"Is multilingual: {lang_result.is_multilingual}")
    print(f"Primary: {lang_result.primary_language}\n")

    # Step 2: Repair text
    print("Step 2: Text Repair")
    repair_result = text_repairer.repair_text(broken_text)
    print(f"Repaired: {repair_result.repaired}")
    print(f"Changes: {', '.join(repair_result.changes_made)}\n")

    # Step 3: Reconstruct fragments
    print("Step 3: Fragment Reconstruction")
    recon_result = reconstructor.smart_reconstruct(repair_result.repaired)
    print(f"Reconstructed: {recon_result['reconstructed']}")
    print(f"Confidence: {recon_result['confidence']:.2%}\n")

    # Step 4: Final speech processing
    print("Step 4: Final Speech Processing")
    final_result = speech_proc.reconstruct_broken_speech(recon_result['reconstructed'])
    print(f"Final output: {final_result['reconstructed']}")
    print(f"Is multilingual: {final_result['is_multilingual']}")
    print(f"Fragment count: {len(final_result['fragments'])}")
    print()


def example_6_real_world_scenarios():
    """Example 6: Real-world use case scenarios"""
    print_section("Example 6: Real-World Scenarios")

    scenarios = [
        {
            "name": "Social Media Post",
            "text": "Excited about this! متحمس جداً #AI #الذكاء_الاصطناعي",
            "description": "Mixed language social media content"
        },
        {
            "name": "Chat Message",
            "text": "HelloWorldهذا نص مكسورMoreText...!!!",
            "description": "Corrupted chat message with encoding issues"
        },
        {
            "name": "Voice Transcript",
            "text": "um...so...the patient complained of...you know...headache and nausea",
            "description": "Speech-to-text with disfluencies"
        },
        {
            "name": "Mixed Document",
            "text": "Section 1: Introduction   القسم الأول: المقدمة   More content here",
            "description": "Bilingual document with spacing issues"
        },
        {
            "name": "Broken URL/Code",
            "text": "VisitOurWebsiteاتصل بنا atContactPage",
            "description": "Mixed language in technical content"
        }
    ]

    for scenario in scenarios:
        print(f"{scenario['name']}:")
        print(f"Description: {scenario['description']}")
        print(f"Input: {scenario['text']}")

        # Run through complete pipeline
        result = process_broken_speech(scenario['text'])
        repaired = repair_multilingual_text(result['reconstructed'])

        print(f"Output: {repaired['repaired']}")
        print(f"Languages: {result['language_count']}")
        print(f"Confidence: {repaired['confidence']:.2%}")
        print()


def run_all_examples():
    """Run all example demonstrations"""
    print_section("Broken Speech & Multilingual Handling - Examples")
    print("This script demonstrates all features of the system\n")

    examples = [
        ("Basic Speech Processing", example_1_basic_speech_processing),
        ("Text Repair", example_2_text_repair),
        ("Language Detection", example_3_language_detection),
        ("Fragment Reconstruction", example_4_fragment_reconstruction),
        ("Complete Pipeline", example_5_complete_pipeline),
        ("Real-World Scenarios", example_6_real_world_scenarios),
    ]

    for i, (name, func) in enumerate(examples, 1):
        try:
            func()
        except Exception as e:
            print(f"Error in {name}: {e}")
            import traceback
            traceback.print_exc()

    print_section("All Examples Completed")
    print("Check the output above to see how each module handles different")
    print("types of broken speech and multilingual content.\n")


if __name__ == "__main__":
    run_all_examples()
