from hms.interface.user.views import UserViewSet, UserLogoutViewset
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r"user", UserViewSet, basename="user")
# router.register(r"", UserRegistrationView, basename="registration")
# router.register(r"", UserLoginView, basename="login")
router.register(r"user", UserLogoutViewset, basename="logout")
