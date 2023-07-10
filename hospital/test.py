from rest_framework.test import APITestCase, APIClient
from model_bakery import baker

from patient.models import PatientVisit, PatientPrescription


class GenericTest(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.adminDoctor = baker.make_recipe('user.admin_doctor')
        self.adminDoctor.set_password('Password@1')
        self.adminDoctor.save()
        self.adminPatient = baker.make_recipe('user.admin_patient')
        self.adminPatient.set_password('Password@1')
        self.adminPatient.save()
        self.normalDoctor = baker.make_recipe('user.normal_doctor')
        self.normalDoctor.set_password('Password@1')
        self.normalDoctor.save()
        self.normalPatient = baker.make_recipe('user.normal_patient')
        self.normalPatient.set_password('Password@1')
        self.normalPatient.save()
        self.valid_login_data = {
            "username": "adminDoctor",
            "password": "Password@1"
        }
        self.invalid_login_data = {
            "username": "adminDoctor",
            "password": "Password@123"
        }
        self.valid_login_data_non_admin = {
            "username": "normalDoctor",
            "password": "Password@1"
        }
        self.valid_login_data_patient_admin = {
            "username": "adminPatient",
            "password": "Password@1"
        }
        self.doctor = baker.make_recipe('doctor.test_doctor')
        self.patient = baker.make_recipe('patient.test_patient')
        self.visit = baker.make(
            PatientVisit,
            patient=self.patient,
            doctor=self.doctor,
        )
        self.prescription = baker.make(
            PatientPrescription,
            visit=self.visit,
            remarks='Test Remarks.',
        )

    def login_user(self, data):
        response = self.client.post('/api/token/', data=data, format='json')
        return response

    @staticmethod
    def check_keys(keys, response_data):
        for key in keys:
            if key not in response_data:
                return False
        return True

    @staticmethod
    def check_data(expected_data, response_data):
        for key, value in expected_data.items():
            if response_data[key] != value:
                return False
        return True