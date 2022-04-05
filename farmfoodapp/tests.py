from django.test import Client, SimpleTestCase

# Create your tests here.
from farmfoodapp.actions import create_token, decode_token, send_forget_pass_email, send_verification_email


class RegisterModelTest(SimpleTestCase):

    def test_register_view_GET(self):
        client = Client()
        response = client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_login_view_GET(self):
        client = Client()
        response = client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_forget_password(self):
        client = Client()
        response = client.get('/forget-password/')
        self.assertEqual(response.status_code, 200)

    def test_login_api(self):
        client = Client()
        response = client.get('/login-api/')
        self.assertEqual(response.status_code, 200)
