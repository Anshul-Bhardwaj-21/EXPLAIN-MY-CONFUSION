# Explain My Confusion - Backend

NLP-based educational diagnostic system that analyzes student explanations of CS concepts.

## Architecture

The backend follows a clean, modular architecture with separated concerns:

- **API Layer** (`app/api/`): FastAPI routes and dependencies
- **NLP Processing** (`app/nlp/`): Text preprocessing, embeddings, dependency parsing
- **Concept Management** (`app/concepts/`): Concept graphs and syllabus management
- **Evaluation Logic** (`app/evaluation/`): Coverage and correctness assessment
- **Data Models** (`app/models/`): Pydantic schemas for API communication
- **Core** (`app/core/`): Configuration and logging
- **Utils** (`app/utils/`): Shared utility functions

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Download spaCy model:
```bash
python -m spacy download en_core_web_sm
```

3. Run the application:
```bash
uvicorn app.main:app --reload
```

## API Endpoints

- `POST /api/v1/analyze` - Analyze student explanation
- `GET /health` - Health check

## Development

The project structure is designed for scalability and maintainability. Each module has a specific responsibility and can be developed independently.

Implementation of business logic will be added incrementally to each module.