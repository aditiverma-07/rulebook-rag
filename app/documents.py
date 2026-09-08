import os
import re
import csv
import json
import uuid
import pdfplumber
from typing import List, Optional, Dict, Any
from pydantic import BaseModel

class Chunk(BaseModel):
    chunk_id: str
    text: str
    source: str
    file_type: str
    section: Optional[str] = None
    page: Optional[int] = None
    metadata: Dict[str, Any] = {}

def split_into_chunks(text: str, max_words: int = 300) -> List[str]:
    """Splits a large text block into smaller chunks based on word count, without breaking paragraphs unnecessarily."""
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = []
    current_length = 0
    
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        words = p.split()
        
        # If a single paragraph is too large, just add it (or it could be further split by sentence)
        # But for university rules, a paragraph is usually coherent.
        if current_length + len(words) > max_words and current_chunk:
            chunks.append('\n\n'.join(current_chunk))
            current_chunk = [p]
            current_length = len(words)
        else:
            current_chunk.append(p)
            current_length += len(words)
            
    if current_chunk:
        chunks.append('\n\n'.join(current_chunk))
        
    return chunks

def ingest_markdown(filepath: str) -> List[Chunk]:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    lines = content.split('\n')
    
    document_title = None
    current_section = None
    current_clause = None
    
    chunks = []
    current_text = []
    
    def finalize_chunk():
        if current_text:
            text_block = '\n'.join(current_text).strip()
            if text_block:
                split_texts = split_into_chunks(text_block)
                for t in split_texts:
                    meta = {}
                    if document_title:
                        meta["document_title"] = document_title
                    if current_clause:
                        meta["clause"] = current_clause
                    
                    section_name = current_clause if current_clause else current_section
                    
                    chunks.append(Chunk(
                        chunk_id=f"chunk_{uuid.uuid4().hex[:8]}",
                        text=t,
                        source=filename,
                        file_type="markdown",
                        section=section_name,
                        page=None,
                        metadata=meta
                    ))
            current_text.clear()

    for line in lines:
        if line.startswith('# '):
            document_title = line[2:].strip()
        elif line.startswith('## '):
            finalize_chunk()
            current_section = line[3:].strip()
            current_clause = None
        elif line.startswith('### '):
            finalize_chunk()
            current_clause = line[4:].strip()
        else:
            current_text.append(line)
            
    finalize_chunk()
    return chunks

def ingest_pdf(filepath: str) -> List[Chunk]:
    filename = os.path.basename(filepath)
    chunks = []
    
    current_section = None
    
    with pdfplumber.open(filepath) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if not text:
                continue
                
            lines = text.split('\n')
            current_text = []
            
            def finalize_pdf_chunk():
                if current_text:
                    text_block = '\n'.join(current_text).strip()
                    if text_block:
                        split_texts = split_into_chunks(text_block)
                        for t in split_texts:
                            chunks.append(Chunk(
                                chunk_id=f"chunk_{uuid.uuid4().hex[:8]}",
                                text=t,
                                source=filename,
                                file_type="pdf",
                                section=current_section,
                                page=page_num,
                                metadata={"document_title": filename}
                            ))
                    current_text.clear()
                    
            for line in lines:
                # Basic section matching for PDF based on how it was generated
                if re.match(r'^\d+\.\s+[A-Z]', line) or re.match(r'^\d+\.\d+\s+[A-Z]', line):
                    finalize_pdf_chunk()
                    current_section = line.strip()
                else:
                    current_text.append(line)
                    
            finalize_pdf_chunk()
            
    return chunks

def ingest_csv(filepath: str) -> List[Chunk]:
    filename = os.path.basename(filepath)
    chunks = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            text_repr = f"Table: {filename}\n"
            for k, v in row.items():
                text_repr += f"{k}: {v}\n"
            
            first_val = list(row.values())[0] if row else None
            
            chunks.append(Chunk(
                chunk_id=f"chunk_{uuid.uuid4().hex[:8]}",
                text=text_repr.strip(),
                source=filename,
                file_type="csv",
                section=first_val,
                page=None,
                metadata={"table_row": first_val}
            ))
    return chunks
