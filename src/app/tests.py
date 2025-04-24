from django.test import TestCase, Client
from app.models import Customer


# Create your tests here.
class TestViews(TestCase):
    # https://docs.djangoproject.com/en/5.2/howto/initial-data/
    fixtures = ["customers.json"]

    def setUp(self) -> None:
        self.client = Client()
        return super().setUp()

    def test_fixture_loaded(self):
        self.assertEqual(Customer.objects.all().count(), 2)

    def test_day01_request(self):
        response = self.client.get("/day01/")
        self.assertHTMLEqual(
            # adi translates to 234 on the keypad
            response.content.decode("utf-8"),
            "<div>Day01 adi 234 Melbourne, VIC, 3163</div>",
        )

    def test_day03_request(self):
        response = self.client.get("/day03/")
        self.assertHTMLEqual(
            response.content.decode("utf-8"),
            "<div>Day02 Coster 123 Jamaica, NY 11435</div>",
        )
