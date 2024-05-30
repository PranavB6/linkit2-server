import pytest


def test_assertion():
    assert 1 == 1


def test_exception():
    with pytest.raises(Exception):
        raise Exception("This is an exception")
