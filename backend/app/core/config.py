"""
Application configuration settings
Manages environment variables and app settings
"""

from pydantic import BaseModel
from typing import List

class Settings(BaseModel):
    """
    Application settings loaded from environment variables
    """
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Explain My Confusion"
    VERSION: str = "1.0.0"
    
    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # NLP Model Settings
    SPACY_MODEL: str = "en_core_web_sm"
    SENTENCE_TRANSFORMER_MODEL: str = "all-MiniLM-L6-v2"
    
    # Logging Settings
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Analysis Settings
    MIN_CONFIDENCE_THRESHOLD: float = 0.5
    MAX_TEXT_LENGTH: int = 5000

settings = Settings()