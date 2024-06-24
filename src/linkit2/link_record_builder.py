import datetime
from typing import Optional, Self

from faker import Faker

from linkit2.models.link_record import LinkRecord
from linkit2.utils import generate_random_slug, now

fake = Faker()


def future_datetime() -> datetime.datetime:
    datetime_start = now() + datetime.timedelta(days=1)
    datetime_end = datetime_start + datetime.timedelta(days=30)

    return fake.date_time_between_dates(
        datetime_start=datetime_start,
        datetime_end=datetime_end,
        tzinfo=datetime.timezone.utc,
    ).replace(microsecond=0)


class LinkRecordBuilder:
    def __init__(self):
        self.link_record_dict = {
            "original_url": fake.url(),
            "slug": generate_random_slug(),
            "created_at": now(),
            "access": {
                "last_accessed_at": future_datetime(),
                "access_count": 0,
            },
            "expiry": {
                "expires_at": future_datetime(),
                "max_access_count": fake.random_int(min=1, max=10),
            },
        }

    def __repr__(self):
        return f"LinkRecordBuilder({self.link_record_dict})"

    def with_slug(self, slug: str) -> Self:
        self.link_record_dict["slug"] = slug

        return self

    def with_access(
        self,
        last_accessed_at: Optional[datetime.datetime] = None,
        access_count: Optional[int] = None,
    ) -> Self:
        if last_accessed_at is not None:
            assert isinstance(self.link_record_dict["access"], dict)
            self.link_record_dict["access"]["last_accessed_at"] = last_accessed_at

        if access_count is not None:
            assert isinstance(self.link_record_dict["access"], dict)
            self.link_record_dict["access"]["access_count"] = access_count

        return self

    def with_expiry(
        self,
        expires_at: Optional[datetime.datetime] = None,
        max_access_count: Optional[int] = None,
    ) -> Self:
        if expires_at is not None:
            assert isinstance(self.link_record_dict["expiry"], dict)
            self.link_record_dict["expiry"]["expires_at"] = expires_at

        if max_access_count is not None:
            assert isinstance(self.link_record_dict["expiry"], dict)
            self.link_record_dict["expiry"]["max_access_count"] = max_access_count

        return self

    def build(self) -> LinkRecord:
        return LinkRecord.model_validate(self.link_record_dict)
