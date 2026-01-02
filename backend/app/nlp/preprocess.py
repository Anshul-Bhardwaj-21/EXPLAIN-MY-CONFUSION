"""
Text preprocessing module
Handles tokenization, lemmatization, and text cleaning with real NLP
"""

import re
import string
from typing import List, Dict, Any, Set
from collections import Counter

class TextPreprocessor:
    """
    Handles all text preprocessing operations with real NLP capabilities
    """
    
    def __init__(self):
        # Initialize with basic NLP tools
        self.stop_words = {
            'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
            'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
            'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
            'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
            'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
            'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
            'while', 'of', 'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after',
            'above', 'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
            'further', 'then', 'once'
        }
        
        # CS-specific terms that should NOT be removed
        self.cs_preserve_terms = {
            'algorithm', 'data', 'structure', 'tree', 'node', 'graph', 'array', 'list', 'stack',
            'queue', 'hash', 'sort', 'search', 'time', 'space', 'complexity', 'big', 'o',
            'recursion', 'iteration', 'loop', 'function', 'method', 'class', 'object',
            'database', 'table', 'query', 'index', 'key', 'value', 'network', 'protocol',
            'tcp', 'ip', 'http', 'process', 'thread', 'memory', 'cpu', 'operating', 'system'
        }
    
    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s\-\(\)\[\]\/\.]', ' ', text)
        
        # Remove extra spaces
        text = text.strip()
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into meaningful terms
        """
        # Clean text first
        cleaned_text = self.clean_text(text)
        
        # Split into tokens
        tokens = cleaned_text.split()
        
        # Remove punctuation and empty tokens
        tokens = [token.strip(string.punctuation) for token in tokens if token.strip(string.punctuation)]
        
        # Filter out very short tokens (but keep important CS terms)
        tokens = [token for token in tokens if len(token) > 2 or token in self.cs_preserve_terms]
        
        return tokens
    
    def extract_key_terms(self, text: str) -> List[str]:
        """
        Extract key technical terms from text
        """
        tokens = self.tokenize(text)
        
        # Remove stop words but preserve CS terms
        filtered_tokens = []
        for token in tokens:
            if token not in self.stop_words or token in self.cs_preserve_terms:
                filtered_tokens.append(token)
        
        # Count frequency and return most common terms
        term_counts = Counter(filtered_tokens)
        
        # Return terms sorted by frequency
        return [term for term, count in term_counts.most_common(20)]
    
    def extract_technical_phrases(self, text: str) -> List[str]:
        """
        Extract multi-word technical phrases
        """
        # Common CS phrase patterns
        cs_patterns = [
            r'binary search tree',
            r'linked list',
            r'hash table',
            r'time complexity',
            r'space complexity',
            r'big o',
            r'data structure',
            r'sorting algorithm',
            r'search algorithm',
            r'graph algorithm',
            r'dynamic programming',
            r'divide and conquer',
            r'greedy algorithm',
            r'breadth first',
            r'depth first',
            r'operating system',
            r'process scheduling',
            r'memory management',
            r'tcp ip',
            r'network protocol',
            r'database management',
            r'acid properties',
            r'sql query'
        ]
        
        phrases = []
        text_lower = text.lower()
        
        for pattern in cs_patterns:
            if re.search(pattern, text_lower):
                phrases.append(pattern.replace(' ', '_'))
        
        return phrases
    
    def analyze_explanation_structure(self, text: str) -> Dict[str, Any]:
        """
        Analyze the structure and quality of the explanation
        """
        sentences = text.split('.')
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # Count different types of content
        definition_indicators = ['is', 'are', 'means', 'refers to', 'defined as']
        example_indicators = ['example', 'for instance', 'such as', 'like']
        process_indicators = ['first', 'then', 'next', 'finally', 'step']
        comparison_indicators = ['unlike', 'similar to', 'compared to', 'different from']
        
        structure_analysis = {
            'sentence_count': len(sentences),
            'word_count': len(text.split()),
            'has_definition': any(indicator in text.lower() for indicator in definition_indicators),
            'has_examples': any(indicator in text.lower() for indicator in example_indicators),
            'has_process_description': any(indicator in text.lower() for indicator in process_indicators),
            'has_comparisons': any(indicator in text.lower() for indicator in comparison_indicators),
            'technical_density': len(self.extract_key_terms(text)) / max(len(text.split()), 1)
        }
        
        return structure_analysis
    
    def extract_concept_mentions(self, text: str, known_concepts: List[str]) -> List[str]:
        """
        Find mentions of known concepts in the text
        """
        text_lower = text.lower()
        mentioned_concepts = []
        
        for concept in known_concepts:
            # Check for exact matches and variations
            concept_variations = [
                concept.replace('_', ' '),
                concept.replace('_', '-'),
                concept.replace('_', ''),
                concept
            ]
            
            for variation in concept_variations:
                if variation.lower() in text_lower:
                    mentioned_concepts.append(concept)
                    break
        
        return list(set(mentioned_concepts))