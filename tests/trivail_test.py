from fastapi.testclient import TestClient
from app.main import app  # Assuming your FastAPI app is defined in a file named main.py

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}  # Assuming your root endpoint returns this message
