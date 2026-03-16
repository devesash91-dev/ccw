#!/usr/bin/env python3
"""
Speech Fragment Reconstruction Module
Reconstructs coherent text from fragmented or broken speech input
"""

import re
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict


@dataclass
class Fragment:
    """Represents a text fragment"""
    content: str
    position: int
    confidence: float
    fragment_type: str  # 'complete', 'partial', 'corrupted'
    language_hint: Optional[str] = None


@dataclass
class ReconstructionResult:
    """Result of speech reconstruction"""
    original_fragments: List[Fragment]
    reconstructed_text: str
    confidence: float
    method_used: str
    fragments_merged: int


class SpeechFragmentReconstructor:
    """
    Reconstructs coherent text from fragmented speech input
    Handles various types of corruption and fragmentation
    """

    def __init__(self):
        # Patterns for detecting fragment boundaries
        self.fragment_indicators = [
            re.compile(r'\.\.\.$'),  # Trailing ellipsis
            re.compile(r'^\.\.\.'),  # Leading ellipsis
            re.compile(r'\s+\.\s+$'),  # Trailing incomplete sentence
            re.compile(r'^\s*[-–—]\s*'),  # Leading dash
            re.compile(r'\s+[-–—]\s*$'),  # Trailing dash
        ]

        # Common speech disfluencies
        self.disfluencies = {
            'um', 'uh', 'er', 'ah', 'like', 'you know',
            'so', 'well', 'I mean', 'basically', 'actually'
        }

    def classify_fragment(self, text: str) -> str:
        """
        Classify a text fragment based on its characteristics

        Args:
            text: Fragment text

        Returns:
            Classification: 'complete', 'partial', or 'corrupted'
        """
        if not text or not text.strip():
            return 'corrupted'

        text = text.strip()

        # Check for fragment indicators
        for pattern in self.fragment_indicators:
            if pattern.search(text):
                return 'partial'

        # Check if it ends with proper punctuation
        if text[-1] in '.!?؟':
            return 'complete'

        # Check for extremely short fragments
        if len(text.split()) < 2:
            return 'partial'

        # Default to partial if unsure
        return 'partial'

    def remove_disfluencies(self, text: str) -> str:
        """
        Remove speech disfluencies from text

        Args:
            text: Input text with potential disfluencies

        Returns:
            Cleaned text
        """
        words = text.split()
        cleaned_words = []

        for word in words:
            # Remove punctuation for comparison
            word_clean = word.lower().strip('.,!?;:')

            # Skip if it's a disfluency
            if word_clean not in self.disfluencies:
                cleaned_words.append(word)

        return ' '.join(cleaned_words)

    def merge_fragments(self, fragments: List[Fragment]) -> str:
        """
        Merge text fragments intelligently

        Args:
            fragments: List of Fragment objects to merge

        Returns:
            Merged text
        """
        if not fragments:
            return ""

        if len(fragments) == 1:
            return fragments[0].content.strip()

        merged_parts = []

        for i, fragment in enumerate(fragments):
            content = fragment.content.strip()

            # Remove leading/trailing ellipsis
            content = re.sub(r'^\.\.\.+\s*', '', content)
            content = re.sub(r'\s*\.\.\.+$', '', content)

            # Remove leading dash if not first fragment
            if i > 0:
                content = re.sub(r'^\s*[-–—]\s*', '', content)

            # Remove trailing dash if not last fragment
            if i < len(fragments) - 1:
                content = re.sub(r'\s*[-–—]\s*$', '', content)

            if content:
                merged_parts.append(content)

        # Join with appropriate spacing
        result = ' '.join(merged_parts)

        # Clean up excessive spacing
        result = re.sub(r'\s+', ' ', result)

        return result.strip()

    def detect_continuation_patterns(self, frag1: str, frag2: str) -> bool:
        """
        Detect if two fragments are likely continuations of each other

        Args:
            frag1: First fragment
            frag2: Second fragment

        Returns:
            True if fragments appear to be continuations
        """
        # Check for explicit continuation markers
        continuation_patterns = [
            (r'\.\.\.$', r'^\.\.\.'),  # Ellipsis connection
            (r'[-–—]$', r'^[-–—]'),  # Dash connection
            (r'\,$', None),  # Trailing comma
        ]

        frag1 = frag1.strip()
        frag2 = frag2.strip()

        for end_pattern, start_pattern in continuation_patterns:
            if end_pattern and re.search(end_pattern, frag1):
                if start_pattern is None or re.match(start_pattern, frag2):
                    return True

        # Check if first fragment is incomplete (no terminal punctuation)
        if frag1 and frag1[-1] not in '.!?؟' and len(frag1) > 3:
            # Check if second fragment continues naturally (starts with lowercase)
            if frag2 and frag2[0].islower():
                return True

        return False

    def reconstruct_from_fragments(
        self,
        fragments: List[str],
        fragment_confidence: Optional[List[float]] = None
    ) -> ReconstructionResult:
        """
        Main reconstruction method

        Args:
            fragments: List of text fragments
            fragment_confidence: Optional confidence scores for each fragment

        Returns:
            ReconstructionResult object
        """
        if not fragments:
            return ReconstructionResult(
                original_fragments=[],
                reconstructed_text="",
                confidence=0.0,
                method_used="none",
                fragments_merged=0
            )

        # Convert to Fragment objects
        fragment_objects = []
        for i, frag_text in enumerate(fragments):
            confidence = fragment_confidence[i] if fragment_confidence else 0.8
            frag_type = self.classify_fragment(frag_text)

            fragment_objects.append(Fragment(
                content=frag_text,
                position=i,
                confidence=confidence,
                fragment_type=frag_type
            ))

        # Remove disfluencies from each fragment
        cleaned_fragments = []
        for frag in fragment_objects:
            cleaned_content = self.remove_disfluencies(frag.content)
            cleaned_fragments.append(Fragment(
                content=cleaned_content,
                position=frag.position,
                confidence=frag.confidence,
                fragment_type=frag.fragment_type,
                language_hint=frag.language_hint
            ))

        # Merge fragments
        reconstructed = self.merge_fragments(cleaned_fragments)

        # Calculate overall confidence
        avg_confidence = sum(f.confidence for f in fragment_objects) / len(fragment_objects)

        # Adjust confidence based on fragment types
        complete_count = sum(1 for f in fragment_objects if f.fragment_type == 'complete')
        confidence_adjustment = complete_count / len(fragment_objects)
        final_confidence = (avg_confidence + confidence_adjustment) / 2

        return ReconstructionResult(
            original_fragments=fragment_objects,
            reconstructed_text=reconstructed,
            confidence=min(1.0, final_confidence),
            method_used="merge_with_disfluency_removal",
            fragments_merged=len(fragments)
        )

    def reconstruct_broken_speech(
        self,
        text: str,
        split_pattern: Optional[str] = None
    ) -> ReconstructionResult:
        """
        Reconstruct speech from a single broken text string

        Args:
            text: Broken speech text
            split_pattern: Optional regex pattern to split text into fragments

        Returns:
            ReconstructionResult object
        """
        if not text or not text.strip():
            return ReconstructionResult(
                original_fragments=[],
                reconstructed_text="",
                confidence=0.0,
                method_used="none",
                fragments_merged=0
            )

        # Default split pattern: split on multiple spaces or ellipsis
        if split_pattern is None:
            split_pattern = r'\s{3,}|\.\.\.+'

        # Split into fragments
        fragments = re.split(split_pattern, text)
        fragments = [f.strip() for f in fragments if f.strip()]

        return self.reconstruct_from_fragments(fragments)

    def smart_reconstruct(self, text: str) -> Dict[str, any]:
        """
        Intelligently reconstruct text using multiple strategies

        Args:
            text: Input text to reconstruct

        Returns:
            Dictionary with reconstruction results
        """
        # Try different reconstruction strategies
        strategies = [
            ("standard", None),
            ("aggressive", r'\s{2,}'),
            ("sentence_based", r'[.!?؟]\s+'),
        ]

        results = []

        for strategy_name, pattern in strategies:
            result = self.reconstruct_broken_speech(text, pattern)
            results.append({
                "strategy": strategy_name,
                "text": result.reconstructed_text,
                "confidence": result.confidence,
                "fragments": result.fragments_merged
            })

        # Select best result based on confidence
        best_result = max(results, key=lambda x: x['confidence'])

        return {
            "original": text,
            "reconstructed": best_result['text'],
            "confidence": best_result['confidence'],
            "strategy_used": best_result['strategy'],
            "fragments_processed": best_result['fragments'],
            "all_attempts": results
        }


def reconstruct_speech(
    text: str,
    fragments: Optional[List[str]] = None
) -> Dict[str, any]:
    """
    Convenience function for speech reconstruction

    Args:
        text: Broken speech text (if fragments not provided)
        fragments: Optional list of pre-split fragments

    Returns:
        Dictionary with reconstruction results
    """
    reconstructor = SpeechFragmentReconstructor()

    if fragments:
        result = reconstructor.reconstruct_from_fragments(fragments)
        return {
            "original": fragments,
            "reconstructed": result.reconstructed_text,
            "confidence": result.confidence,
            "method": result.method_used,
            "fragments_merged": result.fragments_merged
        }
    else:
        return reconstructor.smart_reconstruct(text)


if __name__ == "__main__":
    # Example usage and testing
    print("=== Speech Fragment Reconstruction System ===\n")

    # Test case 1: Fragmented sentence
    test1 = "فقط سوال ... لا تبني ... هل هنالك مستودعات"
    print(f"Test 1 - Fragmented Arabic: {test1}")
    result1 = reconstruct_speech(test1)
    print(f"Reconstructed: {result1['reconstructed']}")
    print(f"Confidence: {result1['confidence']:.2%}\n")

    # Test case 2: Multiple fragments with disfluencies
    test2 = "This is um... like broken text... you know... that needs fixing"
    print(f"Test 2 - With disfluencies: {test2}")
    result2 = reconstruct_speech(test2)
    print(f"Reconstructed: {result2['reconstructed']}")
    print(f"Confidence: {result2['confidence']:.2%}\n")

    # Test case 3: Fragment list
    test3_fragments = [
        "The beginning of a sentence...",
        "...the middle part...",
        "...and the end."
    ]
    print(f"Test 3 - Fragment list: {test3_fragments}")
    result3 = reconstruct_speech("", fragments=test3_fragments)
    print(f"Reconstructed: {result3['reconstructed']}")
    print(f"Confidence: {result3['confidence']:.2%}\n")

    # Test case 4: Mixed language fragmented
    test4 = "English text   وهذا نص عربي   more English"
    print(f"Test 4 - Mixed fragmented: {test4}")
    result4 = reconstruct_speech(test4)
    print(f"Reconstructed: {result4['reconstructed']}")
    print(f"Confidence: {result4['confidence']:.2%}\n")
