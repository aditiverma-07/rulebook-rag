import re
from typing import List, Dict, Any, Tuple

def extract_signals(text: str) -> Dict[str, List[str]]:
    """
    Extract structured signals like percentages, dates, and durations from text.
    Returns a dictionary of category -> list of extracted string values.
    """
    text_lower = text.lower()
    signals = {
        "percentages": [],
        "dates": [],
        "durations": []
    }
    
    # Percentages: 10%, 15%
    pct_matches = re.findall(r'\b(\d+(?:\.\d+)?)\s*%', text_lower)
    signals["percentages"] = [f"{m}%" for m in pct_matches]
    
    # Dates: September 10, 15 September
    date_matches = re.findall(r'\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\s+\d{1,2}\b', text_lower)
    signals["dates"] = [m for m in date_matches]
    
    # Durations: 7 calendar days, 5 working days
    duration_matches = re.findall(r'\b\d+\s+(?:working\s+|calendar\s+|business\s+)?(?:days|weeks|months|years)\b', text_lower)
    signals["durations"] = [m for m in duration_matches]
    
    return signals

def get_query_signal_types(query: str) -> List[str]:
    query_lower = query.lower()
    types = []
    if any(w in query_lower for w in ["percent", "%"]):
        types.append("percentages")
    if any(w in query_lower for w in ["when", "deadline", "date", "time"]):
        types.append("dates")
    if any(w in query_lower for w in ["days", "weeks", "months", "how long", "duration"]):
        types.append("durations")
    return types

def detect_conflict(query: str, evidence: List[Dict[str, Any]]) -> Tuple[bool, List[Dict[str, Any]]]:
    if len(evidence) < 2:
        return False, []
        
    chunk_signals = []
    for chunk in evidence:
        sigs = extract_signals(chunk['text'])
        chunk_signals.append({
            "chunk": chunk,
            "signals": sigs
        })
        
    conflicting_chunks = []
    has_conflict = False
    
    categories = get_query_signal_types(query)
    if not categories:
        return False, []
    
    for category in categories:
        active_chunks = [cs for cs in chunk_signals if cs["signals"][category]]
        
        if len(active_chunks) >= 2:
            base_vals = set(active_chunks[0]["signals"][category])
            
            for other_cs in active_chunks[1:]:
                other_vals = set(other_cs["signals"][category])
                if base_vals.isdisjoint(other_vals):
                    has_conflict = True
                    if active_chunks[0]["chunk"] not in conflicting_chunks:
                        conflicting_chunks.append(active_chunks[0]["chunk"])
                    if other_cs["chunk"] not in conflicting_chunks:
                        conflicting_chunks.append(other_cs["chunk"])
                        
    return has_conflict, conflicting_chunks
