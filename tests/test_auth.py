import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_missing_api_key():
    response = client.post(
        "/reviews/predict",
        json={"review": "Nice product"}
    )
    # 422 = missing required header, 401 = invalid key
    assert response.status_code in [401, 403, 422]
