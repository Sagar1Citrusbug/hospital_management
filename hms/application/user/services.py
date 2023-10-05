from rest_framework_simplejwt.tokens import (
    RefreshToken,
    OutstandingToken,
    BlacklistedToken,
)
from hms.domain.user.models import User
from hms.domain.user.services import UserServices
from hms.utils.custom_exceptions import UserLoginException, UserLogoutException


class UserAppServices:
    """
    Application layer Services for user.
    """

    def __init__(self) -> None:
        self.user_services = UserServices()

    def get_user_token(self, user: User) -> dict:
        """This method will generate refresh and access token for user."""
        try:
            token = RefreshToken.for_user(user)
            data = dict(
                id=user.id,
                email=user.email,
                username=user.username,
                is_staff=user.is_staff,
                is_patient=user.is_patient,
                created_at=user.created_at,
                updated_at=user.updated_at,
                is_active=user.is_active,
                access=str(token.access_token),
                refesh=str(token),
            )
            return data
        except Exception as e:
            raise UserLoginException("Invalid-Credentials", str(e))

    def logout_user(self, user: User) -> bool:
    
        try:
            tokens = OutstandingToken.objects.filter(user_id=user)
            for token in tokens:
                t, _ = BlacklistedToken.objects.get_or_create(token=token)
            return True
        except Exception as e:
            raise UserLogoutException(str(e), "User not exist")
