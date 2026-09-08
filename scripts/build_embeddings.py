import json
import os
from app.embeddings import EmbeddingManager, save_embeddings

def main():
    print("--- Building Local Embeddings ---")
    
    chunks_path = 'data/chunks.json'
    if not os.path.exists(chunks_path):
        print("\u274c Error: data/chunks.json not found. Run ingest.py first.")
        return
        
    with open(chunks_path, 'r', encoding='utf-8') as f:
        chunks = json.load(f)
        
    if not chunks:
        print("\u274c No chunks to embed.")
        return
        
    texts = [c['text'] for c in chunks]
    
    manager = EmbeddingManager()
    
    print(f"Generating embeddings for {len(texts)} chunks using {manager.model.tokenizer.name_or_path}...")
    embeddings = manager.embed_texts(texts)
    
    save_embeddings(embeddings, chunks)
    
    print("\n--- Summary ---")
    print(f"Chunks embedded: {len(chunks)}")
    print(f"Embedding dimensions: {embeddings.shape}")
    print(f"Model dimensions: {manager.model.get_sentence_embedding_dimension()}")
    print(f"Embedding file: data/embeddings/chunk_embeddings.npy")
    print(f"Index mapping file: data/embeddings/chunk_index.json")

if __name__ == "__main__":
    main()
