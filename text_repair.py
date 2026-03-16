#!/usr/bin/env python3
"""
Multilingual Text Repair Utilities
Provides advanced text repair and normalization for multilingual content
"""

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class RepairResult:
    """Result of text repair operation"""
    original: str
    repaired: str
    changes_made: List[str]
    confidence: float


class MultilingualTextRepairer:
    """
    Advanced text repair system for multilingual content
    Handles common issues in broken speech transcription
    """

    def __init__(self):
        # Unicode ranges for different scripts
        self.script_ranges = {
            'arabic': (0x0600, 0x06FF),
            'arabic_supplement': (0x0750, 0x077F),
            'arabic_extended_a': (0x08A0, 0x08FF),
            'arabic_presentation_a': (0xFB50, 0xFDFF),
            'arabic_presentation_b': (0xFE70, 0xFEFF),
            'latin': (0x0041, 0x007A),
            'latin_extended': (0x0100, 0x017F),
            'cyrillic': (0x0400, 0x04FF),
            'greek': (0x0370, 0x03FF),
            'hebrew': (0x0590, 0x05FF),
            'devanagari': (0x0900, 0x097F),
            'cjk': (0x4E00, 0x9FFF),
        }

        # Common repair patterns
        self.repair_patterns = self._initialize_repair_patterns()

    def _initialize_repair_patterns(self) -> List[Tuple[re.Pattern, str, str]]:
        """Initialize patterns for text repair"""
        return [
            # Pattern, Replacement, Description
            (re.compile(r'\s+'), ' ', 'Normalize whitespace'),
            (re.compile(r'\.{3,}'), '...', 'Normalize ellipsis'),
            (re.compile(r'!{2,}'), '!', 'Remove excessive exclamation'),
            (re.compile(r'\?{2,}'), '?', 'Remove excessive question marks'),
            (re.compile(r'([.!?])\1+'), r'\1', 'Remove duplicate punctuation'),
            (re.compile(r'\s([.!?,;:])'), r'\1', 'Fix space before punctuation'),
            (re.compile(r'([.!?])([A-ZА-ЯА-ЯΆΈΉΊΌΎΏА-Я\u0600-\u06FF])'), r'\1 \2', 'Add space after sentence end'),
            (re.compile(r'([a-z])([A-Z])'), r'\1 \2', 'Split camelCase words'),
            (re.compile(r'(\d)([A-Za-z])'), r'\1 \2', 'Separate numbers from letters'),
            (re.compile(r'([A-Za-z])(\d)'), r'\1 \2', 'Separate letters from numbers'),
        ]

    def detect_script(self, char: str) -> Optional[str]:
        """
        Detect which script a character belongs to

        Args:
            char: Single character to analyze

        Returns:
            Script name or None
        """
        if not char:
            return None

        code_point = ord(char)

        for script_name, (start, end) in self.script_ranges.items():
            if start <= code_point <= end:
                return script_name

        return None

    def add_script_boundaries(self, text: str) -> str:
        """
        Add spaces at script boundaries to improve readability

        Args:
            text: Input text with potential mixed scripts

        Returns:
            Text with proper script boundaries
        """
        if not text or len(text) < 2:
            return text

        result = [text[0]]
        prev_script = self.detect_script(text[0])

        for i in range(1, len(text)):
            curr_char = text[i]
            curr_script = self.detect_script(curr_char)

            # Check if we're crossing script boundaries
            if (prev_script and curr_script and
                prev_script != curr_script and
                not curr_char.isspace() and
                not text[i-1].isspace()):

                # Don't add space if previous char is punctuation
                if not text[i-1] in '.!?,;:':
                    result.append(' ')

            result.append(curr_char)

            if curr_script:
                prev_script = curr_script

        return ''.join(result)

    def fix_rtl_ltr_mixing(self, text: str) -> str:
        """
        Handle mixed right-to-left and left-to-right text

        Args:
            text: Text with potentially mixed directionality

        Returns:
            Text with improved directionality handling
        """
        # Add zero-width markers for better rendering (optional)
        # For now, just ensure proper spacing
        return self.add_script_boundaries(text)

    def repair_word_breaks(self, text: str) -> str:
        """
        Attempt to repair broken words

        Args:
            text: Text with potential word breaks

        Returns:
            Repaired text
        """
        # Fix common patterns where words are concatenated
        repaired = text

        # Split concatenated words at case changes
        repaired = re.sub(r'([a-z])([A-Z])', r'\1 \2', repaired)

        # Fix missing spaces after punctuation
        repaired = re.sub(r'([.!?;:])([A-Za-zА-Я\u0600-\u06FF])', r'\1 \2', repaired)

        return repaired

    def normalize_punctuation(self, text: str) -> str:
        """
        Normalize punctuation marks

        Args:
            text: Text with potentially malformed punctuation

        Returns:
            Text with normalized punctuation
        """
        normalized = text

        # Fix multiple consecutive punctuation marks
        normalized = re.sub(r'([.!?]){2,}', r'\1', normalized)

        # Fix spaces around punctuation
        normalized = re.sub(r'\s+([.!?,;:])', r'\1', normalized)
        normalized = re.sub(r'([.!?])\s{2,}', r'\1 ', normalized)

        # Fix Arabic punctuation
        normalized = re.sub(r'،\s*،+', '،', normalized)  # Arabic comma
        normalized = re.sub(r'؛\s*؛+', '؛', normalized)  # Arabic semicolon

        return normalized

    def repair_text(self, text: str, aggressive: bool = False) -> RepairResult:
        """
        Main repair function that applies all repair strategies

        Args:
            text: Input text to repair
            aggressive: If True, apply more aggressive repair strategies

        Returns:
            RepairResult object with repair details
        """
        if not text:
            return RepairResult(
                original="",
                repaired="",
                changes_made=["Empty input"],
                confidence=1.0
            )

        changes = []
        repaired = text

        # Step 1: Normalize whitespace
        before = repaired
        repaired = re.sub(r'\s+', ' ', repaired).strip()
        if before != repaired:
            changes.append("Normalized whitespace")

        # Step 2: Apply standard repair patterns
        for pattern, replacement, description in self.repair_patterns:
            before = repaired
            repaired = pattern.sub(replacement, repaired)
            if before != repaired:
                changes.append(description)

        # Step 3: Fix script boundaries
        before = repaired
        repaired = self.add_script_boundaries(repaired)
        if before != repaired:
            changes.append("Added script boundaries")

        # Step 4: Repair word breaks
        before = repaired
        repaired = self.repair_word_breaks(repaired)
        if before != repaired:
            changes.append("Repaired word breaks")

        # Step 5: Normalize punctuation
        before = repaired
        repaired = self.normalize_punctuation(repaired)
        if before != repaired:
            changes.append("Normalized punctuation")

        # Step 6: Fix RTL/LTR mixing
        before = repaired
        repaired = self.fix_rtl_ltr_mixing(repaired)
        if before != repaired:
            changes.append("Fixed RTL/LTR mixing")

        # Calculate confidence based on number of changes
        confidence = 1.0
        if len(changes) > 0:
            # More changes = lower confidence
            confidence = max(0.5, 1.0 - (len(changes) * 0.05))

        return RepairResult(
            original=text,
            repaired=repaired.strip(),
            changes_made=changes if changes else ["No changes needed"],
            confidence=confidence
        )

    def batch_repair(self, texts: List[str]) -> List[RepairResult]:
        """
        Repair multiple texts

        Args:
            texts: List of texts to repair

        Returns:
            List of RepairResult objects
        """
        return [self.repair_text(text) for text in texts]


def repair_multilingual_text(text: str, aggressive: bool = False) -> Dict[str, any]:
    """
    Convenience function to repair multilingual text

    Args:
        text: Text to repair
        aggressive: Use aggressive repair strategies

    Returns:
        Dictionary with repair results
    """
    repairer = MultilingualTextRepairer()
    result = repairer.repair_text(text, aggressive)

    return {
        "original": result.original,
        "repaired": result.repaired,
        "changes": result.changes_made,
        "confidence": result.confidence,
        "improvement_ratio": len(result.changes_made) / max(1, len(text.split()))
    }


if __name__ == "__main__":
    # Example usage and testing
    print("=== Multilingual Text Repair System ===\n")

    # Test case 1: Arabic text with spacing issues
    test1 = "فقط سوال لا تبني هل هنالك مستودعات"
    print(f"Test 1 - Arabic: {test1}")
    result1 = repair_multilingual_text(test1)
    print(f"Repaired: {result1['repaired']}")
    print(f"Changes: {result1['changes']}\n")

    # Test case 2: Mixed language without spaces
    test2 = "HelloWorldهذا عربيMoreText"
    print(f"Test 2 - Mixed: {test2}")
    result2 = repair_multilingual_text(test2)
    print(f"Repaired: {result2['repaired']}")
    print(f"Changes: {result2['changes']}\n")

    # Test case 3: Text with punctuation issues
    test3 = "This is broken...!!!And has   issues???"
    print(f"Test 3 - Punctuation: {test3}")
    result3 = repair_multilingual_text(test3)
    print(f"Repaired: {result3['repaired']}")
    print(f"Changes: {result3['changes']}\n")

    # Test case 4: RTL/LTR mixing
    test4 = "Englishنص عربيMoreEnglish"
    print(f"Test 4 - RTL/LTR: {test4}")
    result4 = repair_multilingual_text(test4)
    print(f"Repaired: {result4['repaired']}")
    print(f"Changes: {result4['changes']}\n")
