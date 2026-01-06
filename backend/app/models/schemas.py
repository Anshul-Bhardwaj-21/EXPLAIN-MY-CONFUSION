"""
Pydantic models for real analysis system
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class AnalysisRequest(BaseModel):
    """Request model for explanation analysis"""
    explanation: str = Field(..., description="Student's textual explanation", min_length=10, max_length=5000)
    topic: str = Field(..., description="Topic to analyze", min_length=2, max_length=100)
    subject: Optional[str] = Field(None, description="Subject area (optional)", max_length=50)

class StudentAnalysis(BaseModel):
    """Analysis of student's input"""
    word_count: int
    sentence_count: int
    key_terms: List[str]
    complexity: float

class ReferenceInfo(BaseModel):
    """Information about the reference source"""
    source: str
    title: str
    url: str
    summary_preview: str

class ConceptAnalysis(BaseModel):
    """Results of concept comparison"""
    correct_concepts: List[str]
    missing_concepts: List[str]
    extra_concepts: List[str]
    similarity_score: float
    reference_source: str
    reference_title: str

class Explanations(BaseModel):
    """Generated explanations"""
    what_you_got_right: str
    what_you_missed: str
    where_confusion_is: str
    learning_suggestions: str

class RealAnalysisResponse(BaseModel):
    """Real analysis response using Wikipedia knowledge"""
    success: bool
    topic: str
    subject: Optional[str]
    student_analysis: StudentAnalysis
    reference_info: ReferenceInfo
    concept_analysis: ConceptAnalysis
    explanations: Explanations
    learning_suggestions: List[str]

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    features_available: List[str]