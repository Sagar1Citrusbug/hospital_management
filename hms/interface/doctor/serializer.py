from rest_framework import serializers
from hms.domain.doctor.models import Doctor
from hms.domain.user.models import User
from django.conf import settings
import re


class UserProfileSerializer(serializers.ModelSerializer):
    """UserProfile Serializer"""

    class Meta:
        model = User
        fields = [
            "username",
        ]


class DoctorSerializer(serializers.ModelSerializer):
    """Doctor Serializer"""

    class Meta:
        model = Doctor
        fields = ["id", "user", "name", "specialization", "contact_no"]

    def to_representation(self, instance):
        self.fields["user"] = UserProfileSerializer(read_only=True)
        return super(DoctorSerializer, self).to_representation(instance)


class DoctorBaseSerializer(serializers.Serializer):
    """Doctor base create serializer"""

    name = serializers.CharField(max_length=100, required=False)
    specialization = serializers.CharField(max_length=200, required=False)
    contact_no = serializers.CharField(max_length=100, required=False)
    email = serializers.CharField(max_length=150, required=False)
    username = serializers.CharField(max_length=60, required=False)
    password = serializers.CharField(max_length=60, required=False)


class DoctorCreateSerializer(DoctorBaseSerializer):
    """Doctor create serializer"""

    name = serializers.CharField(max_length=100, required=True)
    specialization = serializers.CharField(max_length=200, required=True)
    contact_no = serializers.CharField(max_length=100, required=True)
    email = serializers.CharField(max_length=150, required=True)
    username = serializers.CharField(max_length=60, required=True)
    password = serializers.CharField(max_length=60, required=True)

    def validate_email(self, value):
        regex = re.compile(
            r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])"
        )
        if not re.fullmatch(regex, value):
            raise serializers.ValidationError("Invalid E-mail address format.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password should be 8 char long")
        return value

    def validate_name(self, value):
        if len(value) > 50:
            raise serializers.ValidationError("Name should not be more than 50 latter")
        return value

    def validate_specialization(self, value):
        if len(value) > 100:
            raise serializers.ValidationError(
                "Specialization should not be more than 100 latter"
            )
        return value

    def validate_contact_no(self, value):
        regex = re.compile(r"(^[+0-9]{1,3})*([0-9]{10,11}$)")

        if not re.fullmatch(regex, value):
            raise serializers.ValidationError("Invalid contact number")
        return value


class DoctorEditSerializer(DoctorBaseSerializer):
    """Doctor edit serializer"""

    name = serializers.CharField(max_length=100, required=False)
    specialization = serializers.CharField(max_length=100, required=False)
    contact_no = serializers.CharField(max_length=100, required=False)
    email = None
    username = None
    password = None

    def validate_name(self, value):
        if len(value) > 50:
            raise serializers.ValidationError("Name should not be more than 50 latter")
        return value

    def validate_specialization(self, value):
        if len(value) > 100:
            raise serializers.ValidationError(
                "Specialization should not be more than 100 latter"
            )
        return value

    def validate_contact_no(self, value):
        regex = re.compile(r"(^[+0-9]{1,3})*([0-9]{10,11}$)")

        if not re.fullmatch(regex, value):
            raise serializers.ValidationError("Invalid contact number")
        return value
