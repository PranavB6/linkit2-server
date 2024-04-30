import datetime

from faker import Faker

from linkit2.models.link_record import LinkRecord

fake = Faker()


class LinkRecordBuilder:
    def __init__(self):
        self.link_record_dict = {
            "original_url": fake.url(),
            "created_at": datetime.datetime.now(datetime.timezone.utc).replace(
                microsecond=0
            ),
            "access": {
                "last_accessed_at": fake.future_datetime(
                    tzinfo=datetime.timezone.utc
                ).replace(microsecond=0),
                "access_count": fake.random_int(),
            },
            "expiry": {
                "expires_at": fake.future_datetime(
                    tzinfo=datetime.timezone.utc
                ).replace(microsecond=0),
                "max_access_count": fake.random_int(),
            },
        }

    def __repr__(self):
        return f"LinkRecordBuilder({self.link_record_dict})"

    def build(self) -> LinkRecord:
        return LinkRecord.model_validate(self.link_record_dict)
