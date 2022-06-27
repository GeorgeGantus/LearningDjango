from django.forms import ValidationError

from .test_recipe_base import RecipeTestBase


class CategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category()
        return super().setUp()

    def test_category_name_max_length_is_65_chars(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
            self.category.save()

    def test_category_string_representation(self):
        name = 'This is a category name'
        self.category.name = name
        self.category.full_clean()
        self.category.save()
        self.assertEqual(str(self.category), name)
