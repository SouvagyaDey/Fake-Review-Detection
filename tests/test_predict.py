import sys
import os
import uuid
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_predict_endpoint():

    username = f"test_user_{uuid.uuid4().hex[:8]}"
    user_response = client.post(
        "/users",
        json={"username": username}
    )
    api_key = user_response.json().get("api_key")
    
    response = client.post(
        "/reviews/predict",
        headers={"X-API-Key": api_key},
        json={"review": "This product is amazing"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    assert "confidence" in data
