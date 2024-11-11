from .base.test_base import TestBaseRecipes, RecipeURLMixin, RecipeAssertionsMixin, RecipeCreationMixin
from recipes import views
from django.core.cache import cache
from unittest.mock import patch

class RecipeHomeViewTest(TestBaseRecipes, RecipeURLMixin, RecipeCreationMixin, RecipeAssertionsMixin):
    def test_recipe_home_view_function_is_correct(self):
        self.assertViewFunctionIsCorrect(self.home_url, views.home)
        
    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        
    def test_recipe_home_view_loads_correct_template(self):
        response  = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'recipes/pages/home.html')
        
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        cache.clear()
        response = self.client.get(self.home_url)
        self.assertIn('<h2>No recipes found here</h2>', response.content.decode('utf-8'))
        
    def test_recipe_home_template_loads_recipes(self):
        recipe = self.make_recipe()
        
        response = self.client.get(self.home_url)
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        
        self.assertIn(recipe.title, content)
        self.assertIn(f'{recipe.preparation_time} {recipe.preparation_time_unit}', content)
        self.assertIn(f'{recipe.servings} {recipe.servings_unit}', content)
        self.assertEqual(len(response_context_recipes), 1)
        
    def test_recipe_home_template_dont_load_recipes_not_published(self):
        self.make_recipe(is_published=False)
        
        response = self.client.get(self.home_url)
        content = response.content.decode('utf-8')
        
        self.assertIn('<h2>No recipes found here</h2>', content)
    
    @patch('recipes.views.RECIPES_PER_PAGE', new=2)
    def test_recipe_home_is_paginated(self):
        for i in range(4):
            kwargs={
                'slug': f'slug-{i}',
                'author_data': {
                    'username': f'author-{i}',
                }
            }
            self.make_recipe(**kwargs)
        
        response = self.client.get(self.home_url)
        recipes = response.context['recipes']
        paginator = recipes.paginator
        
        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(len(paginator.get_page(1)), 2)
        self.assertEqual(len(paginator.get_page(2)), 2)