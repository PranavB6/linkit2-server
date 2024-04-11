from linkit2.linkit_config import get_linkit_config
from linkit2.models.link_record import LinkRecord
from linkit2.mongodb import MongoDB


def main():
    print("Hello World!")
    config = get_linkit_config()
    mongodb = MongoDB(config.mongodb)
    mongodb.test_connection()

    inserted = mongodb.insert_link_record(LinkRecord(url="https://www.google.com"))

    print(f"Inserted: {inserted}")

    records = mongodb.get_all_link_records()

    for record in records:
        print(mongodb.get_link_record_by_id(record.id))


if __name__ == "__main__":
    main()
