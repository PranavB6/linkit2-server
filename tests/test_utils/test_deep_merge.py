from linkit2.utils import deep_merge


class TestDeepMerge:
    def test_basic(self):
        a = {"name": "Alice"}
        b = {"name": "Bob"}

        assert deep_merge(a, b) == {"name": "Bob"}
        assert deep_merge(b, a) == {"name": "Alice"}

    def test_extra_keys(self):
        a = {"name": "Alice", "age": 30}
        b = {"name": "Bob"}

        assert deep_merge(a, b) == {"name": "Bob", "age": 30}
        assert deep_merge(b, a) == {"name": "Alice", "age": 30}

    def test_nested(self):
        a = {"name": "Alice", "address": {"city": "New York"}}
        b = {"name": "Bob", "address": {"country": "USA"}}

        assert deep_merge(a, b) == {
            "name": "Bob",
            "address": {"city": "New York", "country": "USA"},
        }
        assert deep_merge(b, a) == {
            "name": "Alice",
            "address": {"city": "New York", "country": "USA"},
        }
