from linkit2.utils import is_url


class TestIsUrl:
    def test_basic_is_url(self):
        assert is_url("https://www.google.com")

    def test_is_url_with_no_subdomain(self):
        assert is_url("https://google.com")

    def test_is_url_with_path(self):
        assert is_url("https://www.google.com/search")

    def test_is_url_with_query_params(self):
        assert is_url("https://www.google.com?q=python")

    def test_is_url_with_fragment(self):
        assert is_url("https://www.google.com#top")

    def test_is_url_with_port(self):
        assert is_url("https://www.google.com:8080")

    def test_is_url_with_port_and_path(self):
        assert is_url("https://www.google.com:8080/search")

    def test_is_url_with_port_and_path_and_query_params(self):
        assert is_url("https://www.google.com:8080/search?q=python")

    def test_is_url_with_port_and_path_and_query_params_and_fragment(self):
        assert is_url("https://www.google.com:8080/search?q=python#top")

    def test_is_url_with_ftp(self):
        assert is_url("ftp://www.google.com")

    def test_is_url_with_ftp_and_path(self):
        assert is_url("ftp://www.google.com/search")

    def test_is_url_with_ftp_and_query_params(self):
        assert is_url("ftp://www.google.com?q=python")

    def test_is_url_with_ftp_and_fragment(self):
        assert is_url("ftp://www.google.com#top")

    def test_is_url_with_ftp_and_port(self):
        assert is_url("ftp://www.google.com:8080")

    def test_is_url_with_ftp_and_port_and_path(self):
        assert is_url("ftp://www.google.com:8080/search")

    def test_is_url_with_ftp_and_port_and_query_params(self):
        assert is_url("ftp://www.google.com:8080/search?q=python")

    def test_is_url_with_ftp_and_port_and_fragment(self):
        assert is_url("ftp://www.google.com:8080/search?q=python#top")

    def test_is_url_with_ftp_and_port_and_path_and_query_params(self):
        assert is_url("ftp://www.google.com:8080/search?q=python")

    def test_is_url_with_ftp_and_port_and_path_and_fragment(self):
        assert is_url("ftp://www.google.com:8080/search?q=python#top")

    def test_is_url_with_ftp_and_port_and_query_params_and_fragment(self):
        assert is_url("ftp://www.google.com:8080/search?q=python#top")

    def test_is_url_with_ftp_and_port_and_path_and_query_params_and_fragment(self):
        assert is_url("ftp://www.google.com:8080/search?q=python#top")

    def test_is_url_with_random_protocol(self):
        assert is_url("random://www.google.com")

    def test_is_url_with_random_string(self):
        assert not is_url("random_string")

    def test_is_url_with_empty_string(self):
        assert not is_url("")

    def test_is_url_with_localhost(self):
        assert is_url("http://localhost")

    def test_is_url_with_no_scheme(self):
        assert not is_url("www.google.com")

    def test_is_url_with_no_netloc(self):
        assert not is_url("https://")

    def test_is_url_with_no_scheme_and_no_netloc(self):
        assert not is_url("://")

    def test_is_url_with_no_scheme_and_no_subdomain(self):
        assert not is_url("google.com")
