import random
import string
from django.forms import ValidationError

from faker import Faker

from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import force_authenticate

from hms.domain.user.models import User
from hms.domain.doctor.models import Doctor
from hms.domain.patient.models import Patient
from hms.domain.appointment.models import Appointment

from .views import AppointmentViewSet

fake = Faker()


class TestAppointmentView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.appointment_view_set = AppointmentViewSet
        cls.appointment_add_view = cls.appointment_view_set.as_view({"post": "add"})
        cls.appointment_list_view = cls.appointment_view_set.as_view({"get": "all"})
        cls.appointment_get_view = cls.appointment_view_set.as_view({"get": "get"})
        cls.appointment_patch_view = cls.appointment_view_set.as_view({"patch": "edit"})
        cls.appointment_delete_view = cls.appointment_view_set.as_view(
            {"delete": "delete"}
        )

        cls.password = "Test@123"
        cls.user_email = fake.email()
        cls.user_name = fake.name()
        cls.user = dict(email=cls.user_email, username=cls.user_name, is_superuser=True, name = fake.name(), contact_no = fake.phone_number())
        cls.admin_user = User.objects.create(**cls.user)
        cls.admin_user.set_password(cls.password)
        cls.admin_user.save()

        cls.doctor_email = fake.email()
        cls.doctor_name = fake.name()
        cls.contact_number = "".join(random.sample(string.digits, 10))
        cls.doctor_user_data = dict(
            name = fake.name(),
            contact_no = fake.phone_number(),
            email=cls.doctor_email,
            username=cls.doctor_name,
        )
        cls.doctor_user = User.objects.create(**cls.doctor_user_data)
        cls.doctor_user.set_password(cls.password)
        cls.doctor_user.save()
        cls.doctor_data = dict(
            user=cls.doctor_user,        
            specialization=cls.doctor_name,
        )
        cls.doctor = Doctor.objects.create(**cls.doctor_data)
        cls.doctor.save()

        cls.patient_email = fake.email()
        cls.patient_name = fake.name()
        cls.dob = fake.date_object()
        cls.gender = fake.random_choices(elements=["MALE", "FEMALE", "OTHER"])
        cls.address = fake.address()
        cls.patient_user_data = dict(
            name = fake.name(),
            contact_no = fake.phone_number(),
            email=cls.patient_email,
            username=cls.patient_name,
        )
        cls.patient_user = User.objects.create(**cls.patient_user_data)
        cls.patient_user.set_password(cls.password)
        cls.patient_user.save()
        cls.patient_data = dict(
            user=cls.patient_user,
            dob=cls.dob,
            gender=cls.gender,
            address=cls.address,
        )
        cls.patient = Patient.objects.create(**cls.patient_data)
        cls.patient.save()

        cls.appointment_date = fake.date_object()
        cls.purpose = fpurpose=fake.paragraph(nb_sentences=2)
        cls.appointment_data = dict(
            doctor=cls.doctor,
            patient=cls.patient,
            appointment_date=cls.appointment_date,
            purpose=cls.purpose,
        )
        cls.appointment = Appointment.objects.create(**cls.appointment_data)
        cls.appointment.save()

    def test_add(self):
        """
        Test-case method on AppointmentViewSet to add test.
        """
        patient_email = fake.email()
        
        dob = fake.date_object()
        gender = fake.random_choices(elements=["MALE", "FEMALE", "OTHER"])
        address = fake.address()
        patient_user_data = dict(
            name = fake.name(),
            contact_no = fake.phone_number(),
            email=patient_email,
            username=fake.first_name(),
        )
        patient_user = User.objects.create(**patient_user_data)
        patient_user.set_password(self.password)
        patient_user.save()
        patient_data = dict(
            user=patient_user,            
            dob=fake.date_object(),
            gender=gender,
            address=address,
        )
        patient = Patient.objects.create(**patient_data)
        patient.save()

        appointment_date = "2024-01-01"
        purpose=fake.paragraph(nb_sentences=2)
        data = dict(
            doctor=self.doctor,
            patient_id=patient.id,
            appointment_date=appointment_date,
            purpose=purpose,
        )
        request = self.factory.post("/api/v0/appointment/add/", data)
        force_authenticate(request, user=self.doctor_user)
        response = self.appointment_add_view(request)
        response_keys = response.data.keys()
        self.assertEqual(response.data["success"], True)
        self.assertIn("message", response_keys)
        self.assertIn("data", response_keys)

    def test_all(self):
        """
        Test-case method on AppointmentViewSet to all test.
        """
        request = self.factory.get("/api/v0/appointment/all/")
        force_authenticate(request, user=self.admin_user)
        response = self.appointment_list_view(request)
        response_keys = response.data.keys()
        self.assertEqual(response.data["success"], True)
        self.assertIn("message", response_keys)
        self.assertIn("data", response_keys)

    def test_get(self):
        """
        Test-case method on AppointmentViewSet to get test.
        """
        id = self.appointment.id
        request = self.factory.get("/api/v0/appointment/")
        force_authenticate(request, user=self.patient_user)
        response = self.appointment_get_view(request, pk=id)
        response_keys = response.data.keys()
        self.assertEqual(response.data["success"], True)
        self.assertIn("message", response_keys)
        self.assertIn("data", response_keys)


    def test_edit(self):
        """
        Test-case method on AppointmentViewSet to edit test.
        """
        purpose=fake.paragraph(nb_sentences=2)
        data = dict(purpose=purpose)
        id = self.appointment.id
        request = self.factory.patch("/api/v0/appointment/", data)
        force_authenticate(request, user=self.doctor_user)
        response = self.appointment_patch_view(request, pk=id)
        response_keys = response.data.keys()
        self.assertEqual(response.data["success"], True)
        self.assertIn("message", response_keys)
        self.assertIn("data", response_keys)



    def test_delete(self):
        """
        Test-case method on AppointmentViewSet to delete test.
        """
        id = self.appointment.id
        request = self.factory.delete("/api/v0/appointment/")
        force_authenticate(request, user=self.patient_user)
        response = self.appointment_delete_view(request, pk=id)
        response_keys = response.data.keys()
        self.assertEqual(response.data["success"], True)
        self.assertIn("message", response_keys)
        self.assertIn("data", response_keys)
