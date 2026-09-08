from fastapi.testclient import TestClient
from app.main import app
import app.llm as llm

client = TestClient(app)

queries = [
    "What is the minimum attendance requirement?",
    "What happens if I miss an exam due to a medical emergency?",
    "What is the attendance condonation limit?",
    "Can I bring a smartwatch into the examination hall?"
]

for q in queries:
    print(f"\nQuery: {q}")
    print(f"Current LLM_MODEL: {llm.LLM_MODEL}")
    res = client.post("/ask", json={"query": q})
    print("Status:", res.status_code)
    try:
        print("Response:", res.json())
    except:
        print("Response text:", res.text)
