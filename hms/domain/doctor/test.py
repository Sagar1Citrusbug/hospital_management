from django.forms import ValidationError
from django.test import TestCase
from .services import DoctorServices
from hms.domain.user.test import UserModelTestCase
from hms.domain.doctor.models import Doctor, DoctorFactory
from hms.application.doctor.services import DoctorAppServices
from faker import Faker

fake = Faker()


class DoctorModelTestCase(TestCase):
    """Doctor model test case"""

    def setUp(self):
        self.user = UserModelTestCase
        self.doctor_factory = DoctorFactory()
        self.doctor_service = DoctorServices
        self.doctor_app_service = DoctorAppServices
        self.doctor_model = Doctor
        self.user_obj = self.user.setUp(self)
        self.doctor_create = self.doctor_factory.build_entity_with_id(
             specialization=fake.name(),
            user=self.user_obj,
        )
        self.doctor_create.save()
        self.doctor_id = self.doctor_create.id
        return self.doctor_create

    def test_create_doctor_factory(self):
        """Test Case on doctor Model to test Create doctor with build entity"""
        doctor_obj = self.doctor_factory.build_entity_with_id(
            specialization=fake.name(),
            user=self.user_obj,
        )
        doctor_obj.save()
        self.assertTrue(isinstance(doctor_obj, self.doctor_model))

    def test_create_doctor(self):
        """Test Case on doctor Model to test Create doctor"""
        doctor_data = dict(
            specialization=fake.name(),
            user=self.user_obj,
        )
        doctor_create = Doctor.objects.create(**doctor_data)
        self.assertTrue(isinstance(doctor_create, self.doctor_model))

    def test_negative_create_doctor(self):
        """Negative Test Case on doctor Model to test Create doctor"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            data = dict(
                specialization=fake.name(),
                user=fake.name(),
            )
            doctor_create = Doctor.objects.create(**data)
            self.assertTrue(isinstance(doctor_create, self.doctor_model))

    def test_get_doctor(self):
        """Test Case on doctor Model to test get doctor"""
        doctor_obj = Doctor.objects.get(id=self.doctor_id)
        self.assertTrue(isinstance(doctor_obj, self.doctor_model))

    def test_negative_get_doctor(self):
        """Negative Test Case on doctor Model to test get doctor"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            doctor_obj = Doctor.objects.get(id="fsdjkl3oiruo")
            self.assertTrue(isinstance(doctor_obj, self.doctor_model))

    def test_update_doctor(self):
        """Test Case on doctor Model to test Update doctor"""
        doctor_update = Doctor.objects.get(id=self.doctor_id)
        current_doctor = doctor_update.user.name
        doctor_update.user.name = fake.name()
        doctor_update.save()
        self.assertNotEqual(doctor_update, current_doctor)

    def test_negative_update_doctor(self):
        """Negative Test Case on doctor Model to test Update doctor"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            doctor_obj = Doctor.objects.get(id="fsioru23ojklfsdjlqer")
            updated_doctor_obj = doctor_obj.user.name
            doctor_obj.user.name = fake.name()
            doctor_obj.save()
            self.assertTrue(updated_doctor_obj, self.doctor_model)

    def test_delete_doctor(self):
        """Test Case on doctor Model to test Delete doctor"""
        doctor_obj = Doctor.objects.get(id=self.doctor_id)
        doctor_obj.delete()
        get_doctor = Doctor.objects.filter(id=self.doctor_id)
        self.assertEqual(get_doctor.__len__(), 0)

    def test_negative_delete_doctor(self):
        """Negative Test Case on doctor Model to test Delete doctor"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            doctor_obj = Doctor.objects.get(id="hello")
            doctor_obj.delete()
            get_doctor = Doctor.objects.filter(id=self.doctor_id)
            self.assertEqual(get_doctor.__len__(), 0)
