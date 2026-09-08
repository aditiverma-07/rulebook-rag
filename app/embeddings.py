import os
import json
import numpy as np
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer

# We use a lightweight multilingual model that's very fast and effective.
# Using 'all-MiniLM-L6-v2' as it is <100MB and great for local RAG MVP.
MODEL_NAME = os.getenv('LLM_MODEL', 'all-MiniLM-L6-v2')

class EmbeddingManager:
    def __init__(self, model_name: str = MODEL_NAME):
        self.model = SentenceTransformer(model_name)
        
    def embed_texts(self, texts: List[str]) -> np.ndarray:
        """Embeds a list of texts and returns normalized vectors for cosine similarity."""
        embeddings = self.model.encode(texts, normalize_embeddings=True, show_progress_bar=True)
        return embeddings

    def embed_query(self, query: str) -> np.ndarray:
        """Embeds a single query string, returning a normalized 1D array."""
        embedding = self.model.encode([query], normalize_embeddings=True)[0]
        return embedding

def save_embeddings(embeddings: np.ndarray, chunks: List[Dict], embed_dir: str = 'data/embeddings'):
    """Saves embeddings and index metadata to disk deterministically."""
    os.makedirs(embed_dir, exist_ok=True)
    np.save(os.path.join(embed_dir, 'chunk_embeddings.npy'), embeddings)
    
    index_mapping = []
    for i, c in enumerate(chunks):
        index_mapping.append({
            "vector_index": i,
            "chunk_id": c.get('chunk_id')
        })
    with open(os.path.join(embed_dir, 'chunk_index.json'), 'w', encoding='utf-8') as f:
        json.dump(index_mapping, f, indent=4)
        
def load_embeddings(embed_dir: str = 'data/embeddings') -> Tuple[np.ndarray, List[Dict]]:
    """Loads embeddings and index metadata from disk."""
    emb_path = os.path.join(embed_dir, 'chunk_embeddings.npy')
    idx_path = os.path.join(embed_dir, 'chunk_index.json')
    
    if not os.path.exists(emb_path) or not os.path.exists(idx_path):
        raise FileNotFoundError(f"Embedding files not found in {embed_dir}. Run build_embeddings.py first.")
        
    embeddings = np.load(emb_path)
    with open(idx_path, 'r', encoding='utf-8') as f:
        index_mapping = json.load(f)
        
    # Validate dimensions
    if len(embeddings) != len(index_mapping):
        raise ValueError("Mismatch between number of vectors and index mapping entries.")
        
    return embeddings, index_mapping
