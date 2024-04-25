import os

from linkit2.linkit_settings import LinkitEnvironment, get_linkit_settings


class TestSettings:
    def test_updating_environment(self):
        curr_environment = os.environ.get("LINKIT_ENVIRONMENT")

        assert curr_environment is not None

        os.environ["LINKIT_ENVIRONMENT"] = "test"
        settings = get_linkit_settings()
        assert settings.environment == LinkitEnvironment.TEST

        os.environ["LINKIT_ENVIRONMENT"] = "development"
        settings = get_linkit_settings()
        assert settings.environment == LinkitEnvironment.DEVELOPMENT

        os.environ["LINKIT_ENVIRONMENT"] = "production"
        settings = get_linkit_settings()
        assert settings.environment == LinkitEnvironment.PRODUCTION

        os.environ["LINKIT_ENVIRONMENT"] = curr_environment
