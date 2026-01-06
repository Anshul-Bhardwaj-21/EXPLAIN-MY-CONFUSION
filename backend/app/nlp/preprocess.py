"""
Real NLP preprocessing using NLTK (Windows compatible)
Handles tokenization, lemmatization, and concept extraction
"""

import nltk
from typing import List, Dict, Any, Set
import logging
from collections import Counter
import re

logger = logging.getLogger(__name__)

class RealNLPProcessor:
    """
    Real NLP processing using NLTK (Windows compatible)
    """
    
    def __init__(self):
        self._download_nltk_data()
    
    def _download_nltk_data(self):
        """
        Download required NLTK data
        """
        required_data = [
            'punkt',
            'stopwords', 
            'averaged_perceptron_tagger',
            'wordnet',
            'omw-1.4'
        ]
        
        for data in required_data:
            try:
                nltk.data.find(f'tokenizers/{data}')
            except LookupError:
                try:
                    nltk.data.find(f'corpora/{data}')
                except LookupError:
                    try:
                        nltk.data.find(f'taggers/{data}')
                    except LookupError:
                        try:
                            logger.info(f"Downloading NLTK data: {data}")
                            nltk.download(data, quiet=True)
                        except Exception as e:
                            logger.warning(f"Failed to download {data}: {e}")
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words
        """
        from nltk.tokenize import word_tokenize
        try:
            return word_tokenize(text)
        except Exception as e:
            logger.warning(f"Tokenization failed, using simple split: {e}")
            return text.split()
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Remove common stopwords
        """
        try:
            from nltk.corpus import stopwords
            stop_words = set(stopwords.words('english'))
        except Exception as e:
            logger.warning(f"Stopwords not available, using basic list: {e}")
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        # Keep tokens that are not stopwords and are alphabetic
        return [token.lower() for token in tokens 
                if token.lower() not in stop_words and token.isalpha() and len(token) > 2]
    
    def lemmatize(self, tokens: List[str]) -> List[str]:
        """
        Lemmatize tokens to their base forms
        """
        try:
            from nltk.stem import WordNetLemmatizer
            lemmatizer = WordNetLemmatizer()
            return [lemmatizer.lemmatize(token.lower()) for token in tokens if token.isalpha()]
        except Exception as e:
            logger.warning(f"Lemmatization failed, returning lowercase tokens: {e}")
            return [token.lower() for token in tokens if token.isalpha()]
    
    def segment_sentences(self, text: str) -> List[str]:
        """
        Split text into sentences
        """
        try:
            from nltk.tokenize import sent_tokenize
            return sent_tokenize(text)
        except Exception as e:
            logger.warning(f"Sentence segmentation failed, using simple split: {e}")
            # Simple fallback
            sentences = re.split(r'[.!?]+', text)
            return [s.strip() for s in sentences if s.strip()]
    
    def extract_noun_phrases(self, text: str) -> List[str]:
        """
        Extract noun phrases from text using POS tagging
        """
        try:
            from nltk.tokenize import word_tokenize
            from nltk.tag import pos_tag
            
            tokens = word_tokenize(text)
            pos_tags = pos_tag(tokens)
            
            noun_phrases = []
            current_phrase = []
            
            for word, pos in pos_tags:
                if pos.startswith('NN') or pos.startswith('JJ'):  # Nouns and adjectives
                    current_phrase.append(word)
                else:
                    if len(current_phrase) > 1:
                        phrase = ' '.join(current_phrase).lower()
                        if len(phrase) > 3:
                            noun_phrases.append(phrase)
                    current_phrase = []
            
            # Don't forget the last phrase
            if len(current_phrase) > 1:
                phrase = ' '.join(current_phrase).lower()
                if len(phrase) > 3:
                    noun_phrases.append(phrase)
            
            return noun_phrases
            
        except Exception as e:
            logger.warning(f"Noun phrase extraction failed: {e}")
            # Simple fallback - extract multi-word sequences
            words = text.lower().split()
            phrases = []
            for i in range(len(words) - 1):
                if len(words[i]) > 3 and len(words[i+1]) > 3:
                    phrase = f"{words[i]} {words[i+1]}"
                    phrases.append(phrase)
            return phrases[:10]  # Limit results
    
    def extract_key_terms(self, text: str) -> List[str]:
        """
        Extract key terms using multiple methods
        """
        # Method 1: Tokenization + stopword removal + lemmatization
        tokens = self.tokenize(text)
        clean_tokens = self.remove_stopwords(tokens)
        lemmatized = self.lemmatize(clean_tokens)
        
        # Method 2: Noun phrases
        noun_phrases = self.extract_noun_phrases(text)
        
        # Method 3: Extract capitalized words (potential proper nouns)
        capitalized = [word.lower() for word in tokens if word.istitle() and len(word) > 2]
        
        # Combine all methods
        all_terms = lemmatized + noun_phrases + capitalized
        
        # Count frequency and return most common
        term_counts = Counter(all_terms)
        
        # Filter out very short terms and return top terms
        filtered_terms = [(term, count) for term, count in term_counts.items() 
                         if len(term) > 2 and count > 0]
        
        # Sort by frequency and return terms
        sorted_terms = sorted(filtered_terms, key=lambda x: x[1], reverse=True)
        return [term for term, count in sorted_terms[:20]]
    
    def analyze_text_structure(self, text: str) -> Dict[str, Any]:
        """
        Analyze the structure and properties of the text
        """
        sentences = self.segment_sentences(text)
        tokens = self.tokenize(text)
        key_terms = self.extract_key_terms(text)
        
        # Calculate basic statistics
        word_count = len([token for token in tokens if token.isalpha()])
        sentence_count = len(sentences)
        avg_sentence_length = word_count / max(sentence_count, 1)
        
        # Analyze complexity
        complex_words = [token for token in tokens if len(token) > 6]
        complexity_ratio = len(complex_words) / max(word_count, 1)
        
        return {
            'word_count': word_count,
            'sentence_count': sentence_count,
            'avg_sentence_length': avg_sentence_length,
            'key_terms': key_terms,
            'complexity_ratio': complexity_ratio,
            'sentences': sentences
        }
    
    def preprocess_for_comparison(self, text: str) -> Dict[str, Any]:
        """
        Complete preprocessing pipeline for concept comparison
        """
        # Basic analysis
        structure = self.analyze_text_structure(text)
        
        # Extract different types of concepts
        key_terms = self.extract_key_terms(text)
        noun_phrases = self.extract_noun_phrases(text)
        
        # Clean and normalize
        normalized_text = text.lower().strip()
        
        return {
            'original_text': text,
            'normalized_text': normalized_text,
            'structure': structure,
            'key_terms': key_terms,
            'noun_phrases': noun_phrases,
            'processed': True
        }