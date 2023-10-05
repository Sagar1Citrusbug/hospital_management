from django.contrib.auth import authenticate
from rest_framework import viewsets
from hms.application.user.services import UserAppServices
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from hms.utils.custom_response import CustomResponse
from .serializers import UserSerializer, UserLoginSerializer
from hms.utils.custom_exceptions import UserLoginException, UserLogoutException


class UserLoginView(viewsets.ViewSet):
    """
    API endpoint that allows users to login.
    """

    def get_serializer_class(self):
        if self.action == "sign_up":
            return UserRegistrationSerializer
        if self.action == "login":
            return UserLoginSerializer
        return UserSerializer


    @action(detail=False, methods=["post"], name="sign_up")
    @access_control()
    def sign_up(self, request):
        serializer = self.get_serializer_class()
        serializer_data = serializer(data=request.data)
        if serializer_data.is_valid():
            try:
                user_data = UserAppServices(log=self.log).create_user_from_dict(
                    data=serializer_data.data
                )
                serialized_user_data = UserSerializer(
                    instance=user_data,
                    context={
                        "log": self.log,
                    },
                )
                return APIResponse(
                    status_code=status.HTTP_201_CREATED,
                    data=serialized_user_data.data,
                    message=f"Successfully sign-up for user.",
                )
            except UserSignUpException as use:
                return APIResponse(
                    status_code=use.status_code,
                    errors=use.error_data(),
                    message=f"An error occurred while Sign-up.",
                    for_error=True,
                )
            except UserAlreadyExistsException as uae:
                return APIResponse(
                    status_code=uae.status_code,
                    errors=uae.error_data(),
                    message=f"User already exists",
                    for_error=True,
                )
            except MailNotSendException as uae:
                return APIResponse(
                    status_code=uae.status_code,
                    errors=uae.error_data(),
                    message="Mail not sent.",
                    for_error=True,
                )
            except Exception as e:
                return APIResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    errors=e.args,
                    for_error=True,
                    general_error=True,
                )
        return APIResponse(
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
                return CustomResponse().success(data=response_data, message=message)
            except UserLoginException as e:
                message = "Invalid Credentials"
                return CustomResponse().fail(
                    status=status.HTTP_400_BAD_REQUEST,
                    errors=e.error_data(),
                    message=message,
                )
            except Exception as e:
                return CustomResponse().fail(
                    status=status.HTTP_400_BAD_REQUEST,
                    errors=str(e.args),
                    message="An error occurred while Login.",
                )
        return CustomResponse().fail(
            status=status.HTTP_400_BAD_REQUEST,
            errors=serializer_obj.errors,
            message=serializer_obj.errors,
        )

class UserLogoutView(viewsets.ViewSet):
    """
    API endpoint that allows users to logout.
    """

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    @action(detail=False, methods=["post"])
    def logout(self, request):
        try:
            UserAppServices().logout_user(user=self.request.user)
            return CustomResponse().success(
                data=None,
                message="Successfully logout",
            )
        except UserLogoutException as e:
            return CustomResponse().fail(
                status=status.HTTP_400_BAD_REQUEST,
                errors=e.error_data(),
                message="An error occurred while logout.",
            )
