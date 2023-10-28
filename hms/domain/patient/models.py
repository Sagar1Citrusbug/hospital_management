"""This is a model module to store Patient data in to the database"""

import uuid
from dataclasses import dataclass
from django.db import models
from hms.domain.user.models import User
from hms.utils.base_models import AuditModelMixin


@dataclass(frozen=True)
class PatientID:
    value: uuid.UUID


GENDER_CHOICES = (
    ("MALE", "Male"),
    ("FEMALE", "Female"),
    ("OTHER", "Other"),
)


class Patient(AuditModelMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dob = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    address = models.CharField(max_length=250)

    def __str__(self):
        return self.user.email

    class Meta:
        db_table = "patient"


class PatientFactory:
    @staticmethod
    def build_entity(
        id: PatientID,
        dob: str,
        gender: str,
        address: str,
        user,
    ) -> Patient:
        return Patient(
            id=id.value,
            dob=dob,
            gender=gender,
            address=address,
            user=user,
        )

    @classmethod
    def build_entity_with_id(
        cls,
        dob: str,
        gender: str,
        address: str,
        user,
    ) -> Patient:
        entity_id = PatientID(uuid.uuid4())
        return cls.build_entity(
            id=entity_id,
            dob=dob,
            gender=gender,
            address=address,
            user=user,
        )

    @classmethod
    def update_entity(
        self,
        patient: Patient,
        name:str, 
        contact_no:str,
        dob: str,
        gender: str,
        address: str,
    ) -> Patient:
        if name:
            patient.user.name = name
        if contact_no:
            patient.user.contact_no = contact_no
        if dob:
            patient.dob = dob
        if gender:
            patient.gender = gender

        if address:
            patient.address = address
        return patient
