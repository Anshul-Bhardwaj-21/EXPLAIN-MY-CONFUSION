"""
Real Concept Comparison Engine
Compares student explanations with Wikipedia knowledge
"""

from typing import Dict, List, Any, Optional
import logging
from app.knowledge.wikipedia_kb import WikipediaKnowledgeBase
from app.nlp.preprocess import RealNLPProcessor

logger = logging.getLogger(__name__)

class ConceptComparisonEngine:
    """
    Real engine that compares student concepts with Wikipedia knowledge
    """
    
    def __init__(self):
        self.kb = WikipediaKnowledgeBase()
        self.nlp = RealNLPProcessor()
    
    def analyze_explanation(self, student_text: str, topic: str, subject: str = None) -> Dict[str, Any]:
        """
        Complete analysis pipeline using real Wikipedia data
        """
        try:
            # Step 1: Preprocess student input
            logger.info(f"Processing student explanation for topic: {topic}")
            student_analysis = self.nlp.preprocess_for_comparison(student_text)
            
            # Step 2: Retrieve reference knowledge from Wikipedia
            logger.info(f"Retrieving Wikipedia content for: {topic}")
            reference_content = self.kb.get_relevant_content(topic, subject)
            
            if not reference_content.get('found'):
                return {
                    'success': False,
                    'error': reference_content.get('message', 'Could not retrieve reference content'),
                    'topic': topic,
                    'subject': subject
                }
            
            # Step 3: Compare concepts
            logger.info("Comparing student concepts with Wikipedia reference")
            comparison = self.kb.compare_concepts(student_text, reference_content)
            
            if 'error' in comparison:
                return {
                    'success': False,
                    'error': comparison['error'],
                    'topic': topic,
                    'subject': subject
                }
            
            # Step 4: Generate explanations
            logger.info("Generating feedback based on comparison")
            explanations = self.kb.generate_explanation(comparison, student_text)
            
            # Step 5: Compile final result
            result = {
                'success': True,
                'topic': topic,
                'subject': subject,
                'student_analysis': {
                    'word_count': student_analysis['structure']['word_count'],
                    'sentence_count': student_analysis['structure']['sentence_count'],
                    'key_terms': student_analysis['key_terms'][:10],  # Limit for display
                    'complexity': student_analysis['structure']['complexity_ratio']
                },
                'reference_info': {
                    'source': 'Wikipedia',
                    'title': reference_content['main_page']['title'],
                    'url': reference_content['main_page']['url'],
                    'summary_preview': reference_content['main_page']['summary'][:200] + "..."
                },
                'concept_analysis': comparison['comparison'],
                'explanations': explanations,
                'learning_suggestions': self._generate_learning_suggestions(
                    comparison['comparison'], 
                    reference_content
                )
            }
            
            logger.info("Analysis completed successfully")
            return result
            
        except Exception as e:
            logger.error(f"Analysis failed: {str(e)}")
            return {
                'success': False,
                'error': f"Analysis failed: {str(e)}",
                'topic': topic,
                'subject': subject
            }
    
    def _generate_learning_suggestions(self, comparison: Dict, reference_content: Dict) -> List[str]:
        """
        Generate specific learning suggestions based on the analysis
        """
        suggestions = []
        
        # Based on missing concepts
        if comparison.get('missing_concepts'):
            missing = comparison['missing_concepts'][:3]  # Top 3
            suggestions.append(f"Study these key concepts: {', '.join(missing)}")
        
        # Based on similarity score
        similarity = comparison.get('similarity_score', 0)
        if similarity < 0.3:
            suggestions.append("Your explanation differs significantly from the reference. Review the basic concepts.")
        elif similarity < 0.6:
            suggestions.append("Good start! Try to include more technical details to improve accuracy.")
        else:
            suggestions.append("Excellent understanding! Consider exploring advanced aspects of this topic.")
        
        # Wikipedia-specific suggestions
        main_page = reference_content.get('main_page', {})
        if main_page:
            suggestions.append(f"Read the full Wikipedia article: {main_page.get('title', 'Unknown')}")
            
            # Suggest specific sections if available
            sections = main_page.get('sections', {})
            interesting_sections = [s for s in sections.keys() 
                                  if any(keyword in s.lower() for keyword in 
                                        ['example', 'application', 'implementation', 'algorithm'])]
            if interesting_sections:
                suggestions.append(f"Focus on these sections: {', '.join(interesting_sections[:2])}")
        
        # Related topics
        related_pages = reference_content.get('related_pages', [])
        if related_pages:
            related_titles = [page['title'] for page in related_pages[:2]]
            suggestions.append(f"Explore related topics: {', '.join(related_titles)}")
        
        return suggestions[:5]  # Limit to 5 suggestions
    
    def get_topic_overview(self, topic: str) -> Dict[str, Any]:
        """
        Get a quick overview of a topic from Wikipedia
        """
        try:
            reference_content = self.kb.get_relevant_content(topic)
            
            if not reference_content.get('found'):
                return {
                    'found': False,
                    'message': f"No information found for '{topic}'"
                }
            
            main_page = reference_content['main_page']
            
            return {
                'found': True,
                'title': main_page['title'],
                'summary': main_page['summary'],
                'url': main_page['url'],
                'key_concepts': self.kb.extract_key_concepts(main_page['summary'])[:10],
                'sections': list(main_page.get('sections', {}).keys())[:5]
            }
            
        except Exception as e:
            logger.error(f"Failed to get topic overview: {str(e)}")
            return {
                'found': False,
                'message': f"Error retrieving information: {str(e)}"
            }