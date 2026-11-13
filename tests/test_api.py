
import os

os.environ.setdefault("GROQ_API_KEY", "test-key")

from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_health_endpoint():

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_invalid_email():

    response = client.post(
        "/api/generate",
        json={
            "email": "Hi",
            "tone": "professional",
            "length": "medium"
        }
    )

    assert response.status_code == 422
