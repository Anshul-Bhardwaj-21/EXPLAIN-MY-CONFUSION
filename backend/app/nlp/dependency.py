"""
Dependency parsing module
Analyzes grammatical structure and relationships in text
"""

from typing import List, Dict, Any, Tuple
import nltk
import re
import logging

logger = logging.getLogger(__name__)

class DependencyParser:
    """
    Handles dependency parsing and syntactic analysis using NLTK
    """
    
    def __init__(self):
        # Initialize NLTK components
        self._download_nltk_data()
        
        # Causal relationship patterns
        self.causal_patterns = [
            r'because\s+(.+)',
            r'since\s+(.+)',
            r'due to\s+(.+)',
            r'as a result of\s+(.+)',
            r'therefore\s+(.+)',
            r'thus\s+(.+)',
            r'consequently\s+(.+)',
            r'leads to\s+(.+)',
            r'causes\s+(.+)',
            r'results in\s+(.+)'
        ]
        
        # Comparison patterns
        self.comparison_patterns = [
            r'unlike\s+(.+)',
            r'similar to\s+(.+)',
            r'different from\s+(.+)',
            r'compared to\s+(.+)',
            r'versus\s+(.+)',
            r'rather than\s+(.+)'
        ]
    
    def _download_nltk_data(self):
        """Download required NLTK data"""
        required_data = ['punkt', 'averaged_perceptron_tagger', 'maxent_ne_chunker', 'words']
        
        for data in required_data:
            try:
                nltk.data.find(f'tokenizers/{data}')
            except LookupError:
                try:
                    nltk.data.find(f'taggers/{data}')
                except LookupError:
                    try:
                        nltk.data.find(f'chunkers/{data}')
                    except LookupError:
                        try:
                            nltk.data.find(f'corpora/{data}')
                        except LookupError:
                            try:
                                nltk.download(data, quiet=True)
                            except Exception as e:
                                logger.warning(f"Failed to download {data}: {e}")
    
    def parse_dependencies(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract dependency relationships from text using NLTK
        """
        try:
            from nltk.tokenize import sent_tokenize, word_tokenize
            from nltk.tag import pos_tag
            
            sentences = sent_tokenize(text)
            dependencies = []
            
            for sentence in sentences:
                tokens = word_tokenize(sentence)
                pos_tags = pos_tag(tokens)
                
                # Simple dependency extraction based on POS patterns
                for i, (word, pos) in enumerate(pos_tags):
                    if pos.startswith('VB'):  # Verb
                        # Look for subject (noun before verb)
                        subject = None
                        for j in range(i-1, -1, -1):
                            if pos_tags[j][1].startswith('NN'):
                                subject = pos_tags[j][0]
                                break
                        
                        # Look for object (noun after verb)
                        obj = None
                        for j in range(i+1, len(pos_tags)):
                            if pos_tags[j][1].startswith('NN'):
                                obj = pos_tags[j][0]
                                break
                        
                        if subject or obj:
                            dependencies.append({
                                'sentence': sentence,
                                'verb': word,
                                'subject': subject,
                                'object': obj,
                                'relation_type': 'subject-verb-object'
                            })
            
            return dependencies
            
        except Exception as e:
            logger.error(f"Dependency parsing failed: {e}")
            return []
    
    def extract_subject_verb_object(self, text: str) -> List[Tuple[str, str, str]]:
        """
        Extract subject-verb-object triples
        """
        dependencies = self.parse_dependencies(text)
        svo_triples = []
        
        for dep in dependencies:
            if dep['subject'] and dep['verb'] and dep['object']:
                svo_triples.append((dep['subject'], dep['verb'], dep['object']))
        
        return svo_triples
    
    def find_concept_relationships(self, text: str) -> List[Dict[str, Any]]:
        """
        Identify relationships between concepts mentioned in text
        """
        relationships = []
        text_lower = text.lower()
        
        # Find causal relationships
        causal_rels = self.extract_causal_relationships(text)
        relationships.extend(causal_rels)
        
        # Find comparison relationships
        comparison_rels = self.extract_comparison_relationships(text)
        relationships.extend(comparison_rels)
        
        # Find definitional relationships
        definitional_rels = self.extract_definitional_relationships(text)
        relationships.extend(definitional_rels)
        
        return relationships
    
    def extract_causal_relationships(self, text: str) -> List[Dict[str, Any]]:
        """
        Identify cause-effect relationships in explanations
        """
        causal_relationships = []
        text_lower = text.lower()
        
        for pattern in self.causal_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                cause_effect = match.group(1).strip()
                relationship = {
                    'type': 'causal',
                    'pattern': pattern,
                    'cause_effect': cause_effect,
                    'full_match': match.group(0),
                    'position': match.span()
                }
                causal_relationships.append(relationship)
        
        return causal_relationships
    
    def extract_comparison_relationships(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract comparison relationships
        """
        comparison_relationships = []
        text_lower = text.lower()
        
        for pattern in self.comparison_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                compared_item = match.group(1).strip()
                relationship = {
                    'type': 'comparison',
                    'pattern': pattern,
                    'compared_item': compared_item,
                    'full_match': match.group(0),
                    'position': match.span()
                }
                comparison_relationships.append(relationship)
        
        return comparison_relationships
    
    def extract_definitional_relationships(self, text: str) -> List[Dict[str, Any]]:
        """
        Extract definitional relationships (X is Y, X means Y, etc.)
        """
        definitional_relationships = []
        text_lower = text.lower()
        
        definitional_patterns = [
            r'(.+?)\s+is\s+(.+?)(?:\.|$)',
            r'(.+?)\s+means\s+(.+?)(?:\.|$)',
            r'(.+?)\s+refers to\s+(.+?)(?:\.|$)',
            r'(.+?)\s+defined as\s+(.+?)(?:\.|$)'
        ]
        
        for pattern in definitional_patterns:
            matches = re.finditer(pattern, text_lower)
            for match in matches:
                term = match.group(1).strip()
                definition = match.group(2).strip()
                
                # Filter out very short or common terms
                if len(term) > 2 and len(definition) > 5:
                    relationship = {
                        'type': 'definitional',
                        'term': term,
                        'definition': definition,
                        'full_match': match.group(0),
                        'position': match.span()
                    }
                    definitional_relationships.append(relationship)
        
        return definitional_relationships
    
    def analyze_explanation_coherence(self, text: str) -> Dict[str, Any]:
        """
        Analyze the coherence and structure of an explanation
        """
        try:
            from nltk.tokenize import sent_tokenize
            
            sentences = sent_tokenize(text)
            
            # Count different types of relationships
            causal_count = len(self.extract_causal_relationships(text))
            comparison_count = len(self.extract_comparison_relationships(text))
            definitional_count = len(self.extract_definitional_relationships(text))
            
            # Analyze sentence transitions
            transition_words = [
                'however', 'therefore', 'furthermore', 'moreover', 'additionally',
                'consequently', 'nevertheless', 'meanwhile', 'similarly', 'likewise'
            ]
            
            transition_count = sum(1 for word in transition_words if word in text.lower())
            
            coherence_score = min(1.0, (causal_count + comparison_count + definitional_count + transition_count) / len(sentences))
            
            return {
                'sentence_count': len(sentences),
                'causal_relationships': causal_count,
                'comparison_relationships': comparison_count,
                'definitional_relationships': definitional_count,
                'transition_words': transition_count,
                'coherence_score': coherence_score,
                'avg_sentence_length': len(text.split()) / len(sentences) if sentences else 0
            }
            
        except Exception as e:
            logger.error(f"Coherence analysis failed: {e}")
            return {
                'sentence_count': 0,
                'causal_relationships': 0,
                'comparison_relationships': 0,
                'definitional_relationships': 0,
                'transition_words': 0,
                'coherence_score': 0.0,
                'avg_sentence_length': 0.0
            }