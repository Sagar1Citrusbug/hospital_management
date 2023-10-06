from rest_framework import serializers
from hms.domain.user.models import User


class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=254, required=True)
    password = serializers.CharField(max_length=254, required=True)


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email","password" ,"is_staff", "is_patient"]