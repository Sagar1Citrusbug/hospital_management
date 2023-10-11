from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from hms.application.appointment.services import AppointmentAppServices

from hms.domain.appointment.models import Appointment
from hms.utils.pagination import Pagination
from hms.utils.user_permissions import IsSuperUser, IsStaff, IsPatient
from .serializer import (
    AppointmentSerializer,
    AppointmentCreateSerializer,
    AppointmentEditSerializer,
)
from hms.utils.custom_exceptions import (
    AppointmentCreationException,
    EditAppointmentException,
    DeleteAppointmentException,
)

from hms.utils.custom_response import CustomResponse


class AppointmentViewSet(viewsets.ViewSet):
    """DoctorsViewSet for create, update, delete and list Doctor"""

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = Pagination

    appointments_app_services = AppointmentAppServices()

    def get_serializer_class(self):
        if self.action == "add":
            return AppointmentCreateSerializer
        if self.action == "all":
            return AppointmentSerializer
        if self.action == "get":
            return AppointmentSerializer
        if self.action == "delete":
            return AppointmentSerializer
        return AppointmentEditSerializer

    @action(detail=False, methods=["post"], name="add")
    def add(self, request):
        """This method will create Appointment by dict"""

        serializer = self.get_serializer_class()
        serializer_obj = serializer(data=request.data)
        if serializer_obj.is_valid():
            try:
                appointment_obj = (
                    self.appointments_app_services.create_appointment_from_dict(
                        data=serializer_obj.data, user=request.user
                    )
                )
                response = AppointmentSerializer(appointment_obj)
                return CustomResponse(
                    data=response.data,
                    message="You have created appointment successfully",
                )
            except AppointmentCreationException as e:
                return CustomResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message=e.item,
                )
        return CustomResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=serializer_obj.errors,
        )

    @action(detail=False, methods=["get"], name="all")
    def all(self, request):
        """This method will return list of Appointments"""
        serializer = self.get_serializer_class()
        queryset = self.appointments_app_services.list_appointments(
            user=self.request.user
        )
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer_obj = serializer(paginated_queryset, many=True)
        paginated_data = paginator.get_paginated_response(serializer_obj.data).data
        message = "Successfully listed all appointments."
        return CustomResponse(data=paginated_data, message=message)

    @action(detail=True, methods=["get"], name="get")
    def get(self, request, pk=None):
        """This method will get Appointment by pk"""
        get_serializer = self.get_serializer_class()
        try:
            appointment_obj = self.appointments_app_services.get_appointment_by_pk(
                pk=pk, user=self.request.user
            )
            response = get_serializer(appointment_obj)
            return CustomResponse(
                data=response.data, message="Successfully get appointment."
            )
        except EditAppointmentException as e:
            return CustomResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=e.item,
            )

    @action(detail=True, methods=["patch"], name="edit")
    def edit(self, request, pk=None):
        """This method will edit Appointment by pk"""
        serializer = self.get_serializer_class()
        serializer_obj = serializer(data=request.data)
        if serializer_obj.is_valid():
            try:
                appointment_obj = (
                    self.appointments_app_services.edit_appointment_by_dict(
                        data=serializer_obj.data, user=self.request.user, pk=pk
                    )
                )
                appointment = AppointmentSerializer(appointment_obj)
                return CustomResponse(
                    data=appointment.data,
                    message="You have updated appointment successfully",
                )
            except EditAppointmentException as e:
                return CustomResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message=e.item,
                )
        return CustomResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=serializer_obj.errors,
        )

    @action(detail=True, methods=["delete"], name="delete")
    def delete(self, request, pk=None):
        """This method will delete Appointment by pk"""
        try:
            appointment_obj = self.appointments_app_services.delete_appointment_by_pk(
                pk=pk, user=self.request.user
            )
            response = AppointmentSerializer(appointment_obj)
            return CustomResponse(
                data=response.data, message="You have deleted successfully"
            )
        except DeleteAppointmentException as e:
            return CustomResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=e.item,
            )
