from django.forms import ValidationError
from django.test import TestCase
from .services import AppointmentServices
from hms.domain.doctor.test import DoctorModelTestCase
from hms.domain.patient.test import PatientModelTestCase
from hms.application.appointment.services import AppointmentAppServices
from hms.domain.appointment.models import (
    Appointment,
    AppointmentFactory,
)
from hms.utils.custom_exceptions import EditAppointmentException
from faker import Faker

fake = Faker()


class AppointmentTestCase(TestCase):
    """Appointment model test case"""

    def setUp(self):
        self.doctor = DoctorModelTestCase
        self.patient = PatientModelTestCase
        self.appointment_factory = AppointmentFactory()
        self.appointment_services = AppointmentServices()
        self.appointment_app_service = AppointmentAppServices()
        self.appointment_model = Appointment
        self.doctor_obj = self.doctor.setUp(self)
        self.patient_obj = self.patient.setUp(self)        
        self.appointment_create = self.appointment_factory.build_entity_with_id(
             doctor=self.doctor_obj,
            patient=self.patient_obj,
            appointment_date=fake.date_object(),
            purpose=fake.paragraph(nb_sentences=2)
        )
        self.appointment_create.save()
        self.appointment_id = self.appointment_create.id
        return super().setUp()

    def test_create_appointment_factory(self):
        """Test Case on appointment Model to test Create appointment with build entity"""
        appointment_obj = self.appointment_factory.build_entity_with_id(
            doctor=self.doctor_obj,
            patient=self.patient_obj,
            appointment_date=fake.date_object(),
            purpose=fake.paragraph(nb_sentences=2)
        )
        appointment_obj.save()
        self.assertTrue(isinstance(appointment_obj, self.appointment_model))

    def test_create_appointment(self):
        """Test Case on appointment Model to test Create appointment"""
        
        appointment_create = self.appointment_factory.build_entity_with_id(
            doctor=self.doctor_obj,
            patient=self.patient_obj,
            appointment_date=fake.date_object(),
            purpose=fake.paragraph(nb_sentences=2)
        )
        appointment_create.save()
        self.assertTrue(isinstance(appointment_create, self.appointment_model))

    def test_negative_create_appointment(self):
        """Negative Test Case on appointment Model to test Create appointment"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            appointment_create =  self.appointment_factory.build_entity_with_id(
            doctor=self.doctor_obj,
            patient=self.patient_obj,
            purpose=fake.paragraph(nb_sentences=2)
        )
            self.assertTrue(isinstance(appointment_create, self.appointment_model))

    def test_get_appointment(self):
        """Test Case on appointment Model to test get appointment"""
        appointment_obj = self.appointment_app_service.get_appointment_by_pk(pk=self.appointment_id, user=self.patient_obj.user)
        self.assertTrue(isinstance(appointment_obj, self.appointment_model))

    def test_negative_get_appointment(self):
        """Negative Test Case on appointment Model to test get appointment"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError, EditAppointmentException)
        ):
            appointment_obj = self.appointment_app_service.get_appointment_by_pk(pk="sdlkfjho234uyehn", user=self.patient_obj.user)
            self.assertTrue(isinstance(appointment_obj, self.appointment_model))

    def test_update_appointment(self):
        """Test Case on appointment Model to test update appointment"""
        appointment_update = self.appointment_app_service.get_appointment_by_pk(pk=self.appointment_id, user=self.patient_obj.user)
        current_appointment = appointment_update.appointment_date
        appointment_update.appointment_date = fake.date_object()
        appointment_update.save()
        self.assertNotEqual(appointment_update, current_appointment)

    def test_negative_update_appointment(self):
        """Negative Test Case on appointment Model to test update appointment"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            appointment_update = self.appointment_app_service.get_appointment_by_pk(pk=self.appointment_id, user=self.patient_obj.user)
            current_appointment = appointment_update.appointment_date
            appointment_update.appointment_date = fake.paragraph()
            appointment_update.save()
            self.assertNotEqual(appointment_update, current_appointment)

    def test_delete_appointment(self):
        """Test Case on appointment Model to test delete appointment"""
        appointment_obj = self.appointment_app_service.get_appointment_by_pk(pk=self.appointment_id, user=self.patient_obj.user)
        appointment_obj.delete()
        get_appointment = self.appointment_services.get_appointment_repo().filter(pk=self.appointment_id)
        self.assertEqual(get_appointment.__len__(), 0)

    def test_negative_delete_appointment(self):
        """Negative Test Case on appointment Model to test delete appointment"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError, EditAppointmentException)
        ):
            appointment_obj = self.appointment_app_service.get_appointment_by_pk(pk="lsdkfrewiuojlkdfslkj", user=self.patient_obj.user)
            appointment_obj.delete()
            get_appointment = self.appointment_services.get_appointment_repo().filter(pk=self.appointment_id)
            self.assertEqual(get_appointment.__len__(), 0)
