"""
Real Wikipedia Knowledge Base
Retrieves actual content from Wikipedia for concept comparison
"""

import wikipedia
import requests
from typing import List, Dict, Optional, Tuple
import logging
from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
import os

logger = logging.getLogger(__name__)

class WikipediaKnowledgeBase:
    """
    Real knowledge base using Wikipedia content
    """
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.cache_dir = "app/knowledge/cache"
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Set Wikipedia language
        wikipedia.set_lang("en")
    
    def search_topics(self, query: str, max_results: int = 5) -> List[str]:
        """
        Search Wikipedia for topics related to the query
        """
        try:
            results = wikipedia.search(query, results=max_results)
            return results
        except Exception as e:
            logger.error(f"Wikipedia search failed: {e}")
            return []
    
    def get_page_content(self, title: str) -> Optional[Dict[str, str]]:
        """
        Get full Wikipedia page content
        """
        cache_file = os.path.join(self.cache_dir, f"{title.replace(' ', '_')}.json")
        
        # Check cache first
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception:
                pass
        
        try:
            page = wikipedia.page(title)
            content = {
                'title': page.title,
                'summary': page.summary,
                'content': page.content,
                'url': page.url,
                'sections': self._extract_sections(page.content)
            }
            
            # Cache the content
            try:
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(content, f, indent=2, ensure_ascii=False)
            except Exception as e:
                logger.warning(f"Failed to cache content: {e}")
            
            return content
            
        except wikipedia.exceptions.DisambiguationError as e:
            # Try the first option
            if e.options:
                return self.get_page_content(e.options[0])
            return None
        except wikipedia.exceptions.PageError:
            logger.warning(f"Page not found: {title}")
            return None
        except Exception as e:
            logger.error(f"Error fetching page {title}: {e}")
            return None
    
    def _extract_sections(self, content: str) -> Dict[str, str]:
        """
        Extract sections from Wikipedia content
        """
        sections = {}
        current_section = "Introduction"
        current_content = []
        
        lines = content.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('==') and line.endswith('=='):
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                
                # Start new section
                current_section = line.strip('= ')
                current_content = []
            else:
                if line:
                    current_content.append(line)
        
        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()
        
        return sections
    
    def get_relevant_content(self, topic: str, subject: str = None) -> Dict[str, any]:
        """
        Get relevant Wikipedia content for a topic
        """
        # Search for the topic
        search_results = self.search_topics(topic)
        
        if not search_results:
            return {
                'found': False,
                'message': f"No Wikipedia articles found for '{topic}'"
            }
        
        # Get the most relevant page
        main_page = self.get_page_content(search_results[0])
        
        if not main_page:
            return {
                'found': False,
                'message': f"Could not retrieve Wikipedia page for '{topic}'"
            }
        
        # Get related pages if subject is specified
        related_pages = []
        if subject:
            subject_search = self.search_topics(f"{topic} {subject}", max_results=3)
            for result in subject_search[1:]:  # Skip first as it's likely the main page
                page = self.get_page_content(result)
                if page:
                    related_pages.append(page)
        
        return {
            'found': True,
            'main_page': main_page,
            'related_pages': related_pages,
            'source': 'Wikipedia',
            'search_query': topic
        }
    
    def extract_key_concepts(self, text: str) -> List[str]:
        """
        Extract key concepts from text using simple NLP
        """
        import nltk
        from nltk.tokenize import word_tokenize, sent_tokenize
        from nltk.tag import pos_tag
        from nltk.corpus import stopwords
        
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        # Tokenize and get POS tags
        tokens = word_tokenize(text.lower())
        pos_tags = pos_tag(tokens)
        
        # Extract nouns and noun phrases
        stop_words = set(stopwords.words('english'))
        concepts = []
        
        for word, pos in pos_tags:
            if (pos.startswith('NN') and  # Nouns
                word not in stop_words and 
                len(word) > 2 and
                word.isalpha()):
                concepts.append(word)
        
        # Remove duplicates and return most frequent
        concept_counts = {}
        for concept in concepts:
            concept_counts[concept] = concept_counts.get(concept, 0) + 1
        
        # Sort by frequency and return top concepts
        sorted_concepts = sorted(concept_counts.items(), key=lambda x: x[1], reverse=True)
        return [concept for concept, count in sorted_concepts[:20]]
    
    def compare_concepts(self, student_text: str, reference_content: Dict) -> Dict[str, any]:
        """
        Compare student concepts with Wikipedia reference content
        """
        if not reference_content.get('found'):
            return {
                'error': 'No reference content available',
                'comparison': None
            }
        
        # Extract concepts from student text
        student_concepts = self.extract_key_concepts(student_text)
        
        # Extract concepts from reference content
        main_page = reference_content['main_page']
        reference_text = main_page['summary'] + '\n' + main_page['content'][:2000]  # Limit for processing
        reference_concepts = self.extract_key_concepts(reference_text)
        
        # Find overlapping concepts
        student_set = set(student_concepts)
        reference_set = set(reference_concepts)
        
        correct_concepts = list(student_set.intersection(reference_set))
        missing_concepts = list(reference_set - student_set)
        extra_concepts = list(student_set - reference_set)
        
        # Calculate semantic similarity using embeddings
        if student_text.strip() and main_page['summary'].strip():
            student_embedding = self.model.encode([student_text])
            reference_embedding = self.model.encode([main_page['summary']])
            similarity_score = cosine_similarity(student_embedding, reference_embedding)[0][0]
        else:
            similarity_score = 0.0
        
        return {
            'comparison': {
                'correct_concepts': correct_concepts[:10],  # Limit for display
                'missing_concepts': missing_concepts[:10],
                'extra_concepts': extra_concepts[:10],
                'similarity_score': float(similarity_score),
                'reference_source': main_page['url'],
                'reference_title': main_page['title']
            }
        }
    
    def generate_explanation(self, comparison_result: Dict, student_text: str) -> Dict[str, str]:
        """
        Generate explanation based on comparison with Wikipedia content
        """
        if 'error' in comparison_result:
            return {
                'what_you_got_right': "Unable to analyze - no reference content available",
                'what_you_missed': "Please try a different topic",
                'where_confusion_is': "No analysis possible",
                'learning_suggestions': "Try searching for a more specific topic"
            }
        
        comp = comparison_result['comparison']
        
        # What you got right
        if comp['correct_concepts']:
            right_text = f"You correctly mentioned these key concepts: {', '.join(comp['correct_concepts'][:5])}. "
            right_text += f"Your explanation has {comp['similarity_score']:.1%} similarity to the Wikipedia reference."
        else:
            right_text = "Your explanation shows basic understanding, but didn't match key technical concepts from the reference material."
        
        # What you missed
        if comp['missing_concepts']:
            missed_text = f"Important concepts not mentioned: {', '.join(comp['missing_concepts'][:5])}. "
            missed_text += "These are key terms that appear in the Wikipedia article on this topic."
        else:
            missed_text = "You covered most of the important concepts mentioned in the reference material."
        
        # Where confusion might be
        if comp['extra_concepts']:
            confusion_text = f"You mentioned some concepts that aren't central to this topic: {', '.join(comp['extra_concepts'][:3])}. "
            confusion_text += "These might be related but aren't the main focus according to Wikipedia."
        else:
            confusion_text = "No major conceptual confusion detected in your explanation."
        
        # Learning suggestions
        suggestions = f"Study the Wikipedia article: {comp['reference_title']} ({comp['reference_source']}). "
        if comp['missing_concepts']:
            suggestions += f"Focus on understanding: {', '.join(comp['missing_concepts'][:3])}."
        
        return {
            'what_you_got_right': right_text,
            'what_you_missed': missed_text,
            'where_confusion_is': confusion_text,
            'learning_suggestions': suggestions
        }