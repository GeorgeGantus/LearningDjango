from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, views.RecipeDetails)

    def test_recipe_detail_view_return_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_load_recipe(self):
        title = 'This is a recipe detail'
        self.make_recipe(title=title)
        response = self.client.get(reverse('recipes:recipe', kwargs={'pk': 1}))
        recipe = response.context['recipe']
        self.assertEqual(recipe.title, title)

    def test_recipe_detail_template_show_only_published_recipes(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:recipe', kwargs={
                                   'pk': recipe.id}))
        self.assertEqual(response.status_code, 404)
