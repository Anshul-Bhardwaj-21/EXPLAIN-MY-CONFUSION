"""
FastAPI application for real NLP-based educational diagnostic system
Uses Wikipedia knowledge base for concept comparison
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

from app.api.routes import analyze
from app.models.schemas import HealthResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Explain My Confusion - Real NLP Analysis",
    description="Real NLP-based educational diagnostic system using Wikipedia knowledge",
    version="2.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(analyze.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Explain My Confusion - Real NLP Analysis API",
        "version": "2.0.0",
        "features": [
            "Real Wikipedia knowledge retrieval",
            "NLP preprocessing with spaCy/NLTK", 
            "Concept extraction and comparison",
            "Semantic similarity analysis",
            "Fact-grounded explanations"
        ]
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check with feature availability"""
    
    # Check if key components are available
    features_available = []
    
    try:
        from app.knowledge.wikipedia_kb import WikipediaKnowledgeBase
        kb = WikipediaKnowledgeBase()
        features_available.append("Wikipedia Knowledge Base")
    except Exception:
        pass
    
    try:
        from app.nlp.preprocess import RealNLPProcessor
        nlp = RealNLPProcessor()
        features_available.append("NLP Processing")
    except Exception:
        pass
    
    try:
        import wikipedia
        features_available.append("Wikipedia API")
    except Exception:
        pass
    
    try:
        from sentence_transformers import SentenceTransformer
        features_available.append("Sentence Embeddings")
    except Exception:
        pass
    
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        features_available=features_available
    )