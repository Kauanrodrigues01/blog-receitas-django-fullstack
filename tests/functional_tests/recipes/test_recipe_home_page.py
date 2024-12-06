from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here 🥲', body.text)
        
    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch(2)
        recipes[0].title = 'Pizza'
        recipes[0].save()
        
        recipes[1].title = 'Burger'
        recipes[1].save()
        
        # Usuário abre a página inicial
        self.browser.get(self.live_server_url)
        
        # Vê o campo de busca
        search_input = self.browser.find_element(By.XPATH, '//input[@placeholder="Search for a recipe"]')
        
        # Clica no campo de busca e digita "Pizza"
        search_input.click()
        search_input.send_keys(recipes[0].title)
        # Pressiona Enter
        search_input.send_keys(Keys.ENTER)
        
        html = self.browser.page_source
                
        self.assertIn(recipes[0].title, html)
        self.assertNotIn(recipes[1].title, html)