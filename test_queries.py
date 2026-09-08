from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

print("GET /health")
response = client.get("/health")
print(response.status_code, response.json())

queries = [
    "What is the minimum attendance requirement?",
    "What is the attendance condonation limit?",
    "Can I bring a smartwatch into the examination hall?"
]

for q in queries:
    print(f"\nQuery: {q}")
    res = client.post("/ask", json={"query": q})
    print("Status:", res.status_code)
    try:
        print("Response:", res.json())
    except:
        print("Response text:", res.text)
