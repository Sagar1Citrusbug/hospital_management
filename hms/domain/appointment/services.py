from django.db.models.manager import BaseManager
from hms.domain.appointment.models import (
    Appointment,
    AppointmentFactory,
)


class AppointmentServices:
   
    def get_appointment_factory(
        self,
    ):
        return AppointmentFactory

    def get_appointment_repo(self) -> BaseManager[Appointment]:
        return Appointment.objects
