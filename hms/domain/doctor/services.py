from django.db.models.manager import BaseManager
from hms.domain.doctor.models import Doctor, DoctorFactory


class DoctorServices:
    def get_doctor_factory(
        self,
    ):
        return DoctorFactory

    def get_doctor_repo(self) -> BaseManager[Doctor]:
        return Doctor.objects
