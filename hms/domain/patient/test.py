from django.forms import ValidationError
from django.test import TestCase
from hms.domain.user.test import UserModelTestCase
from hms.domain.patient.models import Patient, PatientFactory
from faker import Faker

fake = Faker()


class PatientModelTestCase(TestCase):
    """Patient model test case"""

    def setUp(self):
        self.user = UserModelTestCase
        self.patient_factory = PatientFactory()
        self.patient_model = Patient
        self.user_obj = self.user.setUp(self)
        patient_data = dict(
          
            dob=fake.date(),
            gender=fake.random_choices(elements=["MALE", "FEMALE", "OTHER"]),
            address=fake.address(),
            user=self.user_obj,
        )
        self.patient_create = Patient.objects.create(**patient_data)
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
        patient_data = dict(
             dob=fake.date(),
            gender=fake.random_choices(elements=["MALE", "FEMALE", "OTHER"]),
            address=fake.address(),
            user=self.user_obj,
        )
        patient_create = Patient.objects.create(**patient_data)
        self.assertTrue(isinstance(patient_create, self.patient_model))

    def test_negative_create_patient(self):
        """Negative Test Case on patient Model to test Create patient"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            data = dict(
                dob="sdlkfjslw89",
                gender=fake.random_choices(elements=["MALE", "FEMALE", "OTHER"]),
                user=self.user_obj,
            )
            patient_create = Patient.objects.create(**data)
            self.assertTrue(isinstance(patient_create, self.patient_model))

    def test_get_patient(self):
        """Test Case on patient Model to test get patient"""
        patient_obj = Patient.objects.get(id=self.patient_id)
        self.assertTrue(isinstance(patient_obj, self.patient_model))

    def test_negative_get_patient(self):
        """Negative Test Case on patient Model to test get patient"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            patient_obj = Patient.objects.get(id="mitarth")
            self.assertTrue(isinstance(patient_obj, self.patient_model))

    def test_update_patient(self):
        """Test Case on patient Model to test Update patient"""
        patient_update = Patient.objects.get(id=self.patient_id)
        current_patient = patient_update.user.name
        patient_update.user.name = fake.name()
        patient_update.save()
        self.assertNotEqual(patient_update, current_patient)

    def test_negative_update_patient(self):
        """Negative Test Case on patient Model to test Update patient"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            patient_obj = Patient.objects.get(id=self.patient_id)
            updated_patient_obj = patient_obj.dob
            patient_obj.dob = "abc"
            patient_obj.save()
            self.assertNotEqual(updated_patient_obj, self.patient_model)

    def test_delete_patient(self):
        """Test Case on patient Model to test Delete patient"""
        patient_obj = Patient.objects.get(id=self.patient_id)
        patient_obj.delete()
        get_patient = Patient.objects.filter(id=self.patient_id)
        self.assertEqual(get_patient.__len__(), 0)

    def test_negative_delete_patient(self):
        """Negative Test Case on patient Model to test Delete patient"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            patient_obj = Patient.objects.get(id="skldjfl93909")
            patient_obj.delete()
            get_patient = Patient.objects.filter(id=self.patient_id)
            self.assertEqual(get_patient.__len__(), 0)
