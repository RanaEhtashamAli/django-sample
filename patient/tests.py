from .models import Patient
from hospital.test import GenericTest


class PatientTest(GenericTest):

    def test_patient_list(self):
        login_response = self.login_user(self.valid_login_data_patient_admin)
        response = self.client.get(f'/api/patients/', headers={'Authorization':
                                                               f"Bearer {login_response.data['access']}"})

        self.assertEquals(response.status_code, 200)

    def test_patient_list_invalid(self):
        login_response = self.login_user(self.valid_login_data)
        response = self.client.get(f'/api/patients/', headers={'Authorization':
                                                              f"Bearer {login_response.data['access']}"})

        self.assertEquals(response.status_code, 403)

    def test_patient_create(self):
        login_response = self.login_user(self.valid_login_data_patient_admin)
        data = {
            'first_name': 'Patient',
            'last_name': 'Create Test',
            'address': 'Test Create Patient Address.'
        }
        response = self.client.post(f'/api/patients/', data=data,
                                    headers={'Authorization': f"Bearer {login_response.data['access']}"})

        self.assertEquals(response.status_code, 201)

        created_patient = Patient.objects.get(first_name='Patient', last_name='Create Test')

        keys = ['id', 'first_name', 'last_name', 'address', 'created_at', 'updated_at']
        self.assertEquals(self.check_keys(keys, response.data), True)

        expected_data = {
            'id': created_patient.id,
            'first_name': created_patient.first_name,
            'last_name': created_patient.last_name,
            'address': created_patient.address,
        }

        self.assertEquals(self.check_data(expected_data, response.data), True)

        patients = Patient.objects.count()
        self.assertEquals(patients, 2)

    def test_patient_create_invalid(self):
        login_response = self.login_user(self.valid_login_data_patient_admin)
        data = {
            'last_name': 'Create Test'
        }
        response = self.client.post(f'/api/patients/', data=data,
                                    headers={'Authorization': f"Bearer {login_response.data['access']}"})

        self.assertEquals(response.status_code, 400)

    def test_patient_update(self):
        patient_to_update = Patient.objects.get(first_name='Test', last_name='Patient')
        login_response = self.login_user(self.valid_login_data_patient_admin)
        data = {
            'first_name': 'Test',
            'last_name': 'Patient Updated'
        }
        response = self.client.patch(f'/api/patients/{patient_to_update.id}/', data=data,
                                    headers={'Authorization': f"Bearer {login_response.data['access']}"})

        self.assertEquals(response.status_code, 200)

        updated_patient = Patient.objects.get(first_name='Test', last_name='Patient Updated')

        keys = ['id', 'first_name', 'last_name', 'address', 'created_at', 'updated_at']
        self.assertEquals(self.check_keys(keys, response.data), True)

        expected_data = {
            'id': updated_patient.id,
            'first_name': updated_patient.first_name,
            'last_name': updated_patient.last_name,
            'address': updated_patient.address,
        }

        self.assertEquals(self.check_data(expected_data, response.data), True)

    def test_patient_prescription(self):
        login_response = self.login_user(self.valid_login_data_patient_admin)
        patient = Patient.objects.get(first_name='Test', last_name='Patient')
        response = self.client.get(f"/api/patients/{patient.id}/get_patient_prescriptions/", headers={"Authorization":
                                   f"Bearer {login_response.data['access']}"})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 1)
