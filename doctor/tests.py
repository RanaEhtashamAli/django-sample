from doctor.models import Doctor
from hospital.test import GenericTest


class DoctorTest(GenericTest):

    def test_doctor_list(self):
        login_response = self.login_user(self.valid_login_data)
        response = self.client.get(f'/api/doctors/', headers={'Authorization':
                                                              f"Bearer {login_response.data['access']}"})

        self.assertEquals(response.status_code, 200)

    def test_doctor_list_invalid(self):
        login_response = self.login_user(self.valid_login_data_patient_admin)
        response = self.client.get(f'/api/doctors/', headers={'Authorization':
                                                              f"Bearer {login_response.data['access']}"})

        self.assertEquals(response.status_code, 403)

    def test_doctor_create(self):
        login_response = self.login_user(self.valid_login_data)
        data = {
            'first_name': 'Doctor',
            'last_name': 'Create Test'
        }
        response = self.client.post(f'/api/doctors/', data=data,
                                    headers={'Authorization': f"Bearer {login_response.data['access']}"})

        self.assertEquals(response.status_code, 201)

        created_doctor = Doctor.objects.get(first_name='Doctor', last_name='Create Test')

        keys = ['id', 'first_name', 'last_name', 'created_at', 'updated_at']
        self.assertEquals(self.check_keys(keys, response.data), True)

        expected_data = {
            'id': created_doctor.id,
            'first_name': created_doctor.first_name,
            'last_name': created_doctor.last_name,
        }

        self.assertEquals(self.check_data(expected_data, response.data), True)

        doctors = Doctor.objects.count()
        self.assertEquals(doctors, 2)

    def test_doctor_create_invalid(self):
        login_response = self.login_user(self.valid_login_data)
        data = {
            'last_name': 'Create Test'
        }
        response = self.client.post(f'/api/doctors/', data=data,
                                    headers={'Authorization': f"Bearer {login_response.data['access']}"})

        self.assertEquals(response.status_code, 400)

    def test_doctor_update(self):
        doctor_to_update = Doctor.objects.get(first_name='Test', last_name='Doctor')
        login_response = self.login_user(self.valid_login_data)
        data = {
            'first_name': 'Test',
            'last_name': 'Doctor Updated'
        }
        response = self.client.patch(f'/api/doctors/{doctor_to_update.id}/', data=data,
                                    headers={'Authorization': f"Bearer {login_response.data['access']}"})

        self.assertEquals(response.status_code, 200)

        updated_doctor = Doctor.objects.get(first_name='Test', last_name='Doctor Updated')

        keys = ['id', 'first_name', 'last_name', 'created_at', 'updated_at']
        self.assertEquals(self.check_keys(keys, response.data), True)

        expected_data = {
            'id': updated_doctor.id,
            'first_name': updated_doctor.first_name,
            'last_name': updated_doctor.last_name,
        }

        self.assertEquals(self.check_data(expected_data, response.data), True)

    def test_doctor_prescription(self):
        login_response = self.login_user(self.valid_login_data)
        doctor = Doctor.objects.get(first_name='Test', last_name='Doctor')
        response = self.client.get(f"/api/doctors/{doctor.id}/get_doctor_prescriptions/", headers={"Authorization":
                                   f"Bearer {login_response.data['access']}"})

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 1)
