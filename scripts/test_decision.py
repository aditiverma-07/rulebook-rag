import json
from app.retrieval import Retriever
from app.decision import evaluate_evidence

def main():
    print("Loading Retriever and Decision Engine...")
    retriever = Retriever()
    
    with open('tests/test_questions.json', 'r', encoding='utf-8') as f:
        questions = json.load(f)
        
    print(f"Testing {len(questions)} questions...\n")
    
    passed = 0
    failed = 0
    failures = []
    
    category_stats = {
        "answered": {"total": 0, "passed": 0},
        "not_covered": {"total": 0, "passed": 0},
        "conflict": {"total": 0, "passed": 0},
    }
    
    for q in questions:
        qid = q['id']
        query = q['question']
        expected = q['expected_type']
        
        # 1. Retrieve
        retrieved = retriever.retrieve(query, top_k=15)
        
        # 2. Evaluate
        result = evaluate_evidence(query, retrieved, retrieval_min_score=0.40, evidence_min_score=0.40)
        
        category_stats[expected]["total"] += 1
        
        if result.type.value == expected:
            print(f"{qid} [{expected}]: PASS")
            passed += 1
            category_stats[expected]["passed"] += 1
        else:
            print(f"{qid} [{expected}]: FAIL (Predicted: {result.type.value})")
            failed += 1
            failures.append({
                "id": qid,
                "query": query,
                "expected": expected,
                "predicted": result.type.value,
                "reason": result.reason,
                "top_score": retrieved[0]['score'] if retrieved else 0
            })
            
    print("\n--- Summary ---")
    print(f"Total: {len(questions)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    accuracy = (passed / len(questions)) * 100
    print(f"Accuracy: {accuracy:.1f}%")
    
    print("\n--- Category Accuracy ---")
    for cat, stats in category_stats.items():
        if stats["total"] > 0:
            cat_acc = (stats["passed"] / stats["total"]) * 100
            print(f"{cat.upper()}: {cat_acc:.1f}% ({stats['passed']}/{stats['total']})")
            
    if failures:
        print("\n--- Failure Details ---")
        for fail in failures:
            print(f"{fail['id']}: Expected {fail['expected']}, got {fail['predicted']}")
            print(f"  Query: {fail['query']}")
            print(f"  Top Score: {fail['top_score']:.2f}")
            print(f"  Reason: {fail['reason']}\n")

if __name__ == '__main__':
    main()
