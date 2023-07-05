from rest_framework import serializers
from doctor.serializers import DoctorSerializer
from .models import Patient, PatientVisit, PatientPrescription
from hospital.serializers import PatientSerializer


# class PatientSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Patient
#         fields = '__all__'
#         read_only_fields = ['created_at', 'updated_at']


class VisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientVisit
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class VisitsSerializer(VisitSerializer):
    patient = PatientSerializer()
    doctor = DoctorSerializer()

    class Meta:
        model = PatientVisit
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class PatientVisitsSerializer(VisitsSerializer):

    class Meta:
        model = PatientVisit
        fields = ['doctor', 'created_at', 'updated_at']


class PatientPrescriptionSerializer(serializers.ModelSerializer):
    visit = PatientVisitsSerializer()

    class Meta:
        model = PatientPrescription
        fields = ['visit', 'remarks']


class PrescriptionsSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(source="visit.patient")
    doctor = DoctorSerializer(source="visit.doctor")

    class Meta:
        model = PatientPrescription
        fields = ["id", "patient", 'doctor', 'remarks']


class PrescriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PatientPrescription
        fields = '__all__'
