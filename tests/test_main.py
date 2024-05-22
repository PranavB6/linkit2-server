from fastapi.testclient import TestClient

from linkit2.main import app
from linkit2.models.link_record import LinkRecordInMongoDB

client = TestClient(app)


class TestMain:
    def setup_class(self):
        self.client = TestClient(app)

    def test_read_main(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}

    def test_check_health_live(self):
        response = self.client.get("/health/live")
        assert response.status_code == 200
        assert response.json() == {"status": "LIVE"}

    def test_check_health_db(self):
        response = self.client.get("/health/db")
        assert response.status_code == 200
        assert response.json() == {"db": "CONNECTED"}

    def test_shorten_link(self):
        response = self.client.post(
            "/links", json={"original_url": "https://example.com"}
        )

        assert response.status_code == 200
        assert LinkRecordInMongoDB.model_validate(response.json())
