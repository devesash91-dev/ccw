#!/usr/bin/env python3
"""
Speech Processor Module for Broken Speech Handling
Handles fragmented, corrupted, or broken speech input across multiple languages
"""

import re
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class LanguageScript(Enum):
    """Enumeration of supported language scripts"""
    LATIN = "latin"
    ARABIC = "arabic"
    CYRILLIC = "cyrillic"
    CJK = "cjk"  # Chinese, Japanese, Korean
    DEVANAGARI = "devanagari"
    UNKNOWN = "unknown"


@dataclass
class SpeechFragment:
    """Represents a fragment of speech text"""
    text: str
    language_script: LanguageScript
    confidence: float
    position: int


class SpeechProcessor:
    """
    Main class for processing broken or fragmented speech input
    Handles multilingual content and attempts to reconstruct coherent text
    """

    def __init__(self):
        self.language_patterns = {
            LanguageScript.ARABIC: re.compile(r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]+'),
            LanguageScript.LATIN: re.compile(r'[A-Za-z]+'),
            LanguageScript.CYRILLIC: re.compile(r'[\u0400-\u04FF]+'),
            LanguageScript.CJK: re.compile(r'[\u4E00-\u9FFF\u3040-\u309F\u30A0-\u30FF\uAC00-\uD7AF]+'),
            LanguageScript.DEVANAGARI: re.compile(r'[\u0900-\u097F]+'),
        }

        # Common speech corruption patterns
        self.corruption_patterns = [
            (re.compile(r'\.{2,}'), ' '),  # Multiple dots
            (re.compile(r'\s{2,}'), ' '),  # Multiple spaces
            (re.compile(r'([a-z])([A-Z])'), r'\1 \2'),  # camelCase split
            (re.compile(r'([^\s])([\u0600-\u06FF])'), r'\1 \2'),  # Latin-Arabic boundary
            (re.compile(r'([\u0600-\u06FF])([^\s\u0600-\u06FF])'), r'\1 \2'),  # Arabic-Latin boundary
        ]

    def detect_language_script(self, text: str) -> LanguageScript:
        """
        Detect the primary language script of the given text

        Args:
            text: Input text to analyze

        Returns:
            LanguageScript enum value
        """
        if not text or not text.strip():
            return LanguageScript.UNKNOWN

        # Count characters for each script
        script_counts = {}
        for script, pattern in self.language_patterns.items():
            matches = pattern.findall(text)
            if matches:
                script_counts[script] = sum(len(m) for m in matches)

        if not script_counts:
            return LanguageScript.UNKNOWN

        # Return script with highest character count
        return max(script_counts.items(), key=lambda x: x[1])[0]

    def segment_by_language(self, text: str) -> List[SpeechFragment]:
        """
        Segment mixed-language text into fragments by language script

        Args:
            text: Input text with potentially mixed languages

        Returns:
            List of SpeechFragment objects
        """
        fragments = []
        position = 0

        # Split text into tokens
        tokens = re.split(r'(\s+)', text)
        current_fragment_text = []
        current_script = None

        for token in tokens:
            if not token.strip():
                if current_fragment_text:
                    current_fragment_text.append(token)
                continue

            token_script = self.detect_language_script(token)

            if current_script is None:
                current_script = token_script
                current_fragment_text.append(token)
            elif token_script == current_script or token_script == LanguageScript.UNKNOWN:
                current_fragment_text.append(token)
            else:
                # New script detected, save current fragment
                fragment_text = ''.join(current_fragment_text).strip()
                if fragment_text:
                    fragments.append(SpeechFragment(
                        text=fragment_text,
                        language_script=current_script,
                        confidence=0.8,
                        position=position
                    ))
                    position += 1

                # Start new fragment
                current_script = token_script
                current_fragment_text = [token]

        # Add final fragment
        if current_fragment_text:
            fragment_text = ''.join(current_fragment_text).strip()
            if fragment_text:
                fragments.append(SpeechFragment(
                    text=fragment_text,
                    language_script=current_script,
                    confidence=0.8,
                    position=position
                ))

        return fragments

    def normalize_spacing(self, text: str) -> str:
        """
        Normalize spacing issues in text

        Args:
            text: Input text with potential spacing issues

        Returns:
            Normalized text
        """
        result = text
        for pattern, replacement in self.corruption_patterns:
            result = pattern.sub(replacement, result)

        return result.strip()

    def reconstruct_broken_speech(self, text: str) -> Dict[str, any]:
        """
        Main method to process and reconstruct broken speech input

        Args:
            text: Raw input text that may be broken or corrupted

        Returns:
            Dictionary containing:
                - original: Original input text
                - normalized: Normalized text with spacing fixed
                - fragments: List of language-specific fragments
                - is_multilingual: Boolean indicating if text contains multiple languages
                - reconstructed: Best attempt at reconstructed text
        """
        if not text:
            return {
                "original": "",
                "normalized": "",
                "fragments": [],
                "is_multilingual": False,
                "reconstructed": "",
                "error": "Empty input"
            }

        # Step 1: Normalize spacing and common corruption
        normalized = self.normalize_spacing(text)

        # Step 2: Segment by language
        fragments = self.segment_by_language(normalized)

        # Step 3: Check if multilingual
        unique_scripts = set(f.language_script for f in fragments if f.language_script != LanguageScript.UNKNOWN)
        is_multilingual = len(unique_scripts) > 1

        # Step 4: Reconstruct text maintaining proper spacing
        reconstructed_parts = []
        for i, fragment in enumerate(fragments):
            reconstructed_parts.append(fragment.text)

        reconstructed = ' '.join(reconstructed_parts)

        return {
            "original": text,
            "normalized": normalized,
            "fragments": [
                {
                    "text": f.text,
                    "language_script": f.language_script.value,
                    "confidence": f.confidence,
                    "position": f.position
                } for f in fragments
            ],
            "is_multilingual": is_multilingual,
            "reconstructed": reconstructed,
            "language_count": len(unique_scripts),
            "primary_language": fragments[0].language_script.value if fragments else "unknown"
        }

    def fix_common_corruption(self, text: str) -> str:
        """
        Fix common corruption patterns in speech text

        Args:
            text: Text with potential corruption

        Returns:
            Fixed text
        """
        fixed = text

        # Fix missing spaces after punctuation
        fixed = re.sub(r'([.!?])([A-Za-z\u0600-\u06FF])', r'\1 \2', fixed)

        # Fix missing spaces before punctuation in some cases
        fixed = re.sub(r'([A-Za-z\u0600-\u06FF])([.!?]{2,})', r'\1 \2', fixed)

        # Remove excessive punctuation
        fixed = re.sub(r'([.!?]){3,}', r'\1\1', fixed)

        # Fix word concatenation (basic heuristic)
        # This is a simple approach; more sophisticated methods would use dictionaries
        fixed = re.sub(r'([a-z])([A-Z])', r'\1 \2', fixed)

        return fixed.strip()


def process_broken_speech(text: str) -> Dict[str, any]:
    """
    Convenience function to process broken speech input

    Args:
        text: Input text that may be broken or fragmented

    Returns:
        Processing results dictionary
    """
    processor = SpeechProcessor()
    return processor.reconstruct_broken_speech(text)


if __name__ == "__main__":
    # Example usage and testing
    print("=== Speech Processor for Broken Speech Handling ===\n")

    # Test case 1: Arabic text with issues
    test1 = "فقط سوال لا تبني هل هنالك مستودعات"
    print(f"Test 1 (Arabic): {test1}")
    result1 = process_broken_speech(test1)
    print(f"Result: {result1['reconstructed']}")
    print(f"Language: {result1['primary_language']}\n")

    # Test case 2: Mixed language text
    test2 = "This is Englishهذا عربيand more text"
    print(f"Test 2 (Mixed): {test2}")
    result2 = process_broken_speech(test2)
    print(f"Result: {result2['reconstructed']}")
    print(f"Is multilingual: {result2['is_multilingual']}")
    print(f"Fragments: {len(result2['fragments'])}\n")

    # Test case 3: Text with spacing issues
    test3 = "HelloWorld   this   is    broken...text"
    print(f"Test 3 (Spacing issues): {test3}")
    result3 = process_broken_speech(test3)
    print(f"Result: {result3['reconstructed']}\n")
