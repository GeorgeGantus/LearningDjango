from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
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

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_recipe_category_view_return_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_load_recipes(self):
        category_data = {'name': 'This is a category'}
        self.make_recipe(category_data=category_data)
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 1}))
        recipes = response.context['recipes']
        self.assertEqual(recipes[0].category.name, category_data['name'])

    def test_recipe_category_template_show_only_published_recipes(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:category', kwargs={
                                   'category_id': recipe.category.id}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_return_404_if_no_recipe_found(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_load_recipe(self):
        title = 'This is a recipe detail'
        self.make_recipe(title=title)
        response = self.client.get(reverse('recipes:recipe', kwargs={'id': 1}))
        recipe = response.context['recipe']
        self.assertEqual(recipe.title, title)

    def test_recipe_detail_template_show_only_published_recipes(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:recipe', kwargs={
                                   'id': recipe.id}))
        self.assertEqual(response.status_code, 404)

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
