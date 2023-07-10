
from rest_framework.utils.serializer_helpers import ReturnList

from patient.models import Patient
from user.models import User
from hospital.test import GenericTest


class UserTest(GenericTest):

    def test_setup_users(self):
        total_users = User.objects.count()
        self.assertEquals(total_users, 4)

    def test_setup_user_types(self):
        total_admin_users = User.objects.filter(is_staff=True).count()
        self.assertEquals(total_admin_users, 2)
        total_normal_users = User.objects.filter(is_staff=False).count()
        self.assertEquals(total_normal_users, 2)

    def test_user_login_valid(self):
        response = self.login_user(self.valid_login_data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals('access' in response.data, True)
        self.assertEquals('refresh' in response.data, True)

    def test_user_login_invalid(self):
        response = self.login_user(self.invalid_login_data)
        self.assertEquals(response.status_code, 401)

    def test_user_authed_invalid(self):
        response = self.client.get('/api/users/authed/')
        self.assertEquals(response.status_code, 401)

    def test_user_authed_valid(self):
        login_response = self.login_user(self.valid_login_data)
        response = self.client.get('/api/users/authed/', headers={'Authorization':
                                                                  f"Bearer {login_response.data['access']}"})
        self.assertEquals(response.status_code, 200)

    def test_user_authed_data(self):
        login_response = self.login_user(self.valid_login_data)
        response = self.client.get('/api/users/authed/', headers={'Authorization':
                                                                  f"Bearer {login_response.data['access']}"})
        self.assertEquals(response.status_code, 200)
        data = response.data

        expected_keys = ['first_name', 'last_name', 'username', 'email', 'user_role']
        self.assertEquals(UserTest.check_keys(expected_keys, data), True)

        expected_data = {
            'first_name': 'Admin',
            'last_name': 'Doctor',
            'username': 'adminDoctor',
            'email': 'admin_doctor@gmail.com',
            'user_role': User.UserRoleEnums.DOCTOR,
        }
        self.assertEquals(UserTest.check_data(expected_data, data), True)

    def test_user_retrieve_valid(self):
        user = User.objects.get(username='adminDoctor')

        login_response = self.login_user(self.valid_login_data)
        response = self.client.get(f'/api/users/{user.id}/', headers={'Authorization':
                                                                      f"Bearer {login_response.data['access']}"})

        self.assertEquals(response.status_code, 200)

        expected_keys = ['first_name', 'last_name', 'username', 'email', 'user_role']
        self.assertEquals(UserTest.check_keys(expected_keys, response.data), True)

    def test_user_retrieve_invalid(self):
        user = User.objects.get(username='adminPatient')

        login_response = self.login_user(self.valid_login_data)
        response = self.client.get(f'/api/users/{user.id}/', headers={'Authorization':
                                                                      f"Bearer {login_response.data['access']}"})

        self.assertEquals(response.status_code, 403)

    def test_user_list_valid(self):

        login_response = self.login_user(self.valid_login_data)
        response = self.client.get(f'/api/users/', headers={'Authorization':
                                                            f"Bearer {login_response.data['access']}"})

        self.assertEquals(response.status_code, 200)

        self.assertEquals(type(response.data), ReturnList)

        expected_keys = ['first_name', 'last_name', 'username', 'email', 'user_role']
        self.assertEquals(UserTest.check_keys(expected_keys, response.data[0]), True)

    def test_user_list_invalid(self):
        login_response = self.login_user(self.valid_login_data_non_admin)

        response = self.client.get(f'/api/users/', headers={'Authorization':
                                                            f"Bearer {login_response.data['access']}"})

        self.assertEquals(response.status_code, 403)

    def test_user_create_valid(self):
        create_user_data = {
            'first_name': 'Test',
            'last_name': 'Create',
            'username': 'testCreate',
            'password': 'Password@1',
            'email': 'test_create@gmail.com',
            'user_role': User.UserRoleEnums.PATIENT,
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        }
        login_response = self.login_user(self.valid_login_data)
        response = self.client.post(f'/api/users/', data=create_user_data,
                                    headers={'Authorization': f"Bearer {login_response.data['access']}"})
        self.assertEquals(response.status_code, 201)

        expected_keys = ['id', 'password', 'last_login', 'is_superuser', 'is_staff', 'is_active', 'date_joined',
                         'groups', 'user_permissions', 'first_name', 'last_name', 'username', 'email', 'user_role']
        self.assertEquals(UserTest.check_keys(expected_keys, response.data), True)

        patient = Patient.objects.filter(first_name=create_user_data['first_name'],
                                         last_name=create_user_data['last_name']).count()
        self.assertEquals(patient, 1)

    def test_user_create_invalid(self):
        create_user_data = {
            'first_name': 'Test',
            'last_name': 'Create',
            'username': 'testCreate',
            'password': 'Password@1',
            'email': 'test_create@gmail.com',
            'user_role': User.UserRoleEnums.PATIENT,
            'is_staff': True,
            'is_superuser': True,
            'is_active': True,
        }
        login_response = self.login_user(self.valid_login_data_non_admin)
        response = self.client.post(f'/api/users/', data=create_user_data,
                                    headers={'Authorization': f"Bearer {login_response.data['access']}"})
        self.assertEquals(response.status_code, 403)
