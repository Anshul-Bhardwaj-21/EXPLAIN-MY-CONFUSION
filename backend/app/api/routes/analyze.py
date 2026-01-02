"""
API routes for analyzing student explanations
Handles text input and returns diagnostic results
"""

from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any

from app.models.schemas import AnalysisRequest, AnalysisResponse
from app.api.deps import get_analysis_service

router = APIRouter(tags=["analysis"])

@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_explanation(
    request: AnalysisRequest,
    analysis_service=Depends(get_analysis_service)
) -> AnalysisResponse:
    """
    Analyze student's textual explanation of a CS concept
    Returns classification of understood/misunderstood/missing concepts
    """
    try:
        # Analysis service will orchestrate NLP processing and evaluation
        result = await analysis_service.analyze_text(
            text=request.explanation,
            subject=request.subject,
            topic=request.topic
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))