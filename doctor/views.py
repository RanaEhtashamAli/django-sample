from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action

from patient.models import PatientPrescription
from .serializers import DoctorSerializer, DoctorPrescriptionsSerializer
from .models import Doctor
from .permissions import DoctorPermission


class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, DoctorPermission]

    def get_serializer_class(self):
        if self.action == 'get_doctor_prescriptions':
            return DoctorPrescriptionsSerializer
        return DoctorSerializer

    @action(detail=True, methods=['get'])
    def get_doctor_prescriptions(self, request, pk=None):
        prescriptions = PatientPrescription.objects.filter(visit__doctor_id=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(prescriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
