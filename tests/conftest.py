import os

import pytest


def pytest_sessionstart(session: pytest.Session):
    print("Session starting...")
    os.environ["Linkit_Environment"] = "test"
