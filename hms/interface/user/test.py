from django.forms import ValidationError
from faker import Faker
from django.contrib.auth.hashers import make_password
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import force_authenticate
from hms.domain.user.models import User

from .views import UserViewSet

fake = Faker()


class TestUserView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.user_view_set = UserViewSet
        cls.user_login_view = cls.user_view_set.as_view({"post": "login"})
        cls.email = fake.email()
        cls.user_name = fake.first_name()
        cls.name  = fake.name()
        cls.contact_no = fake.phone_number()
        cls.test_password = make_password("Test@123")
        cls.user_data = dict(email=cls.email, username=cls.user_name, name= cls.name, contact_no  = cls.contact_no)
        cls.test_user = User.objects.create(**cls.user_data)
        cls.test_user.set_password(cls.test_password)
        cls.test_user.save()

    def test_login(self):
        """
        Test-case method on UserViewSet to login test.
        """
        data = dict(email=self.user_name, password=self.test_password)
        request = self.factory.post("/api/v0/user/login/", data)
        force_authenticate(request, user=self.test_user)
        response = self.user_login_view(request)
        print(response.data, "========= res data............")
        response_keys = response.data.keys()
        response_data_keys = response.data["data"].keys()
        self.assertEqual(response.data["success"], True)
        self.assertIn("refresh", response_data_keys)
        self.assertIn("access", response_data_keys)
        self.assertIn("message", response_keys)
        self.assertIn("success", response_keys)
        self.assertIn("data", response_keys)
                                                 

    def test_negative_login(self):
        """
        Negative Test-case method on UserViewSet to login test.
        """
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            data = dict(email=self.user_name, password="123")
            request = self.factory.post("/api/v0/login/", data)
            response = self.user_login_view(request)
            response_keys = response.data.keys()
            response_data_keys = response.data["data"].keys()
            self.assertEqual(response.data["success"], True)
            self.assertIn("refresh", response_data_keys)
            self.assertIn("access", response_data_keys)
            self.assertIn("message", response_keys)
            self.assertIn("success", response_keys)
            self.assertIn("data", response_keys)
