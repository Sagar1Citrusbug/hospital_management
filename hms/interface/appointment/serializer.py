import datetime
from rest_framework import serializers
from hms.domain.appointment.models import Appointment
from hms.domain.doctor.models import Doctor
from hms.domain.patient.models import Patient


class DoctorProfileSerializer(serializers.ModelSerializer):
    """DoctorProfile Serializer"""
    name  = serializers.SerializerMethodField()
    def get_name(self, obj):
        return obj.user.name
    class Meta:
        model = Doctor
        fields = [
            "name",
        ]


class PatientProfileSerializer(serializers.ModelSerializer):
    """PatientProfile Serializer"""
    name  = serializers.SerializerMethodField()
    def get_name(self, obj):
        return obj.user.name
    class Meta:
        model = Patient
        fields = [
            "name",
        ]

class AppointmentSerializer(serializers.ModelSerializer):
    """Appointment serializer"""
    
    class Meta:
        model = Appointment
        fields = [
            'id',
            'doctor',
            'patient',
            'appointment_date',
            'purpose',
        ]
        
    def to_representation(self, instance):
        self.fields["doctor"] = DoctorProfileSerializer(read_only=True)
        self.fields["patient"] = PatientProfileSerializer(read_only=True)
        return super(AppointmentSerializer, self).to_representation(instance)

class AppointmentCreateSerializer(serializers.Serializer):
    """Appointment create serializer"""

    patient_id = serializers.UUIDField(required=True)
    appointment_date = serializers.DateField(required=True)
    purpose = serializers.CharField(max_length=200, required=True)

    def validate_appointment_date(self, value):
        today = datetime.date.today()
        if value < today:
            raise serializers.ValidationError("Invalid Date")
        return value

    def validate_purpose(self, value):
        if len(value) > 100:
            raise serializers.ValidationError(
                "purpose should not be more than 100 latter"
            )
        return value


class AppointmentEditSerializer(serializers.Serializer):
    """Appointment edit serializer"""

    appointment_date = serializers.DateField(required=False)
    purpose = serializers.CharField(max_length=200, required=False)

    def validate_appointment_date(self, value):
        today = datetime.date.today()
        if value < today:
            raise serializers.ValidationError("Invalid Date")
        return value

    def validate_purpose(self, value):
        if len(value) > 100:
            raise serializers.ValidationError(
                "purpose should not be more than 100 latter"
            )
        return value
