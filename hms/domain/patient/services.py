from django.db.models.manager import BaseManager
from hms.domain.patient.models import Patient, PatientFactory


class PatientServices:
    def get_patient_factory(
        self,
    ):
        return PatientFactory

    def get_patient_repo(self) -> BaseManager[Patient]:
        return Patient.objects
