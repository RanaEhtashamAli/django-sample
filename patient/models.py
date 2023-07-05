from django.db import models
from doctor.models import Doctor


class Patient(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class PatientVisit(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.RESTRICT, related_name='patient_visits')
    doctor = models.ForeignKey(Doctor, on_delete=models.RESTRICT, related_name='doctor_patients')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.patient.full_name} to {self.doctor.full_name}"


class PatientPrescription(models.Model):
    visit = models.ForeignKey(PatientVisit, on_delete=models.RESTRICT)
    remarks = models.TextField()

    def __str__(self):
        return f"{self.visit.patient.full_name}'s visit to {self.visit.doctor.full_name}"
