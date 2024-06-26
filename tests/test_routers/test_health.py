from enum import Enum

from fastapi.testclient import TestClient

from linkit2.linkit_settings import get_linkit_settings
from linkit2.main import app
from linkit2.mongodb import MongoDB

client = TestClient(app)


class HealthEndpoints(str, Enum):
    live = "/health/live"
    db = "/health/db"


class TestHealthRouter:
    def setup_class(self):
        self.client = TestClient(app)

        settings = get_linkit_settings()
        self.mongodb = MongoDB(settings.mongodb)

    def setup_method(self):
        self.mongodb.delete_database()

    def test_health_liveness(self):
        response = self.client.get(HealthEndpoints.live)
        assert response.status_code == 200
        assert response.json() == {"status": "LIVE"}

    def test_health_db(self):
        response = self.client.get(HealthEndpoints.db)
        assert response.status_code == 200
        assert response.json() == {"db": "CONNECTED"}
