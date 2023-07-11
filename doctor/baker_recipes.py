from model_bakery.recipe import Recipe
from .models import Doctor

test_doctor = Recipe(
    Doctor,
    first_name='Test',
    last_name='Doctor',
)
