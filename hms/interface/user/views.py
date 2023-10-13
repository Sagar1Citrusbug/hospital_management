from django.contrib.auth import authenticate
from rest_framework import viewsets
from hms.application.user.services import UserAppServices
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from hms.utils.custom_response import CustomResponse
from .serializers import UserRegistrationSerializer, UserLoginSerializer
from hms.utils.custom_exceptions import (
    UserLoginException,
    UserLogoutException,
    UserRegistrationException,
    UserAlreadyExistsException,
)


class UserViewSet(viewsets.ViewSet):
    def get_serializer_class(self):
        if self.action == "registration":
            return UserRegistrationSerializer
        if self.action == "login":
            return UserLoginSerializer

    @action(detail=False, methods=["post"], name="registration")
    def registration(self, request):
        serializer = self.get_serializer_class()
        serializer_data = serializer(data=request.data)
        if serializer_data.is_valid():
            try:
                UserAppServices().create_user_from_dict(data=serializer_data.data)
                return CustomResponse(
                    status_code=status.HTTP_201_CREATED,
                    data=serializer_data.data,
                    message=f"user created Successfully.",
                )
            except UserRegistrationException as use:
                return CustomResponse(
                    status_code=use.status_code,
                    errors=use.error_data(),
                    message=f"An error occurred while Sign-up.",
                    for_error=True,
                )
            except UserAlreadyExistsException as uae:
                return CustomResponse(
                    status_code=uae.status_code,
                    errors=uae.error_data(),
                    message=f"User already exists",
                    for_error=True,
                )
            except Exception as e:
                return CustomResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    errors=e.args,
                    for_error=True,
                    general_error=True,
                )

        return CustomResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            errors=serializer_data.errors,
            message=f"Incorrect email or password",
            for_error=True,
        )

    @action(detail=False, methods=["post"], name="login")
    def login(self, request):
        serializer = self.get_serializer_class()
        serializer_obj = serializer(data=request.data)
        if serializer_obj.is_valid():
            email = serializer_obj.data.get("email", None)
            password = serializer_obj.data.get("password", None)

            try:
                user = authenticate(email=email, password=password)

                response_data = UserAppServices().get_user_token(user=user)
                message = "Login Successful"
                return CustomResponse(data=response_data, message=message)
            except UserLoginException as e:
                message = "Invalid Credentials"
                return CustomResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message=message,
                )
            except Exception as e:
                return CustomResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="An error occurred while Login.",
                )
        return CustomResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=serializer_obj.errors,
        )


class UserLogoutViewset(viewsets.ViewSet):
    """
    API endpoint that allows users to logout.
    """

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=["post"], name="logout")
    def logout(self, request):
        try:
            UserAppServices().logout_user(user=self.request.user)
            return CustomResponse(
                data=None,
                message="Successfully logout",
            )
        except UserLogoutException as e:
            print(e)
            return CustomResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="An error occurred while logout.",
            )
