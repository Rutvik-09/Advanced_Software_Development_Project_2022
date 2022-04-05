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

class BlogModelTest(SimpleTestCase):

    def test_blogs(self):
        client = Client()
        response = client.get('/blogs/')
        self.assertEqual(response.url, '/login/')

    def test_blog_with_id(self):
        client = Client()
        response = client.get('/blog/1')
        self.assertEqual(response.url, '/login/')

    def test_edit_blog(self):
        client = Client()
        response = client.get('/edit-blog/1')
        self.assertEqual(response.url, '/login/')

class ExpenseModelTest(SimpleTestCase):

    def test_delete_expense(self):
        client = Client()
        response = client.get('/delete-cost/1')
        self.assertEqual(response.url, '/login/')

    def test_edit_expenses(self):
        client = Client()
        response = client.get('/edit-cost/1')
        self.assertEqual(response.url, '/login/')

    def test_view_expenses(self):
        client = Client()
        response = client.get('/view-expenses/')
        self.assertEqual(response.url, '/login/')

    def test_cost_manager_view(self):
        client = Client()
        response = client.get('/cost-manager/')
        self.assertEqual(response.url, '/login/')

class ChartModelTest(SimpleTestCase):

    def test_charts(self):
        client = Client()
        response = client.get('/analytics/')
        self.assertEqual(response.url, '/login/')


class SearchAPITest(SimpleTestCase):

    def test_search(self):
        client = Client()
        response = client.post('/search-api/')
        self.assertEqual(response.url, '/login/')


class InventoryTest(SimpleTestCase):

    def test_view_inventory(self):
        client = Client()
        response = client.get('/view-inventory/')
        self.assertEqual(response.url, '/login/')

