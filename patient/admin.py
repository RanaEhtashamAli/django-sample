from django.contrib import admin
from .models import Patient, PatientVisit, PatientPrescription

admin.site.register(Patient)
admin.site.register(PatientVisit)
admin.site.register(PatientPrescription)
