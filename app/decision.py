import re
import json
import os
from typing import List, Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel
from app.conflict import detect_conflict

class DecisionType(str, Enum):
    ANSWERED = "answered"
    NOT_COVERED = "not_covered"
    CONFLICT = "conflict"

class EvidenceItem(BaseModel):
    chunk_id: str
    source: str
    section: Optional[str] = None
    page: Optional[int] = None
    text: str
    similarity: float
    file_type: Optional[str] = None

class DecisionResult(BaseModel):
    type: DecisionType
    answer: str
    evidence: List[EvidenceItem]
    reason: str

_global_vocab = set()

def get_global_vocab() -> set:
    global _global_vocab
    if not _global_vocab:
        try:
            chunks_path = 'data/chunks.json'
            if os.path.exists(chunks_path):
                with open(chunks_path, 'r', encoding='utf-8') as f:
                    chunks = json.load(f)
                    combined = " ".join([c['text'].lower() for c in chunks])
                    _global_vocab = set(re.findall(r'\b[a-z]{3,}\b', combined))
        except Exception:
            pass
    return _global_vocab

def extract_nouns(text: str) -> set:
    """A simplistic heuristic to extract noun-like words from a query by ignoring common stopwords."""
    stopwords = {"what", "is", "the", "a", "an", "do", "does", "did", "can", "could", "would", "should",
                 "how", "much", "many", "percentage", "of", "to", "i", "you", "he", "she", "it", "we", "they",
                 "my", "your", "his", "her", "their", "our", "for", "in", "on", "at", "with", "by", "from",
                 "about", "as", "into", "like", "through", "after", "over", "between", "out", "against",
                 "during", "without", "before", "under", "around", "among", "are", "be", "been", "being",
                 "have", "has", "had", "will", "shall", "may", "might", "must", "if", "then", "else", "when",
                 "where", "why", "who", "which", "that", "this", "these", "those", "and", "but", "or", "not",
                 "no", "yes", "any", "all", "some", "every", "each", "both", "few", "more", "most", "other",
                 "another", "such", "only", "own", "same", "so", "than", "too", "very", "just", "now", "up",
                 "down", "here", "there", "there", "out", "very", "required", "eligible", "allowed", "bring", "submit", "apply",
                 "provide", "change", "join", "pay", "use", "using", "take", "make", "get", "need", "needs", "happen", "happens"}
                 
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    return {w for w in words if w not in stopwords}

def evaluate_evidence(query: str, retrieved: List[Dict[str, Any]], 
                      retrieval_min_score: float = 0.35, 
                      evidence_min_score: float = 0.40) -> DecisionResult:
    """
    Evaluates raw retrieved chunks to determine evidence sufficiency and detect conflicts.
    """
    if not retrieved:
        return DecisionResult(
            type=DecisionType.NOT_COVERED,
            answer="The rulebook does not contain enough information to answer this question.",
            evidence=[],
            reason="No chunks were retrieved."
        )
        
    top_score = retrieved[0]['score']
    
    if top_score < retrieval_min_score:
        return DecisionResult(
            type=DecisionType.NOT_COVERED,
            answer="The rulebook does not contain enough information to answer this question.",
            evidence=[],
            reason=f"Top score {top_score:.2f} is below retrieval threshold {retrieval_min_score}."
        )
        
    query_nouns = extract_nouns(query)
    vocab = get_global_vocab()
    
    if vocab and query_nouns:
        missing_from_corpus = set()
        for q in query_nouns:
            found = False
            if q in vocab:
                found = True
            else:
                for suffix in ['s', 'es', 'ed', 'ing', 'd', 'ation', 'ly', 'ment']:
                    if q.endswith(suffix) and q[:-len(suffix)] in vocab:
                        found = True
                        break
                    for v in vocab:
                        if v.endswith(suffix) and v[:-len(suffix)] == q:
                            found = True
                            break
                    if found:
                        break
            if not found:
                missing_from_corpus.add(q)
                
        # Only trigger not_covered if we are sure an essential keyword is entirely missing
        if missing_from_corpus:
            return DecisionResult(
                type=DecisionType.NOT_COVERED,
                answer="The rulebook does not contain enough information to answer this question.",
                evidence=[],
                reason=f"Key query concepts {missing_from_corpus} are entirely absent from the corpus."
            )

    strong_evidence = [c for c in retrieved if c['score'] >= evidence_min_score]
    
    if not strong_evidence:
        return DecisionResult(
            type=DecisionType.NOT_COVERED,
            answer="The rulebook does not contain enough information to answer this question.",
            evidence=[],
            reason=f"No chunks passed evidence threshold {evidence_min_score}."
        )
        
    has_conflict, conflicting_chunks = detect_conflict(query, strong_evidence)
    if has_conflict:
        evidence_items = [
            EvidenceItem(
                chunk_id=c['chunk_id'],
                source=c['source'],
                section=c['section'],
                page=c['page'],
                text=c['text'],
                similarity=c['score'],
                file_type=c['file_type']
            ) for c in conflicting_chunks
        ]
        return DecisionResult(
            type=DecisionType.CONFLICT,
            answer="The rulebook contains conflicting provisions on this issue.",
            evidence=evidence_items,
            reason="Contradictory numeric signals found in top evidence."
        )
        
    evidence_items = [
        EvidenceItem(
            chunk_id=c['chunk_id'],
            source=c['source'],
            section=c['section'],
            page=c['page'],
            text=c['text'],
            similarity=c['score'],
            file_type=c['file_type']
        ) for c in strong_evidence[:3]
    ]
    return DecisionResult(
        type=DecisionType.ANSWERED,
        answer="Sufficient evidence found to answer this question.",
        evidence=evidence_items,
        reason="Strong evidence found without conflict."
    )
