from faker import Faker


def generate_random_slug() -> str:
    return Faker().pystr_format(
        string_format="?????", letters="abcdefghijklmnopqrstuvwxyz"
    )
