from src.template_py_pdm.linkit_config import LinkitEnvironment, get_linkit_config


class TestLinkitConfig:
    def test_basic(self):
        config = get_linkit_config()

        assert config is not None

    def test_env(self):
        config = get_linkit_config()

        assert config.env == LinkitEnvironment.TEST
