from django.test import TestCase

from registration.models import User
from core.testhelpers import TestClient


class TestLogin(TestCase):

    def setUp(self):
        super().setUp()
        self.client = TestClient()
        self.url = '/api/auth/v1/login/'

        self.valid_data = {'username': 'Bob', 'password': 'pass'}
        self.user = User(username='Bob')
        self.user.set_password('pass')
        self.user.save()

    def test_success(self):
        response = self.client.post(self.url, json=self.valid_data)
        self.assertEqual(200, response.status_code)
        self.assertTrue(self.client.is_authenticated)

    def test_already_logged_in(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url, json=self.valid_data)
        self.assertEqual(406, response.status_code)

    def test_invalid_username(self):
        response = self.client.post(self.url, json={'username': 'Bob-other', 'password': 'pass'})
        self.assertEqual(403, response.status_code)
        self.assertFalse(self.client.is_authenticated)

    def test_invalid_password(self):
        response = self.client.post(self.url, json={'username': 'Bob', 'password': 'invalid'})
        self.assertEqual(403, response.status_code)
        self.assertFalse(self.client.is_authenticated)


class TestLogout(TestCase):
    def setUp(self):
        super().setUp()
        self.client = TestClient()
        self.url = '/api/auth/v1/logout/'

        self.user = User.objects.create(username='Bob')

    def test_success(self):
        self.client.force_login(self.user)
        response = self.client.post(self.url)
        self.assertEqual(200, response.status_code)
        self.assertFalse(self.client.is_authenticated)

    def test_not_logged_in(self):
        response = self.client.post(self.url)
        self.assertEqual(406, response.status_code)
