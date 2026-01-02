"""
FastAPI application entry point for Explain My Confusion
Educational diagnostic app for analyzing student explanations
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import analyze
from app.core.config import settings

app = FastAPI(
    title="Explain My Confusion API",
    description="NLP-based educational diagnostic system",
    version="1.0.0"
)

# CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(analyze.router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "Explain My Confusion API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}