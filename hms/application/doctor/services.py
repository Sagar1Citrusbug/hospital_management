from django.db.models.manager import BaseManager
from hms.domain.doctor.models import Doctor
from hms.domain.doctor.services import DoctorServices
from hms.domain.user.models import UserPersonalData
from hms.domain.user.services import UserServices
from django.db import transaction
from hms.utils.custom_exceptions import (
    DoctorCreationException,
    DoctorEditException,
    DeleteDoctorException,
)


class DoctorAppServices:
    """
    Application layer Services for Doctors.
    """

    def __init__(self) -> None:
        self.doctors_services = DoctorServices()
        self.user_services = UserServices()

    def create_doctor_from_dict(self, data: dict) -> Doctor:
        """This method will return doctor."""

        name = data.get("name", None)
        specialization = data.get("specialization", None)
        contact_no = data.get("contact_no", None)
        email = data.get("email", None)
        username = data.get("username", None)
        password = data.get("password", None)
        user_personal_data = UserPersonalData(email=email, username=username, name=name, contact_no=contact_no)
        user_factory_method = self.user_services.get_user_factory()
        doctor_factory_method = self.doctors_services.get_doctor_factory()
        try:
            with transaction.atomic():
                exist_user_obj = self.user_services.get_user_repo().filter(
                    email=email
                )
                if exist_user_obj:
                    raise DoctorCreationException(f"{email}", "already exists")
                user_obj = user_factory_method.build_entity_with_id(
                    
                    personal_data=user_personal_data,
                    is_staff=True,
                    is_patient=False,
                )
                user_obj.set_password(password)
                user_obj.save()
                doctor_obj = doctor_factory_method.build_entity_with_id(
                    specialization=specialization,
                    user=user_obj,
                )
                doctor_obj.save()
                return doctor_obj
        except DoctorCreationException as e:
            raise DoctorCreationException(str(e), "Doctor create exception")

    def list_doctors(self) -> BaseManager[Doctor]:
        """This method will return list of Doctors."""
        return (
            self.doctors_services.get_doctor_repo()
            .filter(is_active=True)
            .order_by("-created_at")
        )

    def get_doctor_by_pk(self, pk: str) -> Doctor:
        """This method will return doctor by pk."""
        try:
            return self.list_doctors().get(id=pk)
        except Exception as e:
            raise DoctorEditException("Doctor does not exist", str(e))

    def edit_doctor_by_dict(self, pk: str, data: dict) -> Doctor:
        """This method will edit doctor by pk."""
        name = data.get("name", None)
        specialization = data.get("specialization", None)
        contact_no = data.get("contact_no", None)
        doctor_factory_method = self.doctors_services.get_doctor_factory()
        try:
            doctor_obj = self.get_doctor_by_pk(pk=pk)
            doctor = doctor_factory_method.update_entity(
                doctor=doctor_obj,
                name=name,
                specialization=specialization,
                contact_no=contact_no,
            )
            doctor.save()
            return doctor
        except Exception as e:
            raise DoctorEditException("Doctor does not exist", str(e))

    def delete_doctor_by_pk(self, pk: str) -> str:
        """This method will delete doctor."""
        try:
            with transaction.atomic():
                doctor = self.get_doctor_by_pk(pk=pk)
                user = (
                    self.user_services.get_user_repo().filter(pk=doctor.user.id).first()
                )
                doctor.delete()
                user.delete()
                return doctor
        except Exception as e:
            raise DeleteDoctorException(
                "Doctor does not exist or already deleted", str(e)
            )
