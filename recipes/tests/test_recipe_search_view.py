from unittest.mock import patch

from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):

    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse('recipes:search'))
        self.assertEqual(view.func.view_class, views.RecipeListViewSearch)

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

    def test_recipe_search_view_can_find_recipe_by_title(self):
        title1 = 'This is recipe 1'
        title2 = 'This is recipe 2'

        recipe1 = self.make_recipe(
            slug='one', title=title1, user_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            slug='two', title=title2, user_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

    def test_recipe_search_view_only_show_published_recipes(self):
        title1 = 'This is a published recipe'
        title2 = 'This is a not published recipe'

        recipe1 = self.make_recipe(
            slug='published', title=title1, user_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            slug='not-published', is_published=False,
            title=title2, user_data={'username': 'two'}
        )

        response = self.client.get(reverse('recipes:search')+'?q=published')
        self.assertIn(recipe1, response.context['recipes'])
        self.assertNotIn(recipe2, response.context['recipes'])

    def test_recipe_search_is_paginated(self):
        self.make_n_recipes(8)
        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:search')+'?q=Recipe')
            recipes = response.context['recipes']
            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)
