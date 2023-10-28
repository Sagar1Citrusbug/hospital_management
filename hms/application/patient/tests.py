from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth.hashers import make_password
from hms.application.patient.services import PatientAppServices
from hms.domain.patient.models import Patient
from hms.domain.user.services import UserServices
from hms.domain.patient.services import PatientServices

from faker import Faker

fake = Faker()


class PatientServicesTestCase(TestCase):
    """Patient services test case"""

    def setUp(self) -> None:
        self.patient_app_services = PatientAppServices()
        self.user_services = UserServices()
        self.patients_services = PatientServices()
        self.patient_model = Patient
        self.user_data = dict(
          name = fake.name(), contact_no = fake.phone_number() ,  username=fake.first_name(), email=fake.email(), password=make_password(fake.password())
        )
        self.user = self.user_services.get_user_repo().create(**self.user_data)
        patient_data = dict(
            dob=fake.date_object(),
            gender=fake.random_choices(elements=["MALE", "FEMALE", "OTHER"]),
            address=fake.address(),
            user=self.user,
        )
        self.patient_create = self.patients_services.get_patient_repo().create(
            **patient_data
        )
        return self.patient_create

    def test_create_patient_from_dict(self):
        """create patient from dict in services test case"""

        data = dict(
            dob=fake.date_object(),
            gender=fake.random_choices(elements=["MALE", "FEMALE", "OTHER"]),
            address=fake.address(),
            user=self.user,
            username=fake.first_name(),
            email=fake.email(),
            password=fake.password(),
        )
        patient = self.patient_app_services.create_patient_from_dict(data=data)
        self.assertTrue(isinstance(patient, self.patient_model))

    def test_negative_create_patient_from_dict(self):
        """Negative create patient from dict in services test case"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            try:
                data = dict(
                    name=fake.name(),
                    date_of_birth=fake.date(),
                    contact_number=fake.phone_number(),
                    gender=fake.random_choices(elements=["male", "female", "other"]),
                    address=fake.address(),
                    user=self.user,
                    username=fake.name(),
                    email="",
                    password=fake.password(),
                )
                patient = self.patient_app_services.create_patient_from_dict(data=data)
                self.assertTrue(isinstance(patient, self.patient_model))
            except:
                raise ValueError("Invalid value")

    def test_list_patients(self):
        """get list of patients in services test case"""
        patients = self.patient_app_services.list_patients()
        self.assertIn(self.patient_create, patients)

    def test_get_patient_by_pk(self):
        """get patient by pk in services test case"""

        pk = self.patient_create.id
        patient = self.patient_app_services.get_patient_by_pk(pk=pk)
        self.assertTrue(isinstance(patient, self.patient_model))

    def test_negative_get_patient_by_pk(self):
        """Negative get patient by pk in services test case"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            try:
                pk = "sdfsdfsrw"
                patient = self.patient_app_services.get_patient_by_pk(pk=pk)
                self.assertTrue(isinstance(patient, self.patient_model))
            except:
                raise TypeError("Invalid id")

    def test_edit_patient_by_dict(self):
        """edit patient by pk in services test case"""

        data = dict(
            dob=fake.date_object(),
            contact_no=fake.phone_number(),
            gender=fake.random_choices(elements=["MALE", "FEMALE", "OTHER"]),
            address=fake.address(),
        )
        pk = self.patient_create.id
        patient = self.patient_app_services.edit_patient_by_dict(pk=pk, data=data)
        self.assertTrue(isinstance(patient, self.patient_model))

    def test_negative_edit_patient_by_pk(self):
        """Negative get edit by pk in services test case"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            try:
                data = dict(
                    dob=fake.date_object(),
                    contact_no=fake.phone_number(),
                    gender=fake.random_choices(elements=["MALE", "FEMALE", "OTHER"]),
                    address=fake.address(),
                )
                pk = "sldkfjlr09"
                patient = self.patient_app_services.edit_patient_by_dict(
                    pk=pk, data=data
                )
                self.assertTrue(isinstance(patient, self.patient_model))
            except:
                raise TypeError("Invalid id")

    def test_delete_patient__by_pk(self):
        """patient delete by pk in services test case"""

        pk = self.patient_create.id
        self.patient_app_services.delete_patient_by_pk(pk=pk)
        get_doctor = self.patients_services.get_patient_repo()
        self.assertEqual(get_doctor.filter(id=pk).__len__(), 0)

    def test_negative_delete_patient_by_pk(self):
        """Negative delete patient by pk in services test case"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            try:
                pk = "sdfljw3p"
                patient = self.patient_app_services.delete_patient_by_pk(pk=pk)
                self.assertFalse(patient.is_active)
            except:
                raise TypeError("Invalid id")
