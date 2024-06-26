from fastapi.testclient import TestClient

from linkit2.linkit_settings import get_linkit_settings
from linkit2.main import app
from linkit2.mongodb import MongoDB

client = TestClient(app)


class TestMain:
    def setup_class(self):
        self.client = TestClient(app)

        settings = get_linkit_settings()
        self.mongodb = MongoDB(settings.mongodb)

    def setup_method(self):
        self.mongodb.delete_database()

    def test_read_main(self):
        response = self.client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello World"}
