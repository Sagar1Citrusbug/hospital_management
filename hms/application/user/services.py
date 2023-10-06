from rest_framework_simplejwt.tokens import (
    RefreshToken,
    OutstandingToken,
    BlacklistedToken,
)
from django.contrib.auth.hashers import make_password
from django.db import transaction
from hms.domain.user.models import User, UserBasePermissions, UserPersonalData
from hms.domain.user.services import UserServices
from hms.utils.custom_exceptions import UserLoginException, UserLogoutException, UserAlreadyExistsException, UserRegistrationException


class UserAppServices:
    """
    Application layer Services for user.
    """

    def __init__(self) -> None:
        self.user_services = UserServices()

    def create_user_from_dict(self, data: dict) -> User:
        """This method will create user from dict."""
        with transaction.atomic():
            email = data.get("email", None)
            username=data.get("username", None)
            password = data.get("password", None)
            user_exists = self.user_services.get_user_repo().filter(email=email)
            if user_exists:
                raise UserAlreadyExistsException(
                    "User already Exists", f"{user_exists[0].email} already exists."
                )
            user_personal_data = UserPersonalData(
          username=username, email=email
            )
           
            user_factory_method = self.user_services.get_user_factory()
            try:
                user_obj = user_factory_method.build_entity_with_id(
                    password=make_password(password),
                    personal_data=user_personal_data,
                    is_patient = data.get("is_patient"),
                    is_staff= data.get("is_staff")
                )
                user_obj.save()

                return user_obj
            except UserRegistrationException as ure:
                raise ure(
                    "user creation errror", f"with below provided data"
                )


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
