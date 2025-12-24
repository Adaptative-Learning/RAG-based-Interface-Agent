from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import json
import os
import sys
from dotenv import load_dotenv

# Add the current directory to the path so we can import from src
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# Also add parent directory for when running from root
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import our existing classes
from vector_store import VectorStore
from llm_analyzer import LLMAnalyzer
from questionnaire import Questionnaire

# Load environment variables
load_dotenv()

app = FastAPI(
    title="RAG-based IT Orientation API",
    description="API for adaptive learning system using RAG technology",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Specify frontend origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models for request/response
class Answer(BaseModel):
    question_id: int
    answer: str

class QuestionnaireResponse(BaseModel):
    answers: List[Answer]

class Question(BaseModel):
    id: int
    question: str
    type: str
    options: List[str]
    linked_domains: List[str]

class QuestionnaireData(BaseModel):
    title: str
    description: str
    questions: List[Question]

class Prediction(BaseModel):
    domaine: str
    score: int
    raisons: List[str]
    confiance: str
    points_forts: List[str]
    axes_amelioration: List[str]

class AnalysisResult(BaseModel):
    predictions: List[Prediction]
    resume_global: str
    top_3_recommandations: List[str]

# Global variables for our services (initialized lazily)
vector_store = None
analyzer = None

def initialize_services():
    """Initialize the vector store and analyzer services."""
    global vector_store, analyzer

    if vector_store is None:
        print("Initializing vector store...")
        try:
            # Use absolute path to data directory from the script location
            script_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(script_dir)
            data_path = os.path.join(project_root, 'data', 'domaines')
            print(f"Loading domains from: {data_path}")
            vector_store = VectorStore()
            vector_store.load_domains(data_path)
            print("Vector store initialized successfully")
        except Exception as e:
            print(f"Error initializing vector store: {e}")
            import traceback
            traceback.print_exc()
            raise

    if analyzer is None:
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            print("Warning: GROQ_API_KEY not configured")
            # Don't raise error here, let the endpoint handle it
        else:
            try:
                analyzer = LLMAnalyzer(api_key)
                print("LLM analyzer initialized successfully")
            except Exception as e:
                print(f"Error initializing analyzer: {e}")
                import traceback
                traceback.print_exc()
                raise

@app.get("/questions", response_model=QuestionnaireData)
async def get_questions():
    """
    Get all questions with their options.
    Returns the complete questionnaire structure.
    """
    try:
        # Load questionnaire from JSON file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        questionnaire_path = os.path.join(project_root, 'questionnaire.json')
        print(f"Loading questionnaire from: {questionnaire_path}")
        with open(questionnaire_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return QuestionnaireData(**data)

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Questionnaire file not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading questions: {str(e)}")

@app.post("/analyze", response_model=AnalysisResult)
async def analyze_responses(response: QuestionnaireResponse):
    """
    Analyze the questionnaire responses and return IT domain recommendations.
    Returns JSON with predictions, global summary, and top recommendations.
    """
    try:
        # Initialize services if not already done
        initialize_services()

        # Convert responses to the format expected by our analyzer
        responses_formatted = []
        for answer in response.answers:
            # Find the question text (we need to load questions to match)
            with open('questionnaire.json', 'r', encoding='utf-8') as f:
                questionnaire_data = json.load(f)

            question_text = None
            for q in questionnaire_data['questions']:
                if q['id'] == answer.question_id:
                    question_text = q['question']
                    break

            if question_text:
                responses_formatted.append({
                    'question': question_text,
                    'answer': answer.answer
                })

        if not responses_formatted:
            raise HTTPException(status_code=400, detail="No valid responses provided")

        # Get similar domains from vector store
        all_answers = " ".join([r['answer'] for r in responses_formatted])
        similar_domains = vector_store.find_similar_domains(all_answers)

        # Analyze with LLM
        results = analyzer.analyze_responses(responses_formatted, similar_domains)

        # Check for errors in results
        if "error" in results:
            raise HTTPException(status_code=500, detail=f"Analysis error: {results['error']}")

        # Validate that predictions exist
        if "predictions" not in results:
            raise HTTPException(status_code=500, detail="No predictions generated")

        return AnalysisResult(**results)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "RAG IT Orientation API"}

# Remove the server startup code - use api_runner.py instead