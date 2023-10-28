from django.forms import ValidationError
from django.test import TestCase
from hms.domain.doctor.test import DoctorModelTestCase
from hms.domain.patient.test import PatientModelTestCase
from hms.domain.appointment.models import (
    Appointment,
    AppointmentFactory,
)
from faker import Faker

fake = Faker()


class AppointmentTestCase(TestCase):
    """Appointment model test case"""

    def setUp(self):
        self.doctor = DoctorModelTestCase
        self.patient = PatientModelTestCase
        self.appointment_factory = AppointmentFactory()
        self.appointment_model = Appointment
        self.doctor_obj = self.doctor.setUp(self)
        self.patient_obj = self.patient.setUp(self)
        appointment_data = dict(
            doctor=self.doctor_obj,
            patient=self.patient_obj,
            appointment_date=fake.date_object(),
            purpose=fake.paragraph(nb_sentences=2)
        )
        self.appointment_create = Appointment.objects.create(**appointment_data)
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
        appointment_data = dict(
            doctor=self.doctor_obj,
            patient=self.patient_obj,
            appointment_date=fake.date_object(),
             purpose=fake.paragraph(nb_sentences=2)
        )
        appointment_create = Appointment.objects.create(**appointment_data)
        self.assertTrue(isinstance(appointment_create, self.appointment_model))

    def test_negative_create_appointment(self):
        """Negative Test Case on appointment Model to test Create appointment"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            appointment_data = dict(
                doctor=self.doctor_obj,
                patient=self.patient_obj,
                appointment_date=fake.name(),
                 purpose=fake.paragraph(nb_sentences=2)
            )
            appointment_create = Appointment.objects.create(**appointment_data)
            self.assertTrue(isinstance(appointment_create, self.appointment_model))

    def test_get_appointment(self):
        """Test Case on appointment Model to test get appointment"""
        appointment_obj = Appointment.objects.get(id=self.appointment_id)
        self.assertTrue(isinstance(appointment_obj, self.appointment_model))

    def test_negative_get_appointment(self):
        """Negative Test Case on appointment Model to test get appointment"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            appointment_obj = Appointment.objects.get(id="sdlkfjho234uyehn")
            self.assertTrue(isinstance(appointment_obj, self.appointment_model))

    def test_update_appointment(self):
        """Test Case on appointment Model to test update appointment"""
        appointment_update = Appointment.objects.get(id=self.appointment_id)
        current_appointment = appointment_update.appointment_date
        appointment_update.appointment_date = fake.date_object()
        appointment_update.save()
        self.assertNotEqual(appointment_update, current_appointment)

    def test_negative_update_appointment(self):
        """Negative Test Case on appointment Model to test update appointment"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            appointment_update = Appointment.objects.get(id=self.appointment_id)
            current_appointment = appointment_update.appointment_date
            appointment_update.appointment_date = fake.paragraph()
            appointment_update.save()
            self.assertNotEqual(appointment_update, current_appointment)

    def test_delete_appointment(self):
        """Test Case on appointment Model to test delete appointment"""
        appointment_obj = Appointment.objects.get(id=self.appointment_id)
        appointment_obj.delete()
        get_appointment = Appointment.objects.filter(id=self.appointment_id)
        self.assertEqual(get_appointment.__len__(), 0)

    def test_negative_delete_appointment(self):
        """Negative Test Case on appointment Model to test delete appointment"""
        with self.assertRaises(
            (ValidationError, NameError, ValueError, TypeError, AssertionError)
        ):
            appointment_obj = Appointment.objects.get(id="djashjfhjksdfhe")
            appointment_obj.delete()
            get_appointment = Appointment.objects.filter(id=self.appointment_id)
            self.assertEqual(get_appointment.__len__(), 0)
