"""
Sentence embeddings module
Handles semantic representation of text using sentence-transformers
"""

import numpy as np
from typing import List, Dict, Any
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    Handles sentence embeddings and semantic similarity
    """
    
    def __init__(self):
        # Initialize sentence transformer model when available
        self.model = None
        self.fallback_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.use_transformers = False
        
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.use_transformers = True
            logger.info("Loaded sentence-transformers model successfully")
        except ImportError:
            logger.warning("sentence-transformers not available - using TF-IDF fallback")
        except Exception as e:
            logger.warning(f"Failed to load sentence-transformers: {e} - using TF-IDF fallback")
    
    def encode_text(self, text: str) -> np.ndarray:
        """
        Convert text to dense vector representation
        """
        if self.use_transformers and self.model:
            try:
                return self.model.encode([text])[0]
            except Exception as e:
                logger.warning(f"Transformer encoding failed: {e}, falling back to TF-IDF")
                self.use_transformers = False
        
        # Fallback to TF-IDF
        try:
            # Fit and transform on single text (not ideal but functional)
            tfidf_matrix = self.fallback_vectorizer.fit_transform([text])
            return tfidf_matrix.toarray()[0]
        except Exception as e:
            logger.error(f"TF-IDF encoding failed: {e}")
            # Return zero vector as last resort
            return np.zeros(100)
    
    def encode_sentences(self, sentences: List[str]) -> np.ndarray:
        """
        Encode multiple sentences into embeddings
        """
        if not sentences:
            return np.array([])
        
        if self.use_transformers and self.model:
            try:
                return self.model.encode(sentences)
            except Exception as e:
                logger.warning(f"Transformer encoding failed: {e}, falling back to TF-IDF")
                self.use_transformers = False
        
        # Fallback to TF-IDF
        try:
            tfidf_matrix = self.fallback_vectorizer.fit_transform(sentences)
            return tfidf_matrix.toarray()
        except Exception as e:
            logger.error(f"TF-IDF encoding failed: {e}")
            # Return zero vectors as last resort
            return np.zeros((len(sentences), 100))
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        Compute semantic similarity between two texts
        """
        if not text1.strip() or not text2.strip():
            return 0.0
        
        try:
            if self.use_transformers and self.model:
                embeddings = self.model.encode([text1, text2])
                similarity = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
                return float(similarity)
            else:
                # Use TF-IDF similarity
                tfidf_matrix = self.fallback_vectorizer.fit_transform([text1, text2])
                similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
                return float(similarity)
        except Exception as e:
            logger.error(f"Similarity computation failed: {e}")
            # Simple word overlap as last resort
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            if not words1 or not words2:
                return 0.0
            intersection = len(words1.intersection(words2))
            union = len(words1.union(words2))
            return intersection / union if union > 0 else 0.0
    
    def find_similar_concepts(self, text: str, concept_embeddings: Dict[str, np.ndarray]) -> List[Dict[str, Any]]:
        """
        Find concepts most similar to the given text
        """
        if not concept_embeddings:
            return []
        
        try:
            text_embedding = self.encode_text(text)
            similarities = []
            
            for concept_name, concept_embedding in concept_embeddings.items():
                if concept_embedding.size > 0 and text_embedding.size > 0:
                    # Ensure embeddings have same dimensionality
                    if text_embedding.shape != concept_embedding.shape:
                        continue
                    
                    similarity = cosine_similarity([text_embedding], [concept_embedding])[0][0]
                    similarities.append({
                        'concept': concept_name,
                        'similarity': float(similarity)
                    })
            
            # Sort by similarity score
            similarities.sort(key=lambda x: x['similarity'], reverse=True)
            return similarities[:5]  # Return top 5
            
        except Exception as e:
            logger.error(f"Concept similarity search failed: {e}")
            return []
    
    def create_concept_embeddings(self, concepts: Dict[str, str]) -> Dict[str, np.ndarray]:
        """
        Create embeddings for a dictionary of concepts
        """
        concept_embeddings = {}
        
        for concept_name, concept_text in concepts.items():
            try:
                embedding = self.encode_text(concept_text)
                concept_embeddings[concept_name] = embedding
            except Exception as e:
                logger.error(f"Failed to create embedding for {concept_name}: {e}")
                concept_embeddings[concept_name] = np.array([])
        
        return concept_embeddings
    
    def batch_similarity(self, query_text: str, candidate_texts: List[str]) -> List[float]:
        """
        Compute similarity between query text and multiple candidate texts
        """
        if not candidate_texts:
            return []
        
        similarities = []
        for candidate in candidate_texts:
            similarity = self.compute_similarity(query_text, candidate)
            similarities.append(similarity)
        
        return similarities