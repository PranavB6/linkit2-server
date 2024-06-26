from fastapi.testclient import TestClient

from linkit2.linkit_settings import get_linkit_settings
from linkit2.main import app
from linkit2.models.link_record import LinkRecordInMongoDB
from linkit2.mongodb import MongoDB

client = TestClient(app)


class TestStatisticsRouter:
    def setup_class(self):
        self.client = TestClient(app)

        settings = get_linkit_settings()
        self.mongodb = MongoDB(settings.mongodb)

    def setup_method(self):
        self.mongodb.delete_database()

    def test_find_link_with_id(self):
        original_url = "https://example.com"

        response_shorten_link = self.client.post(
            "/links", json={"original_url": original_url}
        )
        link_record_from_shorten = LinkRecordInMongoDB.model_validate(
            response_shorten_link.json()
        )

        response_get_link_with_id = self.client.get(
            f"/statistics/links/{link_record_from_shorten.id}"
        )

        assert response_get_link_with_id.status_code == 200

        link_record_from_id = LinkRecordInMongoDB.model_validate(
            response_get_link_with_id.json()
        )

        assert link_record_from_id.id == link_record_from_shorten.id
        assert link_record_from_id.original_url == original_url
