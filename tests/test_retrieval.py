import pytest
import numpy as np
from app.retrieval import Retriever

@pytest.fixture(scope="module")
def retriever():
    try:
        return Retriever()
    except FileNotFoundError:
        pytest.skip("Embeddings not built. Run build_embeddings.py first.")

def test_retriever_initialization(retriever):
    assert len(retriever.embeddings.shape) == 2, "Embeddings should be a 2D matrix"
    assert len(retriever.index_mapping) == retriever.embeddings.shape[0], "Index mapping length should match vector count"

def test_empty_query(retriever):
    with pytest.raises(ValueError, match="Query cannot be empty"):
        retriever.retrieve("")
        
    with pytest.raises(ValueError, match="Query cannot be empty"):
        retriever.retrieve("   ")

def test_invalid_top_k(retriever):
    with pytest.raises(ValueError, match="top_k must be strictly positive"):
        retriever.retrieve("attendance", top_k=-1)
        
    with pytest.raises(ValueError, match="top_k must be strictly positive"):
        retriever.retrieve("attendance", top_k=0)

def test_retrieval_format(retriever):
    results = retriever.retrieve("test query", top_k=3)
    assert len(results) == 3, "Should return exactly top_k results"
    for res in results:
        assert "chunk_id" in res
        assert "score" in res
        assert "text" in res
        assert "source" in res
        assert "file_type" in res
        assert isinstance(res["score"], float)
        
def test_sorting_order(retriever):
    results = retriever.retrieve("attendance", top_k=5)
    scores = [r['score'] for r in results]
    
    # Check descending order
    for i in range(len(scores) - 1):
        assert scores[i] >= scores[i+1], "Scores are not properly sorted in descending order"
