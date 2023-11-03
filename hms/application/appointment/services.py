from django.db.models.manager import BaseManager
from hms.application.user.services import UserAppServices
from hms.application.doctor.services import DoctorAppServices
from hms.domain.user.models import User
from hms.application.patient.services import PatientAppServices
from hms.domain.appointment.models import Appointment
from hms.domain.appointment.services import AppointmentServices
from hms.utils.custom_exceptions import (
    AppointmentCreationException,
    EditAppointmentException,
    DeleteAppointmentException,
)


class AppointmentAppServices:
    """
    Application layer Services for Appointments.
    """

    def __init__(self) -> None:
        self.appointments_services = AppointmentServices()
        self.doctors_services = DoctorAppServices()
        self.patients_services = PatientAppServices()
        self.users_services = UserAppServices()

    def create_appointment_from_dict(self, data: dict, user: User) -> Appointment:
        """This method will return Appointment."""

        patient_id = data.get("patient_id", None)

        appointment_date = data.get("appointment_date", None)
        purpose = data.get("purpose", None)
        appointment_factory_method = (
            self.appointments_services.get_appointment_factory()
        )
        try:
            exists_appointment_obj = (
                self.appointments_services.get_appointment_repo()
                .filter(doctor__user=user, patient__id=patient_id, is_active=True)
                .exists()
            )
            if not exists_appointment_obj:
                patient = self.patients_services.list_patients().get(id=patient_id)
                doctor = self.doctors_services.list_doctors().get(user__id=user.id)
              
                appointment_obj = appointment_factory_method.build_entity_with_id(
                    appointment_date=appointment_date,
                    purpose=purpose,
                    doctor=doctor,
                    patient=patient,
                )
                appointment_obj.save()
                return appointment_obj
            raise AppointmentCreationException(
                "Appointment already exist", "with given patient"
            )
        except AppointmentCreationException as e:
            raise AppointmentCreationException(str(e), "Appointment create exception")
        except Exception as e:
            
            raise AppointmentCreationException(
                "Patient does not exist", "Appointment create exception"
            )

    def list_appointments(self, user: User) -> BaseManager[Appointment]:
        """This method will return list of Appointments."""
        if user.is_patient:
            return self.appointments_services.get_appointment_repo().filter(
                patient__user=user,
                doctor__is_active=True,
                is_active=True,
            )
        elif user.is_staff:
            return self.appointments_services.get_appointment_repo().filter(
                doctor__user=user,
                patient__is_active=True,
                is_active=True,
            )
        else:
            return (
                self.appointments_services.get_appointment_repo()
                .filter(doctor__is_active=True, patient__is_active=True, is_active=True)
                .order_by("-created_at")
            )

    def get_appointment_by_pk(self, pk: str, user: User) -> Appointment:
        """This method will return Appointment by pk."""
        try:
            return self.list_appointments(user=user).get(id=pk)
        except Exception as e:
            raise EditAppointmentException("Appointment does not exist", str(e))

    def edit_appointment_by_dict(self, pk: str, data: dict, user: User) -> Appointment:
        appointment_date = data.get("appointment_date", None)
        purpose = data.get("purpose", None)
        try:
            appointment = self.get_appointment_by_pk(pk=pk, user=user)
            if appointment:
                if appointment_date and (
                    appointment.appointment_date != appointment_date
                ):
                    appointment.appointment_date = appointment_date
                if purpose and (appointment.purpose != purpose):
                    appointment.purpose = purpose
                appointment.save()
                return appointment
        except Exception as e:
            raise EditAppointmentException("Appointment does not exist", str(e))

    def delete_appointment_by_pk(self, pk: str, user: User) -> str:
        """This method will delete Appointment."""
        try:
            appointment = self.get_appointment_by_pk(pk=pk, user=user)
            if appointment:
                appointment.delete()
                return appointment
        except Exception as e:
            raise DeleteAppointmentException(
                "Appointment does not exist or already deleted", str(e)
            )
