from django.forms import ValidationError
from django.test import TestCase
from .services import PatientServices
from hms.domain.user.test import UserModelTestCase
from hms.domain.patient.models import Patient, PatientFactory
from hms.application.patient.services import PatientAppServices
from hms.utils.custom_exceptions import EditPatientException
from faker import Faker

fake = Faker()


class PatientModelTestCase(TestCase):
    """Patient model test case"""

    def setUp(self):
        self.user = UserModelTestCase
        self.patient_factory = PatientFactory()
        self.patient_services = PatientServices()
        self.patient_app_services = PatientAppServices()
        self.patient_model = Patient
        self.user_obj = self.user.setUp(self)
        self.user_obj.is_patient = True
        self.user_obj.save()
        self.patient_create = self.patient_factory.build_entity_with_id(
            dob=fake.date(),
            gender=fake.random_choices(elements=["MALE", "FEMALE", "OTHER"]),
            address=fake.address(),
            user=self.user_obj
            )
        self.patient_create.save()
        self.patient_id = self.patient_create.id
        return self.patient_create

    def test_create_patient_factory(self):
        """Test Case on patient Model to test Create patient with build entity"""
        patient_obj = self.patient_factory.build_entity_with_id(
            dob=fake.date(),
            gender=fake.random_choices(elements=["MALE", "FEMALE", "OTHER"]),
            address=fake.address(),
            user=self.user_obj,
        )
        patient_obj.save()
        self.assertTrue(isinstance(patient_obj, self.patient_model))

    def test_create_patient(self):
        """Test Case on patient Model to test Create patient"""
        
        patient_create = self.patient_factory.build_entity_with_id(
            dob=fake.date(),
            gender=fake.random_choices(elements=["MALE", "FEMALE", "OTHER"]),
            address=fake.address(),
            user=self.user_obj
            )
        self.assertTrue(isinstance(patient_create, self.patient_model))

    def test_negative_create_patient(self):
        """Negative Test Case on patient Model to test Create patient"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            
            patient_create = self.patient_factory.build_entity_with_id(
            dob=fake.name(),
            gender=fake.random_choices(elements=["MALE", "FEMALE", "OTHER"]),
            address=fake.address(),
           
            )
            self.assertTrue(isinstance(patient_create, self.patient_model))

    def test_get_patient(self):
        """Test Case on patient Model to test get patient"""
        patient_obj = self.patient_app_services.get_patient_by_pk(pk=self.patient_id)
        self.assertTrue(isinstance(patient_obj, self.patient_model))

    def test_negative_get_patient(self):
        """Negative Test Case on patient Model to test get patient"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError, EditPatientException)
        ):
            patient_obj = self.patient_app_services.get_patient_by_pk(pk=fake.name())
            self.assertTrue(isinstance(patient_obj, self.patient_model))

    def test_update_patient(self):
        """Test Case on patient Model to test Update patient"""
        patient_update = self.patient_app_services.get_patient_by_pk(pk=self.patient_id)
        current_patient = patient_update.user.name
        patient_update.user.name = fake.name()
        patient_update.save()
        self.assertNotEqual(patient_update, current_patient)

    def test_negative_update_patient(self):
        """Negative Test Case on patient Model to test Update patient"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError, EditPatientException)
        ):
            patient_obj = self.patient_app_services.get_patient_by_pk(pk=fake.name())
            updated_patient_obj = patient_obj.dob
            patient_obj.dob = "abc"
            patient_obj.save()
            self.assertNotEqual(updated_patient_obj, self.patient_model)

    def test_delete_patient(self):
        """Test Case on patient Model to test Delete patient"""
        patient_obj = self.patient_app_services.get_patient_by_pk(pk=self.patient_id)
        patient_obj.delete()
        get_patient = self.patient_services.get_patient_repo().filter(pk=self.patient_id)
        self.assertEqual(get_patient.__len__(), 0)

    def test_negative_delete_patient(self):
        """Negative Test Case on patient Model to test Delete patient"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError, EditPatientException)
        ):
            patient_obj = self.patient_app_services.get_patient_by_pk(pk=fake.name())
            patient_obj.delete()
            get_patient = self.patient_services.get_patient_repo().filter(pk=self.patient_id)
            self.assertEqual(get_patient.__len__(), 0)
