from unittest.mock import patch

from django.urls import resolve, reverse
from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipes:category', kwargs={'category_id': 1}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

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

    def test_recipe_category_is_paginated(self):
        self.make_n_recipes(8)
        with patch('recipes.views.PER_PAGE', new=3):
            response = self.client.get(
                reverse('recipes:category', kwargs={'category_id': 1}))
            paginator = response.context['recipes'].paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)
