from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import PatientVisitsSerializer, PatientPrescriptionSerializer, VisitsSerializer, \
    PrescriptionsSerializer, VisitSerializer, PrescriptionSerializer
from .models import Patient, PatientPrescription, PatientVisit
from hospital.serializers import PatientSerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'get_patient_visits':
            return PatientVisitsSerializer
        elif self.action == 'get_patient_prescriptions':
            return PatientPrescriptionSerializer
        return PatientSerializer

    @action(detail=True, methods=['get'])
    def get_patient_visits(self, request, pk=None):
        obj = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(obj.patient_visits, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def get_patient_prescriptions(self, request, pk=None):
        prescriptions = PatientPrescription.objects.filter(visit__patient_id=pk)
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(prescriptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientVisitViewSet(viewsets.ModelViewSet):
    queryset = PatientVisit.objects.all()
    serializer_class = VisitsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return VisitsSerializer
        return VisitSerializer


class PatientPrescriptionViewSet(viewsets.ModelViewSet):
    queryset = PatientPrescription.objects.all()
    serializer_class = PrescriptionsSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return PrescriptionsSerializer
        return PrescriptionSerializer
