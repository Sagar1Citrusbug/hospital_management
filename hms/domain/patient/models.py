"""This is a model module to store Patient data in to the database"""

import uuid

from dataclasses import dataclass
from django.db import models

from hms.domain.user.models import User
from hms.utils.base_models import AuditModelMixin


@dataclass(frozen=True)
class PatientID:
    """
    This is a value object that should be used to generate and pass the
    PatientID to the PatientFactory
    """

    value: uuid.UUID


GENDER_CHOICES = (
    ("MALE", "Male"),
    ("FEMALE", "Female"),
    ("OTHER", "Other"),
)

# ----------------------------------------------------------------------
# Patient Model
# ----------------------------------------------------------------------


class Patient(AuditModelMixin):
   

    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.user.email


    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"
        db_table = "patient"


class PatientFactory:
    """This is a factory method used for build an instance of Patient"""

    @staticmethod
    def build_entity(
        id: PatientID,
        name: str,
        date_of_birth: str,
        gender: str,
        contact_number: str,
        address: str,
        user,
    ) -> Patient:
        return Patient(
            id=id.value,
            name=name,
            date_of_birth=date_of_birth,
            gender=gender,
            contact_number=contact_number,
            address=address,
            user=user,
        )

    @classmethod
    def build_entity_with_id(
        cls,
        name: str,
        date_of_birth: str,
        gender: str,
        contact_number: str,
        address: str,
        user,
    ) -> Patient:
        entity_id = PatientID(uuid.uuid4())
        return cls.build_entity(
            id=entity_id,
            name=name,
            date_of_birth=date_of_birth,
            gender=gender,
            contact_number=contact_number,
            address=address,
            user=user,
        )

    @classmethod
    def update_entity(
        self,
        patient: Patient,
        name: str,
        date_of_birth: str,
        gender: str,
        contact_number: str,
        address: str,
    ) -> Patient:
        if name:
            patient.name = name
        if date_of_birth:
            patient.date_of_birth = date_of_birth
        if gender:
            patient.gender = gender
        if contact_number:
            patient.contact_number = contact_number
        if address:
            patient.address = address
        return patient
