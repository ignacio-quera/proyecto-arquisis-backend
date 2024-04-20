<<<<<<< HEAD
def test_always_fails():
    assert False, "This test always fails"
=======
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}
>>>>>>> 057a9df (CI changed test structure)
