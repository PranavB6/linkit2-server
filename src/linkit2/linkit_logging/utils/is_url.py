from urllib.parse import urlparse


def is_url(string: str) -> bool:
    try:
        parse_result = urlparse(string)
        return all([parse_result.scheme, parse_result.netloc])
    except ValueError:
        return False
