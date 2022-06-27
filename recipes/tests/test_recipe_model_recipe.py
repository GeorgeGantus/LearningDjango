from django.forms import ValidationError
from parameterized import parameterized

from .test_recipe_base import RecipeTestBase

"""
im using parameterized because i want to use unittest as test
runner because it is the default django test runner 
"""


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65)
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        with self.assertRaises(ValidationError):
            setattr(self.recipe, field, 'A'*(max_length+1))
            self.recipe.full_clean()
            self.recipe.save()

    def test_recipe_string_representation(self):
        title = 'Recipe Title'
        self.recipe.title = title
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(str(self.recipe), self.recipe.title)
