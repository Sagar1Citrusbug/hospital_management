from hms.interface.user.views import UserLoginView, UserLogoutView
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r"", UserLoginView, basename="login")
router.register(r"", UserLogoutView, basename="logout")
