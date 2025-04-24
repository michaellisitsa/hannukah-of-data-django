from django.test import TestCase, Client
from app.models import Customer


# Create your tests here.
class TestViews(TestCase):
    # https://docs.djangoproject.com/en/5.2/howto/initial-data/
    fixtures = ["customers.json"]

    def setUp(self) -> None:
        return super().setUp()

    def test_fixture_loaded(self):
        self.assertEqual(Customer.objects.all().count(), 2)

    def test_day01_request(self):
        c = Client()
        response = c.get("/day01/")
        self.assertHTMLEqual(
            response.content.decode("utf-8"), "<div>John adi 234 VIC</div>"
        )
