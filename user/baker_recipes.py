from model_bakery.recipe import Recipe
from .models import User

admin_doctor = Recipe(
    User,
    first_name='Admin',
    last_name='Doctor',
    username='adminDoctor',
    email='admin_doctor@gmail.com',
    user_role=User.UserRoleEnums.DOCTOR,
    is_staff=True,
    is_superuser=True,
    is_active=True,
)

admin_patient = Recipe(
    User,
    first_name='Admin',
    last_name='Patient',
    username='adminPatient',
    email='admin_patient@gmail.com',
    user_role=User.UserRoleEnums.PATIENT,
    is_staff=True,
    is_superuser=True,
    is_active=True,
)

normal_doctor = Recipe(
    User,
    first_name='Normal',
    last_name='Doctor',
    username='normalDoctor',
    email='normal_doctor@gmail.com',
    user_role=User.UserRoleEnums.DOCTOR,
    is_staff=False,
    is_superuser=False,
    is_active=True,
)

normal_patient = Recipe(
    User,
    first_name='Normal',
    last_name='Patient',
    username='normalPatient',
    email='normal_patient@gmail.com',
    user_role=User.UserRoleEnums.PATIENT,
    is_staff=False,
    is_superuser=False,
    is_active=True,
)
