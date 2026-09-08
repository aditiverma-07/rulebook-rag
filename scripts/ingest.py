import os
import json
from app.documents import ingest_markdown, ingest_pdf, ingest_csv

def main():
    corpus_dir = 'corpus'
    all_chunks = []
    
    md_dir = os.path.join(corpus_dir, 'markdown')
    pdf_dir = os.path.join(corpus_dir, 'pdf')
    csv_dir = os.path.join(corpus_dir, 'tables')
    
    files_processed = 0
    
    # Process Markdown
    if os.path.exists(md_dir):
        for f in os.listdir(md_dir):
            if f.endswith('.md'):
                chunks = ingest_markdown(os.path.join(md_dir, f))
                all_chunks.extend(chunks)
                files_processed += 1
                
    # Process PDF
    if os.path.exists(pdf_dir):
        for f in os.listdir(pdf_dir):
            if f.endswith('.pdf'):
                chunks = ingest_pdf(os.path.join(pdf_dir, f))
                all_chunks.extend(chunks)
                files_processed += 1
                
    # Process CSV
    if os.path.exists(csv_dir):
        for f in os.listdir(csv_dir):
            if f.endswith('.csv'):
                chunks = ingest_csv(os.path.join(csv_dir, f))
                all_chunks.extend(chunks)
                files_processed += 1
                
    # Save output
    data_dir = 'data'
    os.makedirs(data_dir, exist_ok=True)
    out_path = os.path.join(data_dir, 'chunks.json')
    
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump([c.model_dump() for c in all_chunks], f, indent=4)
        
    # Calculate Stats
    md_count = sum(1 for c in all_chunks if c.file_type == 'markdown')
    pdf_count = sum(1 for c in all_chunks if c.file_type == 'pdf')
    csv_count = sum(1 for c in all_chunks if c.file_type == 'csv')
    total_words = sum(len(c.text.split()) for c in all_chunks)
    avg_words = total_words / len(all_chunks) if all_chunks else 0
    with_section = sum(1 for c in all_chunks if c.section)
    with_source = sum(1 for c in all_chunks if c.source)
    
    print(f"Documents processed: {files_processed}")
    print(f"Total chunks: {len(all_chunks)}")
    print(f"Markdown chunks: {md_count}")
    print(f"PDF chunks: {pdf_count}")
    print(f"CSV chunks: {csv_count}")
    print(f"Average chunk size (words): {avg_words:.1f}")
    print(f"Chunks with section metadata: {with_section} ({(with_section/len(all_chunks))*100:.1f}%)")
    print(f"Chunks with source metadata: {with_source} ({(with_source/len(all_chunks))*100:.1f}%)")

if __name__ == '__main__':
    main()
