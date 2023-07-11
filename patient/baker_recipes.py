from model_bakery.recipe import Recipe
from .models import Patient

test_patient = Recipe(
    Patient,
    first_name='Test',
    last_name='Patient',
    address='Test Address',
)
