from django.forms import ValidationError
from django.test import TestCase
from hms.domain.user.models import User, UserPersonalData, UserFactory
from faker import Faker
from django.contrib.auth.hashers import make_password
fake = Faker()


class UserModelTestCase(TestCase):
    """User model test case"""

    def setUp(self):
        self.user_factory = UserFactory()
        self.user_model = User
        data = dict(
            name=fake.first_name(),
            username=fake.name(),
            email=fake.email(),
            contact_no=fake.phone_number(),
        )
        self.user_create = User.objects.create(**data)
        self.user_create.password = make_password(fake.password())
        self.user_id = self.user_create.id
        return self.user_create

    def test_create_user_factory(self):
        """Test Case on User Model to test Create User with build entity"""
        personal_data = UserPersonalData(
            username=fake.first_name(),
            email=fake.email(),
            name=fake.name(),
            contact_no=fake.phone_number(),
        )
        user_obj = self.user_factory.build_entity_with_id(
            personal_data=personal_data,
          
            is_patient=fake.pybool(),
        )
        user_obj.password = make_password(fake.password())
        user_obj.save()
        self.assertTrue(isinstance(user_obj, self.user_model))

    def test_create_user(self):
        """Test Case on User Model to test Create User"""
        data = dict(
            username=fake.name(),
            email=fake.email(),
            name=fake.name(),
            contact_no=fake.phone_number(),
           
            is_patient=fake.pybool(),
        )
        user_create = User.objects.create(**data)
        user_create.password = make_password(fake.password())
        user_create.save()
        self.assertTrue(isinstance(user_create, self.user_model))

    def test_negative_create_user(self):
            """Negative Test Case on User Model to test Create User"""
       
            data = dict(
                name=fake.name(),
                contact_no=fake.phone_number(),
                username=fake.first_name(),
                email=fake.email(),
              
            )
            user_create = User.objects.create(**data)
            user_create.password = make_password(fake.password())
            user_create.save()
            self.assertTrue(isinstance(user_create, self.user_model))

    def test_get_user(self):
        """Test Case on User Model to test get User"""
        user_obj = User.objects.get(id=self.user_id)
        self.assertTrue(isinstance(user_obj, self.user_model))

    def test_negative_get_user(self):
        """Negative Test Case on User Model to test get User"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            user_obj = User.objects.get(id="hello")
            self.assertTrue(isinstance(user_obj, self.user_model))

    def test_update_user(self):
        """Test Case on User Model to test Update User"""
        user_update = User.objects.get(id=self.user_id)
        current_user = user_update.username
        user_update.username = fake.first_name()
        user_update.save()
        self.assertNotEqual(user_update, current_user)

    def test_negative_update_user(self):
        """Negative Test Case on User Model to test Update User"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            user_obj = User.objects.get(id="mitarth")
            updated_user_obj = user_obj.email
            user_obj.email = "sagar"
            user_obj.save()
            self.assertNotEqual(updated_user_obj, self.user_model)

    def test_delete_user(self):
        """Test Case on User Model to test Delete User"""
        user_obj = User.objects.get(id=self.user_id)
        user_obj.delete()
        get_user = User.objects.filter(id=self.user_id)
        self.assertEqual(get_user.__len__(), 0)

    def test_negative_delete_user(self):
        """Negative Test Case on User Model to test Delete User"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            user_obj = User.objects.get(id="sagar")
            user_obj.delete()
            get_user = User.objects.filter(id=self.user_id)
            self.assertEqual(get_user.__len__(), 0)