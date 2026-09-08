# Rulebook RAG: The Rulebook That Argues With Itself

## Problem Statement
The goal is to build a question-answering system over a university rulebook corpus. Unlike generic chatbots, this system strictly grounds its answers on the provided documents. It must return exact passages, highlight rule references, evaluate confidence, and decisively detect cases where the corpus doesn't hold the answer (`NOT_COVERED`) or where the corpus contradicts itself (`CONFLICT`). 

Why this matters: In institutional policy management, silent hallucination or arbitrary conflict resolution by an LLM is unacceptable. Real-world rulebooks contain edge cases and contradictory clauses. Highlighting these conflicts transparently is often more useful than a fabricated "best guess."

## Features (Planned)
- Grounded Semantic Search using NumPy-based cosine similarity
- Section-aware chunking and metadata preservation
- Three-tier response classification: `ANSWERED`, `NOT_COVERED`, and `CONFLICT`
- Explicit conflict detection algorithms and grounded LLM generation
- Clean, vanilla JS frontend to display citations and similarities

## Technology Stack
- **Backend**: Python, FastAPI, Uvicorn, Pydantic
- **AI/ML**: `sentence-transformers/all-MiniLM-L6-v2` (running locally), NumPy (for cosine similarity)
- **Document Parsing**: `pdfplumber`, `pandas`
- **Frontend**: Vanilla HTML, CSS, JavaScript (Zero-dependency)
- **Testing & Evaluation**: Pytest, custom automated evaluation harness

## Corpus and Dataset Design
This repository contains a purely **synthetic corpus** designed for the DigiValet assessment: **"Medicaps Institute of Technology — Academic & Student Regulations 2026"**. 
*Note: This is not an actual institution's policy.*

### Document Formats
The corpus includes multiple formats to test ingestion robustness:
- Markdown (`corpus/markdown/`)
- PDF (`corpus/pdf/`)
- Tabular CSV (`corpus/tables/`)

### Main Regulation Topics Covered
- Course Registration & Add/Drop
- Attendance, Shortage & Condonation
- Medical Leave and Exemptions
- Examinations & Internal Assessment
- Grading, Revaluation & Academic Appeals
- Student Discipline & Examination Malpractice
- Hostel & Library Regulations
- Financial Policies, Fees, Deadlines, & Scholarships

### Planted Conflicts
The corpus contains **3 intentionally planted contradictions**:
1. **Attendance Condonation Limit**: 10% vs. 15% across different documents.
2. **Medical Leave Documentation Deadline**: 7 calendar days vs. 5 working days.
3. **Autumn Fee Deadline**: September 10 vs. September 15.

These conflicts serve to evaluate the pipeline's ability to identify competing regulations rather than arbitrarily picking one.

### Test Dataset
A test dataset (`tests/test_questions.json`) includes:
- **10 Answered Questions**: Simple factual retrieval.
- **3 Conflict Questions**: Directly probing the planted contradictions.
- **25 Not Covered Questions**: "Adjacent" questions that sound extremely plausible for a university handbook (e.g., "Can I park my personal car on the university campus?") but whose answers are deliberately missing from the corpus. This ensures the RAG pipeline is thoroughly tested for hallucination resistance.

This ensures the RAG pipeline is thoroughly tested for hallucination resistance.

## Document Ingestion & Chunking
The corpus is processed by an ingestion pipeline (`app/documents.py`) that respects structural and semantic boundaries. 

### Supported Formats
1. **Markdown**: Extracted keeping section (`##`) and clause (`###`) boundaries intact.
2. **PDF**: Extracted using `pdfplumber`, keeping track of page numbers and document-level headers.
3. **CSV (Tables)**: Converted into textual representations (e.g. `Fee Type: Autumn Semester Tuition\nDeadline: September 10, 2026`) preserving table rows and columns.

### Metadata Preservation
Discarding location context during chunking leads to a loss of citation ability. Every chunk strictly retains:
- `source`: The filename (e.g. `01_academic_regulations.md`)
- `section`: The hierarchical section or clause (e.g. `3.2.1 Minimum Attendance`)
- `page`: Page numbers (for PDF documents)

This metadata makes the final web UI's citations credible and verifiable.

### Storage
Chunks are generated and serialized locally to `data/chunks.json` for subsequent embedding and retrieval phases. No external vector databases (like Pinecone or Chroma) are used, keeping the application entirely self-contained.

## Embedding & Semantic Retrieval
The RAG pipeline operates fully locally without requiring paid API endpoints for embedding or retrieval.

### Local Embeddings
Embeddings are generated using the lightweight `sentence-transformers/all-MiniLM-L6-v2` model, producing 384-dimensional vectors. 
- Generated embeddings are saved directly as a NumPy array (`data/embeddings/chunk_embeddings.npy`).
- A deterministic index mapping connects vector indices directly to their corresponding `chunk_id`.

### Retrieval Mechanism
- The `app/retrieval.py` module performs semantic searches by converting the user query into a 384-dimensional vector.
- Retrieval relies on brute-force NumPy matrix multiplication. Because embeddings are L2 normalized during creation, the dot product computes the precise cosine similarity.
- The pipeline avoids Vector DBs (like Pinecone, FAISS, or Chroma) to maximize code transparency and reduce operational overhead for this dataset.

### Pipeline Architecture
```text
Rulebook Documents
       ↓
Document Chunks
       ↓
Sentence Transformer (all-MiniLM-L6-v2)
       ↓
Local Embeddings (.npy)
       ↓
NumPy Cosine Similarity
       ↓
Top-K Evidence
       ↓
Evidence Decision Engine
       ↓
ANSWERED / NOT_COVERED / CONFLICT
```

## Evidence Decision Engine
The core intelligence layer evaluates the retrieved Top-K chunks without relying on an external LLM. It applies a series of cascading logic checks:

1. **Similarity Thresholds**: Chunks below strict retrieval thresholds are rejected immediately.
2. **Vocabulary & Suffix Overlap Guardrails**: Prevents semantic drift hallucination. The engine extracts nouns from the query and ensures that key concepts (and their morphological variations) are actually present in the retrieved chunks. This ensures that queries about topics missing from the corpus (e.g., "pets", "cryptocurrency") are decisively flagged as `NOT_COVERED`.
3. **Regex Conflict Detection**: For numerical constraints (dates, durations, percentages), the engine extracts signals using Regex and checks for disjoint values across the highly relevant chunks. If differing rules for the exact same context are found (e.g., 10% vs 15% condonation), the system alerts the user with a `CONFLICT` instead of silently guessing.

## Phase 6: Grounded LLM API (`/ask`)
The `POST /ask` endpoint integrates a Large Language Model (configured via environment variables) to synthesize the retrieved evidence into a human-readable answer.

### Strict Decision Enforcement
The LLM is strictly constrained by the Phase 5 decision engine. It **cannot** override the decision:
- If `NOT_COVERED`, the API returns a deterministic safe response without calling the LLM.
- If `CONFLICT`, the LLM is instructed to explicitly present both sides of the contradiction.
- If `ANSWERED`, the LLM synthesizes an answer using *only* the retrieved evidence and cites its sources.

### Example Request
```bash
curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"query": "What is the minimum attendance requirement?"}'
```

### Example Response
```json
{
  "query": "What is the minimum attendance requirement?",
  "type": "answered",
  "answer": "Students must maintain a minimum attendance of 75% in each registered course to be eligible to appear for the end-semester examinations.\n\nSource: 01_academic_regulations.md, Section: 3.2.1 Minimum Attendance",
  "evidence": [
    {
      "chunk_id": "...",
      "source": "01_academic_regulations.md",
      "section": "3.2.1 Minimum Attendance",
      "page": null,
      "text": "Students must maintain a minimum attendance of 75% in each registered course...",
      "similarity": 0.76,
      "file_type": "markdown"
    }
  ],
  "reason": "Strong evidence found without conflict."
}
```

## Phase 7: Demo-Ready Frontend
The system features a polished, responsive, Vanilla HTML/CSS/JS frontend to interact with the `/ask` API. It dynamically visualizes the three states:
- **ANSWERED**: Shows the synthesized response with supporting evidence cards.
- **CONFLICT**: Warns the user visually and displays the contradictory evidence side-by-side.
- **NOT_COVERED**: Explicitly tells the user the information isn't in the rulebook, bypassing LLM hallucinations.

---

## 🚀 How to Run the Complete Application

1. **Clone the Repository & Setup Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Configuration**
   Copy `.env.example` to `.env` and set your API key if you wish to use the LLM (if omitted, the system falls back to safe deterministic strings):
   ```env
   LLM_PROVIDER=openai
   LLM_API_KEY=your_api_key_here
   LLM_MODEL=gpt-4o-mini
   LLM_BASE_URL=https://api.openai.com/v1
   ```

3. **Start the Application**
   The FastAPI server serves both the `POST /ask` API and the static frontend via `/`:
   ```bash
   uvicorn app.main:app --reload
   ```

4. **Access the Frontend**
   Open your browser and navigate to:
   [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### Example Queries to Try:
- "What is the minimum attendance requirement?" *(Expected: ANSWERED)*
- "When does the Add/Drop period close?" *(Expected: ANSWERED)*
- "Can I bring a smartwatch into the examination hall?" *(Expected: NOT_COVERED)*
- "What is the attendance condonation limit?" *(Expected: CONFLICT)*

### 📸 Screenshots
*(Placeholder for UI screenshots: Answered, Conflict, and Not Covered states)*

---

## Testing & Evaluation
The project includes a robust automated test suite (Pytest) and a dedicated system evaluator measuring retrieval accuracy, classification precision, and local inference latency.

### 1. Run Automated Safety & Quality Tests
```bash
pytest
```
Validates the backend routing, semantic similarity calculations, decision guardrails, and LLM hallucination resistance (ensuring `NOT_COVERED` never accesses the LLM).

### 2. Run the Evaluation Benchmark
```bash
python scripts/evaluate.py
```

### Final Benchmark Results (Phase 9)
- **Dataset Composition**: 38 Total Questions (10 Answered, 3 Conflict, 25 Not Covered)
- **Overall Classification Accuracy**: **92.1%**
  - `ANSWERED`: 100.0% (10/10)
  - `CONFLICT`: 100.0% (3/3)
  - `NOT_COVERED`: 88.0% (22/25)
- **Retrieval Hit Rate**: **100.0%** (Top-1, Top-3, Top-5 all successfully retrieved relevant evidence).
- **Conflict Retrieval**: **100.0%** (All sides of every planted conflict were successfully surfaced together).

### Latency Measurement (Local Fallback)
- **Embedding Generation**: ~19-20 ms
- **Retrieval Engine**: ~14-17 ms
- **Decision Engine**: ~1.2 ms
- **Total API Request (w/o external LLM)**: ~20-25 ms

### Known Limitations
- **Guardrail False Positives**: The strict vocabulary guardrails in the Decision Engine currently struggle with "deceptively simple" NOT_COVERED queries that share heavy keyword overlap with unrelated corpus sections (e.g., questions about "credit card fees" pull in generic "fee payment" documents). These queries incorrectly bypass the NOT_COVERED trap and trigger an ANSWERED evaluation (leading to the 92.1% accuracy cap). Solving this requires transitioning from heuristic thresholds to LLM-in-the-loop validation for the decision phase, trading latency for semantic reasoning.
  
# rulebook-rag
A grounded Rulebook QA system using RAG, semantic retrieval, conflict detection, and FastAPI.

