"""
Concept Analysis Engine
Analyzes student explanations to identify understood, misunderstood, and missing concepts
"""

import re
from typing import Dict, List, Tuple, Set
from collections import defaultdict
import math

from app.knowledge.cs_concepts import CS_CONCEPTS, get_concept_by_name, find_related_concepts
from app.nlp.preprocess import TextPreprocessor

class ConceptAnalyzer:
    """
    Analyzes text to determine concept understanding
    """
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        
        # Positive indicators for understanding
        self.understanding_indicators = {
            'strong': ['efficiently', 'optimal', 'because', 'therefore', 'results in', 'leads to', 'causes'],
            'medium': ['works by', 'functions by', 'operates by', 'used for', 'helps to', 'allows'],
            'weak': ['is', 'are', 'has', 'have', 'contains', 'includes']
        }
        
        # Negative indicators (misconceptions)
        self.misconception_indicators = [
            'always', 'never', 'impossible', 'cannot', 'must be', 'has to be',
            'only way', 'best way', 'worst way', 'fastest', 'slowest'
        ]
        
        # Uncertainty indicators
        self.uncertainty_indicators = [
            'i think', 'maybe', 'probably', 'might be', 'could be', 'seems like',
            'i believe', 'i guess', 'not sure', 'uncertain'
        ]
    
    def analyze_concept_understanding(self, text: str, target_concept: str, subject: str) -> Dict[str, any]:
        """
        Main analysis function that determines understanding level
        """
        # Get concept definition
        concept_def = get_concept_by_name(target_concept)
        if not concept_def:
            return self._create_default_analysis(target_concept)
        
        # Preprocess text
        key_terms = self.preprocessor.extract_key_terms(text)
        technical_phrases = self.preprocessor.extract_technical_phrases(text)
        structure_analysis = self.preprocessor.analyze_explanation_structure(text)
        
        # Analyze different aspects
        term_coverage = self._analyze_term_coverage(key_terms + technical_phrases, concept_def)
        understanding_quality = self._analyze_understanding_quality(text, concept_def)
        misconception_analysis = self._analyze_misconceptions(text, concept_def)
        completeness = self._analyze_completeness(text, concept_def, structure_analysis)
        
        # Calculate overall scores
        coverage_score = term_coverage['score']
        correctness_score = understanding_quality['score'] * (1 - misconception_analysis['severity'])
        confidence_score = self._calculate_confidence(text, understanding_quality, misconception_analysis)
        
        return {
            'concept_name': concept_def.name,
            'coverage_score': coverage_score,
            'correctness_score': correctness_score,
            'confidence_score': confidence_score,
            'term_coverage': term_coverage,
            'understanding_quality': understanding_quality,
            'misconceptions': misconception_analysis,
            'completeness': completeness,
            'structure_analysis': structure_analysis
        }
    
    def _analyze_term_coverage(self, extracted_terms: List[str], concept_def) -> Dict[str, any]:
        """
        Analyze how well the explanation covers key terms
        """
        key_terms_lower = [term.lower() for term in concept_def.key_terms]
        extracted_terms_lower = [term.lower() for term in extracted_terms]
        
        # Find matches
        matched_terms = []
        for term in key_terms_lower:
            for extracted in extracted_terms_lower:
                if term in extracted or extracted in term:
                    matched_terms.append(term)
                    break
        
        coverage_ratio = len(set(matched_terms)) / len(key_terms_lower) if key_terms_lower else 0
        
        return {
            'score': coverage_ratio,
            'matched_terms': list(set(matched_terms)),
            'missing_terms': [term for term in key_terms_lower if term not in matched_terms],
            'total_key_terms': len(key_terms_lower)
        }
    
    def _analyze_understanding_quality(self, text: str, concept_def) -> Dict[str, any]:
        """
        Analyze the quality of understanding demonstrated
        """
        text_lower = text.lower()
        quality_score = 0.0
        indicators_found = []
        
        # Check for different levels of understanding indicators
        for level, indicators in self.understanding_indicators.items():
            level_score = 0.8 if level == 'strong' else 0.6 if level == 'medium' else 0.4
            for indicator in indicators:
                if indicator in text_lower:
                    quality_score = max(quality_score, level_score)
                    indicators_found.append((indicator, level))
        
        # Bonus for mentioning applications
        if any(app.lower() in text_lower for app in concept_def.applications):
            quality_score += 0.1
            indicators_found.append(('applications_mentioned', 'bonus'))
        
        # Bonus for mentioning prerequisites
        if any(prereq.lower().replace('_', ' ') in text_lower for prereq in concept_def.prerequisites):
            quality_score += 0.1
            indicators_found.append(('prerequisites_mentioned', 'bonus'))
        
        return {
            'score': min(quality_score, 1.0),
            'indicators_found': indicators_found,
            'has_causal_reasoning': any(ind in text_lower for ind in ['because', 'therefore', 'since', 'due to']),
            'has_examples': any(ind in text_lower for ind in ['example', 'for instance', 'such as'])
        }
    
    def _analyze_misconceptions(self, text: str, concept_def) -> Dict[str, any]:
        """
        Identify potential misconceptions in the explanation
        """
        text_lower = text.lower()
        misconceptions_found = []
        severity = 0.0
        
        # Check for absolute statements that might indicate misconceptions
        for indicator in self.misconception_indicators:
            if indicator in text_lower:
                misconceptions_found.append(indicator)
                severity += 0.1
        
        # Check for known misconceptions specific to this concept
        for misconception in concept_def.common_misconceptions:
            # Simple keyword matching for misconceptions
            misconception_keywords = misconception.lower().split()
            if any(keyword in text_lower for keyword in misconception_keywords if len(keyword) > 3):
                misconceptions_found.append(misconception)
                severity += 0.3
        
        # Check for uncertainty indicators
        uncertainty_count = sum(1 for indicator in self.uncertainty_indicators if indicator in text_lower)
        if uncertainty_count > 2:
            severity += 0.2
            misconceptions_found.append("high_uncertainty")
        
        return {
            'severity': min(severity, 1.0),
            'misconceptions_found': misconceptions_found,
            'uncertainty_level': uncertainty_count
        }
    
    def _analyze_completeness(self, text: str, concept_def, structure_analysis: Dict) -> Dict[str, any]:
        """
        Analyze how complete the explanation is
        """
        completeness_score = 0.0
        missing_aspects = []
        
        # Check for definition
        if structure_analysis['has_definition']:
            completeness_score += 0.3
        else:
            missing_aspects.append("definition")
        
        # Check for examples
        if structure_analysis['has_examples']:
            completeness_score += 0.2
        else:
            missing_aspects.append("examples")
        
        # Check for process description
        if structure_analysis['has_process_description']:
            completeness_score += 0.2
        else:
            missing_aspects.append("process_description")
        
        # Check for comparisons
        if structure_analysis['has_comparisons']:
            completeness_score += 0.1
        else:
            missing_aspects.append("comparisons")
        
        # Check length adequacy
        if structure_analysis['word_count'] >= 50:
            completeness_score += 0.2
        else:
            missing_aspects.append("sufficient_detail")
        
        return {
            'score': completeness_score,
            'missing_aspects': missing_aspects,
            'word_count': structure_analysis['word_count'],
            'sentence_count': structure_analysis['sentence_count']
        }
    
    def _calculate_confidence(self, text: str, understanding_quality: Dict, misconception_analysis: Dict) -> float:
        """
        Calculate confidence in the analysis
        """
        base_confidence = 0.7
        
        # Increase confidence with quality indicators
        if understanding_quality['has_causal_reasoning']:
            base_confidence += 0.1
        if understanding_quality['has_examples']:
            base_confidence += 0.1
        
        # Decrease confidence with misconceptions
        base_confidence -= misconception_analysis['severity'] * 0.3
        
        # Decrease confidence with high uncertainty
        if misconception_analysis['uncertainty_level'] > 1:
            base_confidence -= 0.2
        
        return max(0.1, min(1.0, base_confidence))
    
    def _create_default_analysis(self, concept_name: str) -> Dict[str, any]:
        """
        Create a default analysis when concept is not in knowledge base
        """
        return {
            'concept_name': concept_name,
            'coverage_score': 0.5,
            'correctness_score': 0.5,
            'confidence_score': 0.3,
            'term_coverage': {'score': 0.5, 'matched_terms': [], 'missing_terms': [], 'total_key_terms': 0},
            'understanding_quality': {'score': 0.5, 'indicators_found': [], 'has_causal_reasoning': False, 'has_examples': False},
            'misconceptions': {'severity': 0.0, 'misconceptions_found': [], 'uncertainty_level': 0},
            'completeness': {'score': 0.5, 'missing_aspects': [], 'word_count': 0, 'sentence_count': 0},
            'structure_analysis': {}
        }
    
    def identify_related_concepts(self, text: str, subject: str) -> List[Tuple[str, float]]:
        """
        Identify related concepts mentioned or implied in the text
        """
        from app.knowledge.cs_concepts import get_concepts_by_subject
        
        subject_concepts = get_concepts_by_subject(subject)
        mentioned_concepts = self.preprocessor.extract_concept_mentions(text, subject_concepts)
        
        concept_scores = []
        for concept in mentioned_concepts:
            concept_def = get_concept_by_name(concept)
            if concept_def:
                # Calculate relevance score based on term matches
                key_terms = self.preprocessor.extract_key_terms(text)
                term_matches = sum(1 for term in concept_def.key_terms if term.lower() in [t.lower() for t in key_terms])
                relevance_score = term_matches / len(concept_def.key_terms) if concept_def.key_terms else 0
                concept_scores.append((concept, relevance_score))
        
        # Sort by relevance score
        concept_scores.sort(key=lambda x: x[1], reverse=True)
        return concept_scores[:5]  # Return top 5 related concepts