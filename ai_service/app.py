"""
AI Query Service — entry point.

Exposes a single REST endpoint that receives a natural-language question
and returns a grounded answer, built using product/stock tools.

Run locally:
    uvicorn app:app --reload --port 8000
"""

from dotenv import load_dotenv

load_dotenv()  # loads GROQ_API_KEY (and anything else) from a local .env file

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from agent import answer_question

app = FastAPI(title="HBntory AI Query Service")

# The Client Web Interface (Task 6) runs on a different origin/port during
# development, so CORS must be enabled explicitly. Restrict allow_origins
# to the real client URL(s) before any production-like demo.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: restrict to the Client Web origin
    allow_methods=["POST"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    question: str


class QueryResponse(BaseModel):
    answer: str
    sources: list[str] = []


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/api/v1/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    """
    Each request is handled independently — no conversation history is
    stored or expected (per project scope).
    """
    result = answer_question(request.question)
    return QueryResponse(answer=result["answer"], sources=result["sources"])
