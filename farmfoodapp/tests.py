from django.contrib.auth.hashers import make_password, check_password
from django.test import TestCase
from farmfoodapp.models import RegisterModel


# Create your tests here.


class RegisterModelTest(TestCase):

    def create_register(self):
        return RegisterModel.objects.create(first_name="Test",
                                            last_name="User",
                                            date_of_birth="2013-01-08",
                                            email="test@test.com",
                                            country_code="+1",
                                            phone="1234567890",
                                            user_password=make_password("test@123"))

    def test_user_login_success(self):
        reg = self.create_register()
        password = check_password("test@123", reg.user_password)
        self.assertEqual(password, True)

    def test_user_login_fail(self):
        reg = self.create_register()
        password = check_password("test@1234", reg.user_password)
        self.assertEqual(password, False)
