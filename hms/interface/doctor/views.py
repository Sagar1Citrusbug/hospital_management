from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from hms.application.doctor.services import DoctorAppServices

from hms.utils.pagination import Pagination
from hms.utils.user_permissions import IsSuperUser
from .serializer import DoctorSerializer, DoctorCreateSerializer, DoctorEditSerializer
from hms.utils.custom_exceptions import (
    DoctorCreationException,
    DoctorEditException,
    DeleteDoctorException,
)

from hms.utils.custom_response import CustomResponse


@extend_schema(tags=["doctors"], responses={200: DoctorSerializer})
class DoctorViewSet(viewsets.ViewSet):
    """DoctorsViewSet for create, update, delete and list Doctor"""

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsSuperUser)
    pagination_class = Pagination

    doctors_app_services = DoctorAppServices()

    def get_serializer_class(self):
        if self.action == "add":
            return DoctorCreateSerializer
        if self.action == "all":
            return DoctorSerializer
        if self.action == "get":
            return DoctorSerializer
        if self.action == "delete":
            return DoctorSerializer
        return DoctorEditSerializer

    @action(detail=False, methods=["post"], name="add")
    def add(self, request):
        """This method will create Doctor by dict"""

        serializer = self.get_serializer_class()
        serializer_obj = serializer(data=request.data)
        if serializer_obj.is_valid():
            try:
                doctor_obj = self.doctors_app_services.create_doctor_from_dict(
                    data=serializer_obj.data
                )
                response = DoctorSerializer(doctor_obj)
                return CustomResponse().success(
                    data=response.data,
                    message="You have created doctor successfully",
                )
            except DoctorCreationException as e:
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
        """This method will return list of Doctors"""
        serializer = self.get_serializer_class()
        queryset = self.doctors_app_services.list_doctors()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer_obj = serializer(paginated_queryset, many=True)
        paginated_data = paginator.get_paginated_response(serializer_obj.data).data
        message = "Successfully listed all doctors."
        return CustomResponse(data=paginated_data, message=message)

    @action(detail=True, methods=["get"], name="get")
    def get(self, request, pk=None):
        """This method will get doctor by pk"""
        get_serializer = self.get_serializer_class()
        try:
            doctor_obj = self.doctors_app_services.get_doctor_by_pk(pk=pk)
            response = get_serializer(doctor_obj)
            return CustomResponse(
                data=response.data, message="Successfully get doctor."
            )
        except DoctorEditException as e:
            return CustomResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=e.item,
            )

    @action(detail=True, methods=["patch"], name="edit")
    def edit(self, request, pk=None):
        """This method will edit doctor by pk"""
        serializer = self.get_serializer_class()
        serializer_obj = serializer(data=request.data)
        if serializer_obj.is_valid():
            try:
                doctor_obj = self.doctors_app_services.edit_doctor_by_dict(
                    data=serializer_obj.data, pk=pk
                )
                doctor = DoctorSerializer(doctor_obj)
                return CustomResponse(
                    data=doctor.data, message="You have updated doctor successfully"
                )
            except DoctorEditException as e:
                return CustomResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message=e.item,
                )
        return CustomResponse(
            status=status.HTTP_400_BAD_REQUEST,
            message=serializer_obj.errors,
        )

    @action(detail=True, methods=["delete"], name="delete")
    def delete(self, request, pk=None):
        """This method will delete doctor by pk"""
        try:
            doctor_obj = self.doctors_app_services.delete_doctor_by_pk(pk=pk)
            response = DoctorSerializer(doctor_obj)
            return CustomResponse(
                data=response.data, message="You have deleted successfully"
            )
        except DeleteDoctorException as e:
            return CustomResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=e.item,
            )
