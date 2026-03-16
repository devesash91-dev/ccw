#!/usr/bin/env python3
"""
Language Detection and Analysis Module
Provides sophisticated language detection for multilingual and mixed-language content
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from collections import Counter


@dataclass
class LanguageDetection:
    """Result of language detection"""
    language: str
    script: str
    confidence: float
    character_count: int


@dataclass
class MultilingualAnalysis:
    """Analysis result for multilingual text"""
    text: str
    is_multilingual: bool
    languages: List[LanguageDetection]
    primary_language: str
    segments: List[Dict[str, any]]


class LanguageDetector:
    """
    Advanced language detection system
    Supports detection of multiple languages within the same text
    """

    def __init__(self):
        # Define Unicode ranges for different scripts/languages
        self.script_patterns = {
            'arabic': {
                'pattern': re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+'),
                'name': 'Arabic',
                'direction': 'rtl'
            },
            'latin': {
                'pattern': re.compile(r'[A-Za-zÀ-ÿ]+'),
                'name': 'Latin (English/European)',
                'direction': 'ltr'
            },
            'cyrillic': {
                'pattern': re.compile(r'[\u0400-\u04FF]+'),
                'name': 'Cyrillic (Russian/Slavic)',
                'direction': 'ltr'
            },
            'greek': {
                'pattern': re.compile(r'[\u0370-\u03FF]+'),
                'name': 'Greek',
                'direction': 'ltr'
            },
            'hebrew': {
                'pattern': re.compile(r'[\u0590-\u05FF]+'),
                'name': 'Hebrew',
                'direction': 'rtl'
            },
            'devanagari': {
                'pattern': re.compile(r'[\u0900-\u097F]+'),
                'name': 'Devanagari (Hindi/Sanskrit)',
                'direction': 'ltr'
            },
            'chinese': {
                'pattern': re.compile(r'[\u4E00-\u9FFF]+'),
                'name': 'Chinese',
                'direction': 'ltr'
            },
            'japanese_hiragana': {
                'pattern': re.compile(r'[\u3040-\u309F]+'),
                'name': 'Japanese (Hiragana)',
                'direction': 'ltr'
            },
            'japanese_katakana': {
                'pattern': re.compile(r'[\u30A0-\u30FF]+'),
                'name': 'Japanese (Katakana)',
                'direction': 'ltr'
            },
            'korean': {
                'pattern': re.compile(r'[\uAC00-\uD7AF]+'),
                'name': 'Korean (Hangul)',
                'direction': 'ltr'
            },
            'thai': {
                'pattern': re.compile(r'[\u0E00-\u0E7F]+'),
                'name': 'Thai',
                'direction': 'ltr'
            },
            'bengali': {
                'pattern': re.compile(r'[\u0980-\u09FF]+'),
                'name': 'Bengali',
                'direction': 'ltr'
            },
        }

        # Common words for enhanced detection (optional)
        self.common_words = {
            'english': {'the', 'is', 'are', 'and', 'or', 'a', 'an', 'in', 'on', 'at'},
            'arabic': {'في', 'من', 'إلى', 'على', 'هذا', 'هذه', 'التي', 'الذي'},
        }

    def detect_scripts(self, text: str) -> Dict[str, int]:
        """
        Detect all scripts present in the text and count their characters

        Args:
            text: Input text to analyze

        Returns:
            Dictionary mapping script names to character counts
        """
        script_counts = {}

        for script_id, script_info in self.script_patterns.items():
            pattern = script_info['pattern']
            matches = pattern.findall(text)

            if matches:
                total_chars = sum(len(match) for match in matches)
                if total_chars > 0:
                    script_counts[script_id] = total_chars

        return script_counts

    def get_primary_script(self, text: str) -> Optional[str]:
        """
        Determine the primary script of the text

        Args:
            text: Input text

        Returns:
            Primary script identifier or None
        """
        script_counts = self.detect_scripts(text)

        if not script_counts:
            return None

        return max(script_counts.items(), key=lambda x: x[1])[0]

    def segment_by_script(self, text: str) -> List[Dict[str, any]]:
        """
        Segment text into chunks by script type

        Args:
            text: Input text to segment

        Returns:
            List of segments with script information
        """
        segments = []
        current_segment = []
        current_script = None
        position = 0

        for char in text:
            # Skip whitespace and punctuation for script detection
            if char.isspace() or char in '.,!?;:،؛':
                current_segment.append(char)
                continue

            # Detect script of current character
            char_script = None
            for script_id, script_info in self.script_patterns.items():
                if script_info['pattern'].match(char):
                    char_script = script_id
                    break

            # If no script detected (e.g., numbers), continue with current
            if char_script is None:
                current_segment.append(char)
                continue

            # Check if we need to start a new segment
            if current_script is None:
                current_script = char_script
                current_segment.append(char)
            elif char_script == current_script:
                current_segment.append(char)
            else:
                # Save current segment and start new one
                segment_text = ''.join(current_segment).strip()
                if segment_text:
                    segments.append({
                        'text': segment_text,
                        'script': current_script,
                        'language': self.script_patterns[current_script]['name'],
                        'direction': self.script_patterns[current_script]['direction'],
                        'position': position,
                        'length': len(segment_text)
                    })
                    position += 1

                # Start new segment
                current_script = char_script
                current_segment = [char]

        # Add final segment
        if current_segment:
            segment_text = ''.join(current_segment).strip()
            if segment_text and current_script:
                segments.append({
                    'text': segment_text,
                    'script': current_script,
                    'language': self.script_patterns[current_script]['name'],
                    'direction': self.script_patterns[current_script]['direction'],
                    'position': position,
                    'length': len(segment_text)
                })

        return segments

    def analyze_multilingual_content(self, text: str) -> MultilingualAnalysis:
        """
        Perform comprehensive analysis of potentially multilingual text

        Args:
            text: Input text to analyze

        Returns:
            MultilingualAnalysis object with detailed results
        """
        if not text or not text.strip():
            return MultilingualAnalysis(
                text="",
                is_multilingual=False,
                languages=[],
                primary_language="unknown",
                segments=[]
            )

        # Detect all scripts
        script_counts = self.detect_scripts(text)

        # Create language detection results
        languages = []
        total_chars = sum(script_counts.values())

        for script_id, char_count in script_counts.items():
            confidence = char_count / total_chars if total_chars > 0 else 0
            languages.append(LanguageDetection(
                language=self.script_patterns[script_id]['name'],
                script=script_id,
                confidence=confidence,
                character_count=char_count
            ))

        # Sort by character count (descending)
        languages.sort(key=lambda x: x.character_count, reverse=True)

        # Determine if multilingual
        is_multilingual = len(languages) > 1

        # Get primary language
        primary_language = languages[0].language if languages else "unknown"

        # Segment text
        segments = self.segment_by_script(text)

        return MultilingualAnalysis(
            text=text,
            is_multilingual=is_multilingual,
            languages=languages,
            primary_language=primary_language,
            segments=segments
        )

    def get_text_direction(self, text: str) -> str:
        """
        Determine the primary text direction (LTR or RTL)

        Args:
            text: Input text

        Returns:
            'ltr', 'rtl', or 'mixed'
        """
        script_counts = self.detect_scripts(text)

        if not script_counts:
            return 'ltr'  # Default

        # Count RTL vs LTR characters
        rtl_count = 0
        ltr_count = 0

        for script_id, count in script_counts.items():
            direction = self.script_patterns[script_id]['direction']
            if direction == 'rtl':
                rtl_count += count
            else:
                ltr_count += count

        if rtl_count > ltr_count * 2:
            return 'rtl'
        elif ltr_count > rtl_count * 2:
            return 'ltr'
        else:
            return 'mixed'


def detect_language(text: str) -> Dict[str, any]:
    """
    Convenience function for language detection

    Args:
        text: Input text to analyze

    Returns:
        Dictionary with detection results
    """
    detector = LanguageDetector()
    analysis = detector.analyze_multilingual_content(text)

    return {
        "text": analysis.text,
        "is_multilingual": analysis.is_multilingual,
        "primary_language": analysis.primary_language,
        "languages": [
            {
                "language": lang.language,
                "script": lang.script,
                "confidence": round(lang.confidence, 3),
                "character_count": lang.character_count
            }
            for lang in analysis.languages
        ],
        "segments": analysis.segments,
        "text_direction": detector.get_text_direction(text)
    }


if __name__ == "__main__":
    # Example usage and testing
    print("=== Language Detection System ===\n")

    # Test case 1: Pure Arabic
    test1 = "فقط سوال لا تبني هل هنالك مستودعات تعالج مشاكل"
    print(f"Test 1 - Arabic: {test1}")
    result1 = detect_language(test1)
    print(f"Primary: {result1['primary_language']}")
    print(f"Multilingual: {result1['is_multilingual']}")
    print(f"Direction: {result1['text_direction']}\n")

    # Test case 2: Mixed English and Arabic
    test2 = "This is English text وهذا نص عربي and more English"
    print(f"Test 2 - Mixed: {test2}")
    result2 = detect_language(test2)
    print(f"Primary: {result2['primary_language']}")
    print(f"Multilingual: {result2['is_multilingual']}")
    print(f"Languages detected: {len(result2['languages'])}")
    print(f"Segments: {len(result2['segments'])}")
    for lang in result2['languages']:
        print(f"  - {lang['language']}: {lang['confidence']:.1%} ({lang['character_count']} chars)")
    print()

    # Test case 3: Multiple languages
    test3 = "English Русский العربية 中文"
    print(f"Test 3 - Multiple: {test3}")
    result3 = detect_language(test3)
    print(f"Primary: {result3['primary_language']}")
    print(f"Multilingual: {result3['is_multilingual']}")
    print(f"Languages: {', '.join([l['language'] for l in result3['languages']])}\n")
