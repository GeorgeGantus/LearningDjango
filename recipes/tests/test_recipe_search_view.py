from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):

    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse('recipes:search'))
        self.assertEqual(view.func, views.search)

    def test_recipe_search_view_loads_correct_template(self):
        response = self.client.get(reverse('recipes:search') + '?q=search')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_view_raises_404_if_no_search(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_view_escapes_search(self):
        url = reverse('recipes:search') + '?q=<notarealtag>'
        response = self.client.get(url)
        self.assertIn('Search for "&lt;notarealtag&gt;"',
                      response.content.decode('utf-8'))
