from rest_framework import serializers

from doctor.models import Doctor
from patient.models import Patient
from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        user = super(UserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        if validated_data['user_role'] == User.UserRoleEnums.DOCTOR:
            Doctor.objects.create(first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        elif validated_data['user_role'] == User.UserRoleEnums.PATIENT:
            Patient.objects.create(first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        return user


class UserAuthedSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "user_role"]
