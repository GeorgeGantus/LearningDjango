from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_return_status_code_200(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_template_load_recipes(self):
        title = 'This is a recipe title'
        self.make_recipe(title=title)
        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        self.assertEqual(recipes[0].title, title)

    def test_recipe_home_template_show_only_published_recipes(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        recipes = response.context['recipes']
        self.assertEqual(len(recipes), 0)
