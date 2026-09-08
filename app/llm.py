import os
import requests
from dotenv import load_dotenv
from typing import List
from app.decision import DecisionResult, DecisionType, EvidenceItem

# Load environment variables
load_dotenv()

LLM_PROVIDER = os.getenv("LLM_PROVIDER", "openai")
LLM_API_KEY = os.getenv("LLM_API_KEY", "")
LLM_MODEL = os.getenv("LLM_MODEL", "gpt-4o-mini")
LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")

if LLM_PROVIDER == "gemini" and LLM_MODEL == "gemini-3.6-flash":
    LLM_MODEL = "gemini-3.5-flash"

def _format_evidence(evidence: List[EvidenceItem]) -> str:
    formatted_chunks = []
    for i, e in enumerate(evidence):
        meta = []
        if e.source:
            meta.append(f"Source: {e.source}")
        if e.section:
            meta.append(f"Section: {e.section}")
        if e.page is not None:
            meta.append(f"Page: {e.page}")
        
        meta_str = ", ".join(meta)
        formatted_chunks.append(f"[Evidence {i+1}] ({meta_str})\n{e.text}\n")
    return "\n".join(formatted_chunks)

def generate_answer(query: str, decision: DecisionResult) -> str:
    # Strict rule: NEVER call LLM for NOT_COVERED
    if decision.type == DecisionType.NOT_COVERED:
        return "The rulebook corpus does not contain enough information to answer this question."
    
    # Check if LLM is configured
    if not LLM_API_KEY:
        if decision.type == DecisionType.ANSWERED:
            return "LLM is not configured. Grounded answer generation is unavailable."
        elif decision.type == DecisionType.CONFLICT:
            return "LLM is not configured. The rulebook corpus contains conflicting provisions relevant to this question."
        return ""

    evidence_text = _format_evidence(decision.evidence)
    
    if decision.type == DecisionType.ANSWERED:
        system_prompt = (
            "You are answering questions about a fictional university rulebook.\n"
            "Use ONLY the supplied evidence.\n"
            "Do not use outside knowledge.\n"
            "Do not infer policies that are not explicitly supported.\n"
            "If a requested detail is missing from the evidence, say so.\n"
            "Return a concise answer followed by the supporting rulebook references.\n"
        )
    elif decision.type == DecisionType.CONFLICT:
        system_prompt = (
            "You are answering questions about a fictional university rulebook.\n"
            "The retrieved evidence contains conflicting provisions regarding the user's query.\n"
            "You MUST explicitly state that the retrieved rulebook contains conflicting provisions.\n"
            "You MUST present BOTH conflicting provisions and identify their source, section, and page.\n"
            "Do NOT silently choose one as correct.\n"
            "Do NOT invent a resolution to the conflict.\n"
            "Explain the contradiction clearly.\n"
        )
    else:
        return "Invalid decision type."

    user_message = f"Query: {query}\n\nEvidence:\n{evidence_text}"

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.0
    }

    print(f"DEBUG: Making LLM request with model {payload['model']}", flush=True)
    try:
        response = requests.post(f"{LLM_BASE_URL}/chat/completions", headers=headers, json=payload, timeout=15)
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"].strip()
    except requests.exceptions.HTTPError as e:
        return f"HTTP Error: {str(e)} | Response: {e.response.text}"
    except Exception as e:
        return f"Error communicating with LLM: {str(e)}"
