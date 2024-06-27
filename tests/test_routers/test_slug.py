from fastapi.testclient import TestClient

from linkit2.link_record_builder import LinkRecordBuilder
from linkit2.linkit_settings import get_linkit_settings
from linkit2.main import app
from linkit2.models.link_record import LinkRecordInMongoDB
from linkit2.mongodb import MongoDB

client = TestClient(app)


class TestSlugRouter:
    def setup_class(self):
        self.client = TestClient(app)

        settings = get_linkit_settings()
        self.mongodb = MongoDB(settings.mongodb)

    def setup_method(self):
        self.mongodb.delete_database()

    def test_get_available_slug(self):
        response_available_slug = self.client.get("/slug")
        available_slug = response_available_slug.json()["slug"]

        created_link_record = LinkRecordBuilder().with_slug(available_slug).build()
        self.mongodb.insert_link_record(created_link_record)

        response_link_record = self.client.get(f"/links/{available_slug}")
        link_record_from_response = LinkRecordInMongoDB.model_validate(
            response_link_record.json()
        )

        assert response_link_record.status_code == 200
        assert created_link_record.slug == link_record_from_response.slug
        assert (
            created_link_record.original_url == link_record_from_response.original_url
        )
