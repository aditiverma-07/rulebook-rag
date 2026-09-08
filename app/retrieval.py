import json
import numpy as np
from typing import List, Dict, Any
from app.embeddings import EmbeddingManager, load_embeddings

class Retriever:
    def __init__(self, data_dir: str = 'data'):
        # Load embeddings and their corresponding chunk IDs
        self.embeddings, self.index_mapping = load_embeddings(f"{data_dir}/embeddings")
        
        # Load the actual chunk text/metadata to enrich results
        chunks_path = f"{data_dir}/chunks.json"
        with open(chunks_path, 'r', encoding='utf-8') as f:
            chunks_data = json.load(f)
            self.chunk_dict = {c['chunk_id']: c for c in chunks_data}
            
        # Model is kept loaded in memory for quick query inference
        self.embed_manager = EmbeddingManager()
        
    def retrieve(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieves the top_k most similar chunks using brute-force NumPy cosine similarity.
        """
        if not query or not query.strip():
            raise ValueError("Query cannot be empty.")
        if top_k <= 0:
            raise ValueError("top_k must be strictly positive.")
            
        query_embedding = self.embed_manager.embed_query(query)
        
        # Because the embeddings were normalized during creation, 
        # the dot product is exactly mathematically equivalent to cosine similarity.
        # embeddings shape: (N, D), query_embedding shape: (D,)
        similarities = self.embeddings @ query_embedding
        
        # Argsort gives ascending order, so we reverse it with [::-1]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            score = float(similarities[idx])
            chunk_id = self.index_mapping[idx]['chunk_id']
            chunk_data = self.chunk_dict[chunk_id]
            
            results.append({
                "chunk_id": chunk_id,
                "score": score,
                "text": chunk_data.get("text", ""),
                "source": chunk_data.get("source"),
                "section": chunk_data.get("section"),
                "page": chunk_data.get("page"),
                "file_type": chunk_data.get("file_type"),
                "metadata": chunk_data.get("metadata", {})
            })
            
        return results
