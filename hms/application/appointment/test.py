from django.forms import ValidationError
from django.test import TestCase

from hms.application.doctor.test import DoctorServicesTestCase
from hms.application.patient.test import PatientServicesTestCase
from hms.application.appointment.services import AppointmentAppServices
from hms.domain.appointment.models import Appointment
from hms.domain.appointment.services import AppointmentServices

from faker import Faker

fake = Faker()


class AppointmentServicesTestCase(TestCase):
    """Appointment services test case"""

    def setUp(self) -> None:
        self.appointment_app_services = AppointmentAppServices()
        self.doctor = DoctorServicesTestCase
        self.patient = PatientServicesTestCase
        self.appointments_services = AppointmentServices()
        self.appointment_model = Appointment
        self.doctor_obj = self.doctor.setUp(self)
        self.patient_obj = self.patient.setUp(self)
        appointment_data = dict(
            doctor=self.doctor_obj,
            patient=self.patient_obj,
            appointment_date=fake.date(),
            purpose=fake.name(),
        )
        self.appointment_create = (
            self.appointments_services.get_appointment_repo().create(**appointment_data)
        )
        return super().setUp()

    def test_create_appointment_from_dict(self):
        """create appointment from dict in services test case"""
        doctor = DoctorServicesTestCase
        patient = PatientServicesTestCase
        doctor_obj = doctor.setUp(self)
        patient_obj = patient.setUp(self)
        data = dict(
            patient_id=patient_obj.id,
            appointment_date=fake.date_object(),
           purpose=fake.paragraph(nb_sentences=2)
        )
        appointment = self.appointment_app_services.create_appointment_from_dict(
            data=data, user=doctor_obj.user
        )
        self.assertTrue(isinstance(appointment, self.appointment_model))
        
    def test_negative_create_appointment_from_dict(self):
        """Negative create appointment from dict in services test case"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            try:
                doctor = DoctorServicesTestCase
                patient = PatientServicesTestCase
                doctor_obj = doctor.setUp(self)
                patient_obj = patient.setUp(self)
                data = dict(
                    patient_id=self.patient_obj.id,
                    appointment_date=fake.date(),
                    purpose=fake.name(),
                )
                appointment = self.appointment_app_services.create_appointment_from_dict(
                    data=data, user=self.doctor_obj.user
                )
                self.assertTrue(isinstance(appointment, self.appointment_model))
            except:
                raise ValueError("Invalid value")

    def test_list_appointments(self):
        """get list of appointments in services test case"""
        appointments = self.appointment_app_services.list_appointments(user=self.doctor_obj.user)
        self.assertIn(self.appointment_create, appointments)

    def test_get_appointment_by_pk(self):
        """get appointment by pk in services test case"""

        pk = self.appointment_create.id
        appointment = self.appointment_app_services.get_appointment_by_pk(
            pk=pk, user=self.doctor_obj.user
        )
        self.assertTrue(isinstance(appointment, self.appointment_model))
        
    def test_negative_get_appointment_by_pk(self):
        """Negative get appointment by pk in services test case"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            try:
                pk = 'hello'
                appointment = self.appointment_app_services.get_appointment_by_pk(pk=pk)
                self.assertTrue(isinstance(appointment, self.appointment_model))
            except:
                raise TypeError("Invalid id")

    def test_edit_appointment_by_dict(self):
        """edit appointment by pk in services test case"""

        data = dict(
            appointment_date=fake.date(),
            purpose=fake.name(),
        )
        pk = self.appointment_create.id
        appointment = self.appointment_app_services.edit_appointment_by_dict(
            pk=pk, data=data, user=self.doctor_obj.user
        )
        self.assertTrue(isinstance(appointment, self.appointment_model))
        
    def test_negative_edit_appointment_by_pk(self):
        """Negative edit appointment by pk in services test case"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            try:
                data = dict(
                    appointment_date=fake.name(),
                    purpose=fake.name(),
                )
                pk = 'hello'
                appointment = self.appointment_app_services.edit_appointment_by_dict(
                    pk=pk, data=data, user=self.doctor_obj.user
                )
                self.assertTrue(isinstance(appointment, self.appointment_model))
            except:
                raise TypeError("Invalid id")

    def test_delete_appointment_by_pk(self):
        """delete appointment by pk in services test case"""

        pk = self.appointment_create.id
        appointment = self.appointment_app_services.delete_appointment_by_pk(
            pk=pk, user=self.doctor_obj.user
        )
        try:
            self.appointment_app_services.get_appointment_by_pk(pk=pk)
        except:
            self.assertRaises(Appointment.DoesNotExist)
        
    def test_negative_delete_appointment_by_pk(self):
        """Negative delete appointment by pk in services test case"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            try:
                pk = 'dslkfjo43iurtoirjfklgjfd'
                appointment = self.appointment_app_services.delete_appointment_by_pk(
                    pk=pk, user=self.doctor_obj.user
                )
            except:
                raise TypeError("Invalid id")
