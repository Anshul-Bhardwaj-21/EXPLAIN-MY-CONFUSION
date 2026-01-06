"""
API routes for analyzing student explanations using real Wikipedia knowledge
"""

from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
import logging

from app.models.schemas import AnalysisRequest, RealAnalysisResponse
from app.analysis.concept_engine import ConceptComparisonEngine

logger = logging.getLogger(__name__)
router = APIRouter(tags=["analysis"])

# Global engine instance
analysis_engine = ConceptComparisonEngine()

@router.post("/analyze", response_model=RealAnalysisResponse)
async def analyze_explanation(request: AnalysisRequest) -> RealAnalysisResponse:
    """
    Analyze student's explanation using real Wikipedia knowledge
    """
    try:
        logger.info(f"Received analysis request for topic: {request.topic}")
        
        # Validate input
        if not request.explanation.strip():
            raise HTTPException(status_code=400, detail="Explanation cannot be empty")
        
        if len(request.explanation) > 5000:
            raise HTTPException(status_code=400, detail="Explanation too long (max 5000 characters)")
        
        # Run real analysis
        result = analysis_engine.analyze_explanation(
            student_text=request.explanation,
            topic=request.topic,
            subject=request.subject
        )
        
        if not result.get('success'):
            raise HTTPException(
                status_code=422, 
                detail=result.get('error', 'Analysis failed')
            )
        
        # Convert to response format
        response = RealAnalysisResponse(
            success=True,
            topic=result['topic'],
            subject=result['subject'],
            student_analysis=result['student_analysis'],
            reference_info=result['reference_info'],
            concept_analysis=result['concept_analysis'],
            explanations=result['explanations'],
            learning_suggestions=result['learning_suggestions']
        )
        
        logger.info("Analysis completed successfully")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in analysis: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error during analysis")

@router.get("/topic-overview/{topic}")
async def get_topic_overview(topic: str) -> Dict[str, Any]:
    """
    Get a quick overview of a topic from Wikipedia
    """
    try:
        overview = analysis_engine.get_topic_overview(topic)
        return overview
    except Exception as e:
        logger.error(f"Error getting topic overview: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve topic overview")