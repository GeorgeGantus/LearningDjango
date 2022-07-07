from django.test import TestCase
from recipes.models import Category, Recipe, User


class RecipeMixin:
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
        category=None
    ):

        if not category:
            category = self.make_category(**category_data)

        return Recipe.objects.create(
            category=category,
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

    def make_n_recipes(self, n):
        category = self.make_category()
        for i in range(n):
            kwargs = {'slug': f's{i}', 'category': category,
                      'user_data': {'username': f'u{i}'}}
            self.make_recipe(**kwargs)


class RecipeTestBase(TestCase, RecipeMixin):
    def setUp(self) -> None:
        return super().setUp()
