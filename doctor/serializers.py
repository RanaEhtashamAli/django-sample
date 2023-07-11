from rest_framework import serializers
from hospital.serializers import PatientSerializer
from patient.models import PatientPrescription
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']
        
        
class DoctorPrescriptionsSerializer(serializers.ModelSerializer):
    patient = PatientSerializer(source="visit.patient")

    class Meta:
        model = PatientPrescription
        fields = ['patient', 'remarks']
