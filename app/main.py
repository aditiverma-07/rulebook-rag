import os
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import List, Optional

from app.retrieval import Retriever
from app.decision import evaluate_evidence, DecisionType, EvidenceItem
from app.llm import generate_answer

app = FastAPI(title="Rulebook RAG API")

# Initialize retriever (do it once on startup)
retriever = Retriever()


# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Mount frontend directory for static files (css, js)
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

@app.get("/")
async def serve_frontend():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Frontend not built yet. API is running."}

class AskRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="The question to ask the rulebook")

class AskResponse(BaseModel):
    query: str
    type: str
    answer: str
    evidence: List[EvidenceItem]
    reason: str

@app.post("/ask", response_model=AskResponse)
async def ask_question(request: AskRequest):
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Query cannot be empty")
    
    # 1. Retrieval
    retrieved_chunks = retriever.retrieve(query, top_k=15)
    
    # 2. Decision Engine
    decision = evaluate_evidence(query, retrieved_chunks)
    
    # 3. LLM Generation
    # We pass the decision to generate_answer, which strictly enforces the logic 
    # (e.g. no LLM generation for NOT_COVERED)
    answer = generate_answer(query, decision)
    
    return AskResponse(
        query=query,
        type=decision.type.value,
        answer=answer,
        evidence=decision.evidence,
        reason=decision.reason
    )
