from django.forms import ValidationError
from parameterized import parameterized

from .test_recipe_base import Recipe, RecipeTestBase

"""
im using parameterized because i want to use unittest as test
runner because it is the default django test runner
"""


class RecipeModelTest(RecipeTestBase):

    def make_recipe_no_default(
        self,
        category_data={},
        user_data={},
        title='Recipe Title',
        description='Recipe description',
        slug='recipe-slug',
        servings=10,
        servings_unit='Porções',
        preparation_steps='preparation steps',
        preparation_time=5,
        preparation_time_unit='Minutos',
    ):
        return Recipe.objects.create(
            category=self.make_category(**category_data),
            user=self.make_user(**user_data),
            title=title,
            description=description,
            slug=slug,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
        )

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 65),
        ('servings_unit', 65)
    ])
    def test_recipe_fields_max_length(self, field, max_length):
        recipe = self.make_recipe()
        with self.assertRaises(ValidationError):
            setattr(recipe, field, 'A'*(max_length+1))
            recipe.full_clean()
            recipe.save()

    def test_recipe_string_representation(self):
        recipe = self.make_recipe()
        title = 'Recipe Title'
        recipe.title = title
        recipe.full_clean()
        recipe.save()
        self.assertEqual(str(recipe), recipe.title)

    def test_if_recipe_default_is_published_value_is_false(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(recipe.is_published)

    def test_if_recipe_default_preparation_steps_is_html_is_false(self):
        recipe = self.make_recipe_no_default()
        self.assertFalse(recipe.preparation_steps_is_html)
