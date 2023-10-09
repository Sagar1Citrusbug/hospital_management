from .views import DoctorViewSet

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"doctor", DoctorViewSet, basename="doctor")
