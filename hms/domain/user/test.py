from django.forms import ValidationError
from django.test import TestCase
from hms.domain.user.models import User, UserPersonalData, UserFactory
from hms.application.user.services import UserServices 
from faker import Faker
from django.contrib.auth.hashers import make_password
fake = Faker()


class UserModelTestCase(TestCase):
    """User model test case"""

    def setUp(self):
        self.user_factory = UserFactory()
        self.user_services = UserServices()
        self.user_personal_data = UserPersonalData
        self.user_model = User
      
        self.user_create = self.user_factory.build_entity_with_id(self.user_personal_data(
            name=fake.first_name(),
            username=fake.first_name(),
            email=fake.email(),
            contact_no=fake.phone_number()
            ))
        
        self.user_create.password = make_password(fake.password())
        self.user_create.save()
        self.user_id = self.user_create.id
        return self.user_create

    def test_create_user_factory(self):
        """Test Case on User Model to test Create User with build entity"""
     
        user_obj = self.user_factory.build_entity_with_id(
            personal_data=self.user_personal_data(name=fake.first_name(),
            username=fake.first_name(),
            email=fake.email(),
            contact_no=fake.phone_number()
            )
            
        )
        user_obj.password = make_password(fake.password())
        user_obj.save()
        self.assertTrue(isinstance(user_obj, self.user_model))

    def test_create_user(self):
        """Test Case on User Model to test Create User"""
        
        user_create = self.user_factory.build_entity_with_id(self.user_personal_data(name=fake.first_name(),
            username=fake.first_name(),
            email=fake.email(),
            contact_no=fake.phone_number()
            ))
        user_create.password = make_password(fake.password())
        user_create.save()
        self.assertTrue(isinstance(user_create, self.user_model))

    def test_negative_create_user(self):
            """Negative Test Case on User Model to test Create User"""
       
       
            user_create = self.user_factory.build_entity_with_id(self.user_personal_data(name=fake.first_name(),
            username=fake.first_name(),
            email=fake.email(),
            contact_no=fake.phone_number()
            ))
            user_create.password = make_password(fake.password())
            user_create.save()
            self.assertTrue(isinstance(user_create, self.user_model))

    def test_get_user(self):
        """Test Case on User Model to test get User"""
        user_obj = self.user_services.get_user_by_id(id=self.user_id)
        self.assertTrue(isinstance(user_obj, self.user_model))

    def test_negative_get_user(self):
        """Negative Test Case on User Model to test get User"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            user_obj = self.user_services.get_user_by_id("sdlfkjsfowiru09u")
            self.assertTrue(isinstance(user_obj, self.user_model))

    def test_update_user(self):
        """Test Case on User Model to test Update User"""
        user_update = self.user_services.get_user_by_id(id=self.user_id)
        current_user = user_update.username
        user_update.username = fake.first_name()
        user_update.save()
        self.assertNotEqual(user_update, current_user)

    def test_negative_update_user(self):
        """Negative Test Case on User Model to test Update User"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            user_obj = self.user_services.get_user_by_id("sdlfkjsfowiru09u")
            updated_user_obj = user_obj.email
            user_obj.email = "sagar"
            user_obj.save()
            self.assertNotEqual(updated_user_obj, self.user_model)

    def test_delete_user(self):
        """Test Case on User Model to test Delete User"""
        user_obj = self.user_services.get_user_by_id(id=self.user_id)
        user_obj.delete()
        get_user =  self. user_services.get_user_repo().filter(id=self.user_id)
        self.assertEqual(get_user.__len__(), 0)

    def test_negative_delete_user(self):
        """Negative Test Case on User Model to test Delete User"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            user_obj = self.user_services.get_user_by_id("sdlfkjsfowiru09ufsdffs")
            user_obj.delete()
            get_user = self. user_services.get_user_repo().filter(id=self.user_id)
            self.assertEqual(get_user.__len__(), 0)