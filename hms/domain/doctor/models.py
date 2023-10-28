import uuid
from dataclasses import dataclass
from django.db import models
from hms.domain.user.models import User
from hms.utils.base_models import AuditModelMixin


@dataclass(frozen=True)
class DoctorID:
    value: uuid.UUID


class Doctor(AuditModelMixin):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"
        db_table = "doctor"


class DoctorFactory:
    @staticmethod
    def build_entity_with_id(
       specialization: str, user: User
    ) -> Doctor:
        return Doctor(
            id=DoctorID(uuid.uuid4()).value,
            specialization=specialization,
            user=user,
        )

    @classmethod
    def update_entity(
        self,
        doctor: Doctor,
        specialization: str,
    ) -> Doctor:
       
        if specialization:
            doctor.specialization = specialization
       
        return doctor
