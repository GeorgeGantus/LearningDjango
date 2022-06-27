from django.test import TestCase
from recipes.models import Category, Recipe, User


class RecipeTestBase(TestCase):
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_user(
        self,
        first_name='Jon',
        last_name='Doe',
        username='user_jon',
        password='123456',
        email='jondoe@email.com'
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email
        )

    def make_recipe(
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
        preparation_steps_is_html=False,
        is_published=True,
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
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )