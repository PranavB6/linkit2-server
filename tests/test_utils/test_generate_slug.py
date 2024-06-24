from linkit2.utils import generate_random_slug


class TestGenerateSlugUtil:
    def test_basic(self):
        slug = generate_random_slug()

        assert len(slug) == 5
        assert slug.islower()
        assert slug.isalpha()
