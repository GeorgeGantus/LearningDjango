from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .recipe_base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipe found here!😢', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipe(self):
        self.make_n_recipes(10)
        # Usuario abre a página
        self.browser.get(self.live_server_url)
        title_needed = 'Recipe 1'
        # Usuario ve um campo com texto Search a recipe e busca a Recipe 1
        search = self.browser.find_element(
            By.XPATH, '//input[@placeholder="Search a recipe"]')
        search.send_keys(title_needed)
        search.send_keys(Keys.ENTER)
        # Usuario verifica se o item buscado apareceu na tela
        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        )

    @patch('recipes.views.PER_PAGE', new=3)
    def test_recipe_home_page_pagination(self):
        self.make_n_recipes(18)
        self.browser.get(self.live_server_url)
        page2_link = self.browser.find_element(
            By.XPATH, '//a[@aria-label="Go to page 2"]')
        page2_link.click()
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'card')),
            3
        )
