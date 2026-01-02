"""
Pydantic models for request/response schemas
Defines data structures for API communication
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from enum import Enum

class Subject(str, Enum):
    """Supported CS subjects"""
    DATA_STRUCTURES = "data_structures"
    ALGORITHMS = "algorithms"
    OPERATING_SYSTEMS = "operating_systems"
    DATABASES = "databases"
    COMPUTER_NETWORKS = "computer_networks"
    SOFTWARE_ENGINEERING = "software_engineering"

class AnalysisRequest(BaseModel):
    """Request model for explanation analysis"""
    explanation: str = Field(..., description="Student's textual explanation")
    subject: Subject = Field(..., description="CS subject area")
    topic: str = Field(..., description="Specific topic within the subject")

class ConceptStatus(BaseModel):
    """Status of a single concept"""
    name: str
    status: str  # "understood", "misunderstood", "missing"
    confidence: float = Field(..., ge=0.0, le=1.0)
    details: Optional[str] = None

class AnalysisResponse(BaseModel):
    """Response model for explanation analysis"""
    concepts_understood: List[ConceptStatus]
    concepts_misunderstood: List[ConceptStatus]
    concepts_missing: List[ConceptStatus]
    overall_score: float = Field(..., ge=0.0, le=1.0)
    coverage_score: float = Field(..., ge=0.0, le=1.0)
    correctness_score: float = Field(..., ge=0.0, le=1.0)
    feedback: str
    suggestions: List[str]

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str