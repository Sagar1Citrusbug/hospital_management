from .views import AppointmentViewSet

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"appointment", AppointmentViewSet, basename="appointment")
