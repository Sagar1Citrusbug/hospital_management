from .views import PatientViewSet

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"patient", PatientViewSet, basename="patient")
