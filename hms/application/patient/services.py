from django.db.models.manager import BaseManager
from hms.domain.user.models import UserPersonalData
from hms.domain.user.services import UserServices
from hms.domain.patient.models import Patient
from hms.domain.patient.services import PatientServices
from django.db import transaction
from hms.utils.custom_exceptions import (
    PatientCreationException,
    EditPatientException,
    DeletePatientException,
)


class PatientAppServices:
    """
    Application layer Services for Patients.
    """

    def __init__(self) -> None:
        self.patients_services = PatientServices()
        self.user_services = UserServices()

    def create_patient_from_dict(self, data: dict) -> Patient:
        print(data)
        name = data.get("name", None)
        dob = data.get("dob", None)
        gender = data.get("gender", None)
        contact_no = data.get("contact_no", None)
        address = data.get("address", None)
        email = data.get("email", None)
        username = data.get("username", None)
        password = data.get("password", None)
        print(password, "password in create password dictionary....")
        user_personal_data = UserPersonalData(email=email, username=username)
        user_factory_method = self.user_services.get_user_factory()
        patient_factory_method = self.patients_services.get_patient_factory()
        try:
            with transaction.atomic():
                exist_user_obj = self.user_services.get_user_repo().filter(email=email)
                if exist_user_obj:
                    raise PatientCreationException(f"{username}", "already exists")
                user_obj = user_factory_method.build_entity_with_id(
                    personal_data=user_personal_data,
                    is_staff=False,
                    is_patient=True,
                )
                user_obj.set_password(password)
                print(user_obj.password, "pswd 22222 ----------------")
                user_obj.save()

                patient_obj = patient_factory_method.build_entity_with_id(
                    name=name,
                    dob=dob,
                    gender=gender,
                    contact_no=contact_no,
                    address=address,
                    user=user_obj,
                )
                patient_obj.save()
                return patient_obj
        except PatientCreationException as e:
            raise PatientCreationException(str(e), "Patient create exception")

    def list_patients(self) -> BaseManager[Patient]:
        """This method will return list of Patients."""
        return (
            self.patients_services.get_patient_repo()
            .filter(is_active=True)
            .order_by("-created_at")
        )

    def get_patient_by_pk(self, pk: str):
        try:
            return self.list_patients().get(id=pk)
        except Exception as e:
            raise EditPatientException("Patient does not exist", str(e))

    def edit_patient_by_dict(self, pk: str, data: dict) -> Patient:
        """This method will edit patient by pk."""
        name = data.get("name", None)
        dob = data.get("dob", None)
        gender = data.get("gender", None)
        contact_no = data.get("contact_no", None)
        address = data.get("address", None)
        patient_factory_method = self.patients_services.get_patient_factory()
        try:
            patient_obj = self.get_patient_by_pk(pk=pk)
            patient = patient_factory_method.update_entity(
                patient=patient_obj,
                name=name,
                dob=dob,
                gender=gender,
                contact_no=contact_no,
                address=address,
            )
            patient.save()
            return patient
        except Exception as e:
            raise EditPatientException("Patient does not exist", str(e))

    def delete_patient_by_pk(self, pk: str) -> str:
        """This method will delete Patient."""
        try:
            with transaction.atomic():
                patient = self.get_patient_by_pk(pk=pk)
                user = (
                    self.user_services.get_user_repo()
                    .filter(pk=patient.user.id)
                    .first()
                )
                patient.delete()
                user.delete()
                return patient
        except Exception as e:
            raise DeletePatientException(
                "Patient does not exist or already deleted", str(e)
            )
