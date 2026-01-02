"""
Shared dependencies for API routes
Handles dependency injection for services with real NLP analysis
"""

from typing import Generator
from functools import lru_cache

from app.nlp.preprocess import TextPreprocessor
from app.nlp.concept_analyzer import ConceptAnalyzer
from app.knowledge.cs_concepts import get_concept_by_name, get_concepts_by_subject, find_related_concepts

class AnalysisService:
    """
    Main service that orchestrates the real NLP analysis pipeline
    """
    def __init__(self):
        # Initialize all components
        self.preprocessor = TextPreprocessor()
        self.concept_analyzer = ConceptAnalyzer()
    
    async def analyze_text(self, text: str, subject: str, topic: str):
        """
        Main analysis pipeline using real NLP and concept analysis
        """
        from app.models.schemas import AnalysisResponse, ConceptStatus
        import asyncio
        
        # Simulate processing time for realistic experience
        await asyncio.sleep(2)
        
        # Preprocess the text
        key_terms = self.preprocessor.extract_key_terms(text)
        technical_phrases = self.preprocessor.extract_technical_phrases(text)
        structure_analysis = self.preprocessor.analyze_explanation_structure(text)
        
        # Analyze the main concept
        main_concept_analysis = self.concept_analyzer.analyze_concept_understanding(text, topic, subject)
        
        # Identify related concepts mentioned in the text
        related_concepts = self.concept_analyzer.identify_related_concepts(text, subject)
        
        # Get all concepts for this subject to identify missing ones
        subject_concepts = get_concepts_by_subject(subject)
        
        # Categorize concepts
        understood_concepts = []
        misunderstood_concepts = []
        missing_concepts = []
        
        # Analyze main concept
        if main_concept_analysis['correctness_score'] >= 0.7 and main_concept_analysis['coverage_score'] >= 0.6:
            understood_concepts.append(ConceptStatus(
                name=main_concept_analysis['concept_name'],
                status="understood",
                confidence=main_concept_analysis['confidence_score'],
                details=self._generate_understanding_feedback(main_concept_analysis)
            ))
        elif main_concept_analysis['misconceptions']['severity'] > 0.3:
            misunderstood_concepts.append(ConceptStatus(
                name=main_concept_analysis['concept_name'],
                status="misunderstood",
                confidence=main_concept_analysis['confidence_score'],
                details=self._generate_misconception_feedback(main_concept_analysis)
            ))
        else:
            missing_concepts.append(ConceptStatus(
                name=main_concept_analysis['concept_name'],
                status="missing",
                confidence=main_concept_analysis['confidence_score'],
                details=self._generate_missing_feedback(main_concept_analysis)
            ))
        
        # Analyze related concepts
        for concept_name, relevance_score in related_concepts:
            if relevance_score >= 0.5:
                concept_analysis = self.concept_analyzer.analyze_concept_understanding(text, concept_name, subject)
                
                if concept_analysis['correctness_score'] >= 0.6:
                    understood_concepts.append(ConceptStatus(
                        name=concept_analysis['concept_name'],
                        status="understood",
                        confidence=concept_analysis['confidence_score'] * relevance_score,
                        details=f"Good understanding shown through related discussion"
                    ))
        
        # Identify missing prerequisite concepts
        main_concept_def = get_concept_by_name(topic)
        if main_concept_def:
            for prereq in main_concept_def.prerequisites:
                prereq_mentioned = any(prereq.lower().replace('_', ' ') in text.lower() for prereq in main_concept_def.prerequisites)
                if not prereq_mentioned and len(missing_concepts) < 3:
                    prereq_def = get_concept_by_name(prereq)
                    if prereq_def:
                        missing_concepts.append(ConceptStatus(
                            name=prereq_def.name,
                            status="missing",
                            confidence=0.7,
                            details=f"This is a prerequisite for understanding {main_concept_def.name}"
                        ))
        
        # Calculate overall scores
        total_concepts = len(understood_concepts) + len(misunderstood_concepts) + len(missing_concepts)
        coverage_score = len(understood_concepts) / max(total_concepts, 1) if total_concepts > 0 else main_concept_analysis['coverage_score']
        correctness_score = main_concept_analysis['correctness_score']
        overall_score = (coverage_score + correctness_score) / 2
        
        # Generate personalized feedback
        feedback = self._generate_personalized_feedback(
            main_concept_analysis, understood_concepts, misunderstood_concepts, missing_concepts, structure_analysis
        )
        
        # Generate suggestions
        suggestions = self._generate_learning_suggestions(
            main_concept_analysis, missing_concepts, subject, topic
        )
        
        return AnalysisResponse(
            concepts_understood=understood_concepts,
            concepts_misunderstood=misunderstood_concepts,
            concepts_missing=missing_concepts,
            overall_score=overall_score,
            coverage_score=coverage_score,
            correctness_score=correctness_score,
            feedback=feedback,
            suggestions=suggestions
        )
    
    def _generate_understanding_feedback(self, analysis: dict) -> str:
        """Generate feedback for well-understood concepts"""
        feedback_parts = []
        
        if analysis['understanding_quality']['has_causal_reasoning']:
            feedback_parts.append("You demonstrate good causal reasoning")
        
        if analysis['understanding_quality']['has_examples']:
            feedback_parts.append("Your use of examples shows practical understanding")
        
        if analysis['term_coverage']['score'] > 0.7:
            feedback_parts.append("You use appropriate technical terminology")
        
        return ". ".join(feedback_parts) if feedback_parts else "Good basic understanding demonstrated"
    
    def _generate_misconception_feedback(self, analysis: dict) -> str:
        """Generate feedback for misconceptions"""
        misconceptions = analysis['misconceptions']['misconceptions_found']
        if misconceptions:
            return f"Review the concept carefully - some statements suggest misconceptions about {', '.join(misconceptions[:2])}"
        return "Some aspects of your explanation suggest areas that need clarification"
    
    def _generate_missing_feedback(self, analysis: dict) -> str:
        """Generate feedback for missing concepts"""
        missing_aspects = analysis['completeness']['missing_aspects']
        if 'definition' in missing_aspects:
            return "Try to include a clear definition of the concept"
        elif 'examples' in missing_aspects:
            return "Adding concrete examples would strengthen your explanation"
        elif 'process_description' in missing_aspects:
            return "Describe how the concept works step-by-step"
        return "Your explanation could be more detailed and comprehensive"
    
    def _generate_personalized_feedback(self, main_analysis, understood, misunderstood, missing, structure):
        """Generate comprehensive personalized feedback"""
        feedback_parts = []
        
        # Overall assessment
        if main_analysis['correctness_score'] >= 0.8:
            feedback_parts.append("Excellent understanding! You demonstrate strong grasp of the core concepts.")
        elif main_analysis['correctness_score'] >= 0.6:
            feedback_parts.append("Good understanding with room for improvement in some areas.")
        else:
            feedback_parts.append("Your explanation shows some understanding, but several key areas need attention.")
        
        # Structure feedback
        if structure['word_count'] < 30:
            feedback_parts.append("Try to provide more detailed explanations to better demonstrate your understanding.")
        elif structure['word_count'] > 200:
            feedback_parts.append("Great detail! Make sure all information is relevant and accurate.")
        
        # Specific strengths
        if len(understood) > 1:
            feedback_parts.append(f"You show solid understanding of {len(understood)} key concepts.")
        
        # Areas for improvement
        if len(misunderstood) > 0:
            feedback_parts.append(f"Focus on clarifying {len(misunderstood)} concept(s) that show some confusion.")
        
        if len(missing) > 0:
            feedback_parts.append(f"Consider exploring {len(missing)} additional concept(s) to deepen your understanding.")
        
        return " ".join(feedback_parts)
    
    def _generate_learning_suggestions(self, main_analysis, missing_concepts, subject, topic):
        """Generate specific learning suggestions"""
        suggestions = []
        
        # Based on completeness analysis
        missing_aspects = main_analysis['completeness']['missing_aspects']
        if 'definition' in missing_aspects:
            suggestions.append(f"Start by clearly defining what {topic} means and its key characteristics")
        
        if 'examples' in missing_aspects:
            suggestions.append(f"Practice with concrete examples of {topic} to solidify your understanding")
        
        if 'process_description' in missing_aspects:
            suggestions.append(f"Study the step-by-step process of how {topic} works")
        
        # Based on missing concepts
        if missing_concepts:
            first_missing = missing_concepts[0].name
            suggestions.append(f"Review {first_missing} as it's fundamental to understanding {topic}")
        
        # Subject-specific suggestions
        if subject == "algorithms":
            suggestions.append("Practice implementing the algorithm and analyzing its time complexity")
        elif subject == "data_structures":
            suggestions.append("Draw diagrams and trace through operations to visualize the structure")
        elif subject == "operating_systems":
            suggestions.append("Study real-world examples and system implementations")
        
        # General suggestions
        suggestions.append(f"Connect {topic} to other {subject.replace('_', ' ')} concepts you know")
        
        return suggestions[:4]  # Limit to 4 suggestions

@lru_cache()
def get_analysis_service() -> AnalysisService:
    """
    Dependency injection for analysis service
    """
    return AnalysisService()