"""
Text utility functions
Common text processing and validation utilities
"""

import re
from typing import List, Dict, Any

def clean_whitespace(text: str) -> str:
    """
    Clean excessive whitespace from text
    """
    return re.sub(r'\s+', ' ', text.strip())

def validate_text_length(text: str, max_length: int = 5000) -> bool:
    """
    Validate text length is within acceptable limits
    """
    return len(text) <= max_length

def extract_sentences(text: str) -> List[str]:
    """
    Split text into sentences
    """
    # Basic sentence splitting - will be enhanced later
    sentences = re.split(r'[.!?]+', text)
    return [s.strip() for s in sentences if s.strip()]

def normalize_concept_name(concept: str) -> str:
    """
    Normalize concept names for consistent matching
    """
    return concept.lower().strip().replace(' ', '_')

def calculate_text_similarity_score(text1: str, text2: str) -> float:
    """
    Calculate basic text similarity score
    """
    # Placeholder for similarity calculation
    # Will be implemented with proper NLP techniques later
    return 0.0