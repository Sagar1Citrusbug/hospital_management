"""This is a model module to store Appointment data in to the database"""

import uuid

from dataclasses import dataclass
from django.db import models

from hms.domain.doctor.models import Doctor
from hms.domain.patient.models import Patient

from hms.utils.base_models import AuditModelMixin


@dataclass(frozen=True)
class AppointmentID:
    """
    This is a value object that should be used to generate and pass the
    AppointmentID to the AppointmentFactory
    """

    value: uuid.UUID


# ----------------------------------------------------------------------
# Appointment Model
# ----------------------------------------------------------------------


class Appointment(AuditModelMixin):
    """This model stores the data into Appointment table in db"""

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    purpose = models.CharField(max_length=300)

    def __str__(self):
        return self.patient.user.email

    

    class Meta:
        
        db_table = "appointment"


class AppointmentFactory:
    """This is a factory method used for build an instance of Appointment"""

    @staticmethod
    def build_entity_with_id(
        doctor: Doctor, patient: Patient, appointment_date: str, purpose: str
    ) -> Appointment:
        return Appointment(
            id=AppointmentID(uuid.uuid4()).value,
            doctor=doctor,
            patient=patient,
            appointment_date=appointment_date,
            purpose=purpose,
        )
