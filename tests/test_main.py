from fastapi.testclient import TestClient

from linkit2.main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}


def test_check_health_live():
    response = client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "LIVE"}


def test_check_health_db():
    response = client.get("/health/db")
    assert response.status_code == 200
    assert response.json() == {"db": "CONNECTED"}
