import re, datetime
from django.conf import settings
from rest_framework import serializers
from hms.domain.patient.models import Patient
from hms.domain.user.models import User


class UserProfileSerializer(serializers.ModelSerializer):
    """UserProfile Serializer"""

    class Meta:
        model = User
        fields = [
            "username",
        ]


class PatientSerializer(serializers.ModelSerializer):
    """Patient Serializer"""

    patient_name = serializers.SerializerMethodField()
    contact_no = serializers.SerializerMethodField()

    def get_patient_name(self, obj):
        return obj.user.name

    def get_contact_no(self, obj):
        return obj.user.contact_no

    class Meta:
        model = Patient
        fields = [
            "id",
            "user",
            "patient_name",
            "contact_no",
            "dob",
            "gender",
            "address",
        ]

    def to_representation(self, instance):
        self.fields["user"] = UserProfileSerializer(read_only=True)
        return super(PatientSerializer, self).to_representation(instance)


GENDER_CHOICES = (
    ("MALE", "Male"),
    ("FEMALE", "Female"),
    ("OTHER", "Other"),
)


class PatientCreateSerializer(serializers.Serializer):
    """Patient create serializer"""

    name = serializers.CharField(max_length=100, required=True)
    dob = serializers.DateField(required=True)
    gender = serializers.ChoiceField(required=True, choices=GENDER_CHOICES)
    contact_no = serializers.CharField(max_length=15, required=True)
    address = serializers.CharField(max_length=200, required=True)
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

    def validate_dob(self, value):
        today = datetime.date.today()
        if value > today:
            raise serializers.ValidationError("Invalid Date")
        return value

    def validate_contact_no(self, value):
        regex = re.compile(r"(^[+0-9]{1,3})*([0-9]{10,11}$)")

        if not re.fullmatch(regex, value):
            raise serializers.ValidationError("Invalid contact number")
        return value

    def validate_address(self, value):
        if len(value) > 100:
            raise serializers.ValidationError(
                "Address should not be more than 250 latter"
            )
        return value


class PatientEditSerializer(serializers.Serializer):
    """Patient edit serializer"""

    name = serializers.CharField(max_length=100, required=False)
    dob = serializers.DateField(required=False)
    gender = serializers.CharField(max_length=100, required=False)
    contact_no = serializers.CharField(max_length=60, required=False)
    address = serializers.CharField(max_length=200, required=False)
    email = None
    username = None
    password = None

    def validate_name(self, value):
        if len(value) > 50:
            raise serializers.ValidationError("Name should not be more than 50 latter")
        return value

    def validate_dob(self, value):
        today = datetime.date.today()
        if value > today:
            raise serializers.ValidationError("Invalid Date")
        return value

    def validate_contact_no(self, value):
        regex = re.compile(r"(^[+0-9]{1,3})*([0-9]{10,11}$)")

        if not re.fullmatch(regex, value):
            raise serializers.ValidationError("Invalid contact number")
        return value
    def validate_address(self, value):
        if len(value) > 100:
            raise serializers.ValidationError(
                "Address should not be more than 100 latter"
            )
        return value
