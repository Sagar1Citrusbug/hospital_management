from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action

from .serializer import (
    PatientSerializer,
    PatientCreateSerializer,
    PatientEditSerializer,
)
from hms.application.patient.services import PatientAppServices
from hms.utils.user_permissions import IsPatient, IsStaff, IsSuperUser
from hms.utils.custom_exceptions import (
    PatientCreationException,
    EditPatientException,
    DeletePatientException,
)

from hms.utils.pagination import Pagination
from hms.utils.custom_response import CustomResponse


class PatientViewSet(viewsets.ViewSet):
    """PatientViewSet for create, update, delete and list Patient"""

    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, (IsSuperUser | IsStaff))
    pagination_class = Pagination

    patients_app_services = PatientAppServices()

    def get_serializer_class(self):
        if self.action == "add":
            return PatientCreateSerializer
        if self.action == "all":
            return PatientSerializer
        if self.action == "get":
            return PatientSerializer
        if self.action == "delete":
            return PatientSerializer
        return PatientEditSerializer

    @action(detail=False, methods=["post"], name="add")
    def add(self, request):
        """This method will create Patient by dict"""

        serializer = self.get_serializer_class()
        serializer_obj = serializer(data=request.data)

        if serializer_obj.is_valid():
            try:
                patient_obj = self.patients_app_services.create_patient_from_dict(
                    data=serializer_obj.data
                )
                if patient_obj:
                    response = PatientSerializer(patient_obj)
                    return CustomResponse(
                        data=response.data,
                        message="You have created patient successfully",
                    )
            except PatientCreationException as e:
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
        serializer = self.get_serializer_class()
        queryset = self.patients_app_services.list_patients()
        paginator = self.pagination_class()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializer_obj = serializer(paginated_queryset, many=True)
        paginated_data = paginator.get_paginated_response(serializer_obj.data).data
        message = "Successfully listed all patients."
        return CustomResponse(data=paginated_data, message=message)

    @action(detail=True, methods=["get"], name="get")
    def get(self, request, pk=None):
        """This method will get patient by pk"""
        get_serializer = self.get_serializer_class()
        try:
            patient_obj = self.patients_app_services.get_patient_by_pk(pk=pk)
            response = get_serializer(patient_obj)
            return CustomResponse(
                data=response.data, message="Successfully get patient."
            )
        except EditPatientException as e:
            return CustomResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=e.item,
            )

    @action(detail=True, methods=["patch"], name="edit")
    def edit(self, request, pk=None):
        serializer = self.get_serializer_class()
        serializer_obj = serializer(data=request.data)
        if serializer_obj.is_valid():
            try:
                patient_obj = self.patients_app_services.edit_patient_by_dict(
                    data=serializer_obj.data, pk=pk
                )
                patient = PatientSerializer(patient_obj)
                return CustomResponse(
                    data=patient.data, message="You have Edited patient successfully"
                )
            except EditPatientException as e:
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
        """This method will delete patient by pk"""
        try:
            patient_obj = self.patients_app_services.delete_patient_by_pk(pk=pk)
            response = PatientSerializer(patient_obj)
            return CustomResponse(
                data=response.data, message="You have deleted successfully"
            )
        except DeletePatientException as e:
            return CustomResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                message=e.item,
            )
