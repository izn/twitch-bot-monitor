from flask_testing import TestCase
from twitchbot.server import create_app
import json


class TestServerClient(TestCase):
    def create_app(self):
        return create_app()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_stream(self):
        response = self.client.get('/stream')

        try:
            json.loads(response.data)
        except ValueError:
            raise ValueError('Invalid JSON')

        self.assertEqual(response.status_code, 200)
