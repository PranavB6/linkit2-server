from time import sleep

from fastapi.testclient import TestClient

from linkit2.link_record_builder import LinkRecordBuilder
from linkit2.linkit_settings import get_linkit_settings
from linkit2.main import app
from linkit2.models.link_record import LinkRecordInMongoDB
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

    def test_find_link_with_slug(self):
        original_url = "https://example.com"

        response_shorten_link = self.client.post(
            "/links", json={"original_url": original_url}
        )
        link_record_from_shorten = LinkRecordInMongoDB.model_validate(
            response_shorten_link.json()
        )

        response_get_link_with_slug = self.client.get(
            f"/links/{link_record_from_shorten.slug}"
        )

        assert response_get_link_with_slug.status_code == 200

        link_record_from_slug = LinkRecordInMongoDB.model_validate(
            response_get_link_with_slug.json()
        )

        assert link_record_from_slug.id == link_record_from_shorten.id
        assert link_record_from_slug.original_url == original_url

    def test_find_link_with_slug_updates_access(self):
        original_url = "https://example.com"

        response_shorten_link = self.client.post(
            "/links", json={"original_url": original_url}
        )
        link_record_from_shorten = LinkRecordInMongoDB.model_validate(
            response_shorten_link.json()
        )

        sleep(1)

        response_get_link_with_slug = self.client.get(
            f"/links/{link_record_from_shorten.slug}"
        )

        assert response_get_link_with_slug.status_code == 200

        link_record_from_slug = LinkRecordInMongoDB.model_validate(
            response_get_link_with_slug.json()
        )

        assert link_record_from_slug.id == link_record_from_shorten.id
        assert (
            link_record_from_slug.access.last_accessed_at
            > link_record_from_shorten.access.last_accessed_at
        )
        assert (
            link_record_from_slug.access.access_count
            == link_record_from_shorten.access.access_count + 1
        )

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
