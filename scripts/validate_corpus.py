import os
import json
import csv
import pdfplumber

def count_words_in_file(filepath):
    words = 0
    ext = os.path.splitext(filepath)[1].lower()
    
    if ext == '.md':
        with open(filepath, 'r', encoding='utf-8') as f:
            words += len(f.read().split())
    elif ext == '.csv':
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                words += sum(len(cell.split()) for cell in row)
    elif ext == '.pdf':
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        words += len(text.split())
        except Exception as e:
            print(f"Error reading PDF {filepath}: {e}")
    return words

def main():
    print("--- Corpus Validation ---")
    corpus_dirs = ['corpus/markdown', 'corpus/pdf', 'corpus/tables']
    total_words = 0
    file_counts = {'.md': 0, '.pdf': 0, '.csv': 0}
    
    for d in corpus_dirs:
        if os.path.exists(d):
            for filename in os.listdir(d):
                filepath = os.path.join(d, filename)
                ext = os.path.splitext(filename)[1].lower()
                if ext in file_counts:
                    w_count = count_words_in_file(filepath)
                    print(f"{filename}: {w_count} words")
                    total_words += w_count
                    file_counts[ext] += 1
    
    print(f"\nTotal Corpus Word Count: {total_words}")
    if total_words > 6000:
        print("✅ Word count exceeds 6000")
    else:
        print("❌ Word count is less than 6000")
        
    print("\n--- File Format Check ---")
    print(f"Markdown files: {file_counts['.md']}")
    print(f"PDF files: {file_counts['.pdf']}")
    print(f"CSV files: {file_counts['.csv']}")
    
    if file_counts['.md'] >= 1 and file_counts['.pdf'] >= 1 and file_counts['.csv'] >= 1:
        print("✅ All required formats are present")
    else:
        print("❌ Missing required formats")
        
    print("\n--- Conflicts Check ---")
    try:
        with open('corpus/conflicts.json', 'r', encoding='utf-8') as f:
            conflicts = json.load(f)
            print(f"Conflicts defined: {len(conflicts)}")
            if len(conflicts) >= 3:
                print("✅ Found at least 3 planted conflicts")
            else:
                print("❌ Insufficient planted conflicts")
    except Exception as e:
        print(f"❌ Error reading conflicts.json: {e}")
        
    print("\n--- Test Questions Check ---")
    try:
        with open('tests/test_questions.json', 'r', encoding='utf-8') as f:
            tests = json.load(f)
            answered = sum(1 for t in tests if t.get('expected_type') == 'answered')
            conflict = sum(1 for t in tests if t.get('expected_type') == 'conflict')
            not_covered = sum(1 for t in tests if t.get('expected_type') == 'not_covered')
            
            print(f"Answered: {answered}, Conflict: {conflict}, Not Covered: {not_covered}")
            
            if answered >= 10 and conflict >= 3 and not_covered >= 25:
                print("✅ Test question counts meet requirements")
            else:
                print("❌ Test question counts do not meet requirements")
    except Exception as e:
        print(f"❌ Error reading test_questions.json: {e}")

    print("\n--- NOT_COVERED validation ---")
    try:
        import re
        with open('data/chunks.json', 'r', encoding='utf-8') as f:
            chunks = json.load(f)
        corpus_text = " ".join([c['text'].lower() for c in chunks])
        
        with open('tests/test_questions.json', 'r', encoding='utf-8') as f:
            tests = json.load(f)
            not_covered = [t for t in tests if t.get('expected_type') == 'not_covered']
            
        contamination_rules = {
            "QN001": r"smartwatch",
            "QN002": r"roommate dispute",
            "QN003": r"reimbursement.*conference|conference.*reimbursement",
            "QN004": r"semester abroad|study abroad",
            "QN005": r"lose.*student id|lost.*student id",
            "QN006": r"dress code",
            "QN007": r"park.*car|personal car",
            "QN008": r"pets.*hostel",
            "QN009": r"internship semester",
            "QN010": r"student discount.*transport",
            "QN011": r"student loan\b",
            "QN012": r"test tube.*chemistry",
            "QN013": r"smoking permitted",
            "QN014": r"change.{1,40}major",
            "QN015": r"visitors.*daytime",
            "QN016": r"join.*sports team",
            "QN017": r"political protest",
            "QN018": r"dental",
            "QN019": r"print.*limit",
            "QN020": r"credit card",
            "QN021": r"cafeteria.*hours",
            "QN022": r"financial aid.*international",
            "QN023": r"transcript.*foreign university",
            "QN024": r"parent submit.*assignment",
            "QN025": r"cryptocurrency"
        }
        
        contaminated_count = 0
        clean_count = 0
        for q in not_covered:
            qid = q['id']
            rule = contamination_rules.get(qid)
            if rule and re.search(rule, corpus_text):
                print(f"{qid}: FAILED (Contaminated)")
                contaminated_count += 1
            else:
                print(f"{qid}: PASS")
                clean_count += 1
                
        print(f"\nContaminated questions: {contaminated_count}")
        print(f"Clean NOT_COVERED questions: {clean_count}")
        if contaminated_count > 0:
            print("❌ Remove contamination before proceeding.")
        else:
            print("✅ All NOT_COVERED questions remain clean.")
            
    except FileNotFoundError:
        print("⚠️ data/chunks.json not found yet, run ingest.py first to check contamination.")
    except Exception as e:
        print(f"❌ Error during NOT_COVERED check: {e}")

if __name__ == '__main__':
    main()
