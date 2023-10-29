from django.forms import ValidationError
from django.test import TestCase

from hms.application.doctor.services import DoctorAppServices
from hms.domain.doctor.models import Doctor
from hms.domain.user.services import UserServices
from hms.domain.doctor.services import DoctorServices

from faker import Faker

fake = Faker()


class DoctorServicesTestCase(TestCase):
    """Doctor services test case"""

    def setUp(self) -> None:
        self.doctor_app_services = DoctorAppServices()
        self.user_services = UserServices()
        self.doctors_services = DoctorServices()
        self.doctor_model = Doctor
        self.user_data = dict(
            username=fake.first_name(), email=fake.email(), password=fake.password(), name = fake.name(), contact_no = fake.phone_number()
        )
        self.user = self.user_services.get_user_repo().create(**self.user_data)
        doctor_data = dict(
            specialization=fake.name(),
            user=self.user,
        )
        self.doctor_create = self.doctors_services.get_doctor_repo().create(
            **doctor_data
        )
        return self.doctor_create

    def test_create_doctor_from_dict(self):
        """create doctor from dict in services test case"""

        data = dict(
            name=fake.name(),
            specialization=fake.name(),
            contact_no=fake.phone_number(),
            username=fake.name(),
            email=fake.email(),
            password=fake.password(),
        )
        doctor = self.doctor_app_services.create_doctor_from_dict(data=data)
        self.assertTrue(isinstance(doctor, self.doctor_model))
        
    def test_negative_create_doctor_from_dict(self):
        """Negative create doctor from dict in services test case"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            try:
                data = dict(
                    name=fake.name(),
                    specialization=fake.name(),
                    contact_number=fake.phone_number(),
                    username=fake.first_name(),
                    email='notavalidemail',
                    password=fake.password(),
                )
                doctor = self.doctor_app_services.create_doctor_from_dict(data=data)
                self.assertTrue(isinstance(doctor, self.doctor_model))
            except:
                raise ValueError("Invalid Email ")

    def test_list_doctors(self):
        """get list of doctors in services test case"""

        doctors = self.doctor_app_services.list_doctors()
        self.assertIn(self.doctor_create, doctors)

    def test_get_doctor_by_pk(self):
        """get doctor by pk in services test case"""

        pk = self.doctor_create.id
        doctor = self.doctor_app_services.get_doctor_by_pk(pk=pk)
        self.assertTrue(isinstance(doctor, self.doctor_model))
        
    def test_negative_get_doctor_from_dict(self):
        """Negative get doctor from dict in services test case"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            try:
                pk = 'sdfsdfwer3'
                doctor = self.doctor_app_services.get_doctor_by_pk(pk=pk)
                self.assertTrue(isinstance(doctor, self.doctor_model))
            except:
                raise TypeError("Invalid id")

    def test_edit_doctor_by_dict(self):
        """edit doctor by pk in services test case"""

        data = dict(
            specialization=fake.name(),
            contact_number=fake.phone_number(),
        )
        pk = self.doctor_create.id
        doctor = self.doctor_app_services.edit_doctor_by_dict(pk=pk, data=data)
        self.assertTrue(isinstance(doctor, self.doctor_model))
        
    def test_negative_edit_doctor_from_dict(self):
        """Negative edit doctor from dict in services test case"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            try:
                data = dict(
                specialization=fake.name(),
                contact_number=fake.phone_number(),
                )
                pk = 'hello'
                doctor = self.doctor_app_services.edit_doctor_by_dict(pk=pk, data=data)
                self.assertTrue(isinstance(doctor, self.doctor_model))
            except:
                raise ValueError("Invalid id")

    def test_delete_doctor_by_pk(self):
        """delete doctor by pk in services test case"""

        pk = self.doctor_create.id
        doctor = self.doctor_app_services.delete_doctor_by_pk(pk=pk)
        try:
            self.doctor_app_services.get_doctor_by_pk(pk=pk)
        except :
             self.assertRaises(Doctor.DoesNotExist)

    def test_negative_delete_doctor_from_dict(self):
        """Negative delete doctor from dict in services test case"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            try:
                pk = 'sfklsdj3093u094'
                doctor = self.doctor_app_services.delete_doctor_by_pk(pk=pk)
                self.assertFalse(doctor.is_active)
            except:
                raise ValueError("Invalid id")
