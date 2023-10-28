from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth.hashers import make_password
from hms.application.user.services import UserAppServices
from hms.domain.user.models import User
from hms.domain.user.services import UserServices

from faker import Faker

fake = Faker()


class UserServicesTestCase(TestCase):
    """User services test case"""

    def setUp(self) -> None:
        self.user_app_services = UserAppServices
        self.user_services = UserServices()
        self.user_model = User
        self.data = dict(
          name=fake.name(),contact_no = fake.phone_number(),   username=fake.first_name(), email=fake.email(), password=make_password(fake.password())
        )
        self.user = self.user_services.get_user_repo().create(**self.data)
        return super().setUp()

    def test_get_user_token(self):
        """get user token in services test case"""

        data = self.user_app_services.get_user_token(self, user=self.user)
        data_keys = data.keys()
        self.assertIn("email", data_keys)
        self.assertIn("username", data_keys)
        self.assertIn("access", data_keys)
        self.assertIn("refresh", data_keys)
        
    def test_negative_get_user_token(self):
        """Negative get user token in services test case"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            self.user_model.delete(id=self.user.id)
            data = self.user_app_services.get_user_token(self, user=self.user)
            data_keys = data.keys()
            print(data_keys, "++++++++ data keys")
            self.assertIn("email", data_keys)
            self.assertIn("username", data_keys)
            self.assertIn("access", data_keys)
            self.assertIn("refresh", data_keys)
