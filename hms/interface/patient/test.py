import random
import string
from django.forms import ValidationError

from faker import Faker

from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.test import force_authenticate

from hms.domain.user.models import User
from hms.domain.patient.models import Patient

from .views import PatientViewSet

fake = Faker()


class TestPatientView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.factory = APIRequestFactory()
        cls.patient_view_set = PatientViewSet
        cls.patient_add_view = cls.patient_view_set.as_view({"post": "add"})
        cls.patient_list_view = cls.patient_view_set.as_view({"get": "all"})
        cls.patient_get_view = cls.patient_view_set.as_view({"get": "get"})
        cls.patient_patch_view = cls.patient_view_set.as_view({"patch": "edit"})
        cls.patient_delete_view = cls.patient_view_set.as_view({"delete": "delete"})
        cls.user_name = fake.name()
        cls.user_contact   = "".join(random.sample(string.digits, 10))
        cls.user_email = fake.email()
        cls.username = fake.first_name()
        cls.test_password = "Test@123"
        cls.user = dict(name = cls.user_name, contact_no = cls.user_contact, email=cls.user_email, username=cls.user_name,is_superuser  = True )
        cls.admin_user = User.objects.create(**cls.user)
        cls.admin_user.set_password(cls.test_password)
        cls.admin_user.save()

        cls.patient_email = fake.email()
        cls.patient_name = fake.name()
        cls.dob = fake.date_object()
        cls.gender = fake.random_choices(elements=["MALE", "FEMALE", "OTHER"])
        cls.address = fake.address()
        cls.contact_no = "".join(random.sample(string.digits, 10))

        cls.user_data = dict(
            name = cls.patient_name,
            contact_no = cls.contact_no,
            email=cls.patient_email,
            username=cls.patient_name,
        )
        cls.test_user = User.objects.create(**cls.user_data)
        cls.test_user.set_password(cls.test_password)
        cls.test_user.save()
        cls.patient_data = dict(
            user=cls.test_user,
            gender=cls.gender,
            address=cls.address,
        )
        cls.test_patient = Patient.objects.create(**cls.patient_data)
        cls.test_patient.save()

    def test_add(self):
        """
        Test-case method on PatientViewSet to add test.
        """
        patient_email = fake.email()
        patient_name = fake.name()
        data = dict(
            email=patient_email,
            username=patient_name,
            password=self.test_password,
            name=patient_name,
            dob=self.dob,
            contact_no=self.contact_no,
            gender=self.gender,
            address=self.address,
        )
        request = self.factory.post("/api/v0/patient/add/", data)
        force_authenticate(request, user=self.admin_user)
        response = self.patient_add_view(request)
        response_keys = response.data.keys()
        
        self.assertEqual(response.data["success"], True)
        self.assertIn("message", response_keys)
        #self.assertIn("success", response_keys)
        self.assertIn("data", response_keys)

    def test_all(self):
        """
        Test-case method on PatientViewSet to all test.
        """
        request = self.factory.get("/api/v0/patient/all/")
        force_authenticate(request, user=self.admin_user)
        response = self.patient_list_view(request)
        response_keys = response.data.keys()
        self.assertEqual(response.data["success"], True)
        self.assertIn("message", response_keys)
        #self.assertIn("success", response_keys)
        self.assertIn("data", response_keys)

    def test_get(self):
        """
        Test-case method on PatientViewSet to get test.
        """
        id = self.test_patient.id
        request = self.factory.get("/api/v0/patient/")
        force_authenticate(request, user=self.admin_user)
        response = self.patient_get_view(request, pk=id)
        response_keys = response.data.keys()
        self.assertEqual(response.data["success"], True)
        self.assertIn("message", response_keys)
        #self.assertIn("success", response_keys)
        self.assertIn("data", response_keys)

    
    def test_edit(self):
        """
        Test-case method on PatientViewSet to edit test.
        """
        patient_name = fake.name()
        data = dict(name=patient_name)
        id = self.test_patient.id
        request = self.factory.patch("/api/v0/patient/", data)
        force_authenticate(request, user=self.admin_user)
        response = self.patient_patch_view(request, pk=id)
        response_keys = response.data.keys()
        self.assertEqual(response.data["success"], True)
        self.assertIn("message", response_keys)
        #self.assertIn("success", response_keys)
        self.assertIn("data", response_keys)

    

    def test_delete(self):
        """
        Test-case method on PatientViewSet to delete test.
        """
        id = self.test_patient.id
        request = self.factory.delete("/api/v0/patient/")
        force_authenticate(request, user=self.admin_user)
        response = self.patient_delete_view(request, pk=id)
        response_keys = response.data.keys()
        self.assertEqual(response.data["success"], True)
        self.assertIn("message", response_keys)
        #self.assertIn("success", response_keys)
        self.assertIn("data", response_keys)

   
