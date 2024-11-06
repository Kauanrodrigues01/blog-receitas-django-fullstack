from .base.test_base import TestBaseUrlsAndViews
from recipes.models import Recipe
from django.urls import resolve
from recipes import views
from django.urls import reverse

class RecipeViewTest(TestBaseUrlsAndViews):
    def test_recipe_home_view_function_is_correct(self):
        self.assertViewFunctionIsCorrect(self.home_url, views.home)
        
    def test_recipe_home_view_returns_status_code_200_OK(self):
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        
    def test_recipe_home_view_loads_correct_template(self):
        response  = self.client.get(self.home_url)
        self.assertTemplateUsed(response, 'recipes/pages/home.html')
        
    def test_recipe_home_template_shows_no_recipes_found_if_no_recipes(self):
        recipes = Recipe.objects.all().delete()
        print(recipes)
        response = self.client.get(self.home_url)
        self.assertIn('<h2>Recipes Not Found</h2>', response.content.decode('utf-8'))
        
    def test_recipe_home_template_loads_recipes(self):
        recipe = self.make_recipe()
        
        response = self.client.get(self.home_url)
        content = response.content.decode('utf-8')
        response_context_recipes = response.context['recipes']
        
        self.assertIn(recipe.title, content)
        self.assertIn(f'{recipe.preparation_time} {recipe.preparation_time_unit}', content)
        self.assertIn(f'{recipe.servings} {recipe.servings_unit}', content)
        self.assertEqual(len(response_context_recipes), 1)
        
    def test_recipe_category_view_function_is_correct(self):
        url = self.get_category_url(category_id=1)
        self.assertViewFunctionIsCorrect(url, views.recipes_by_category)
        
    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        url = self.get_category_url(category_id=1000)
        self.assert_404(url)
        
    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        # Need a recipe for this test
        self.make_recipe(title=needed_title)
        
        url = self.get_category_url(category_id=1)
        response = self.client.get(url)
        content = response.content.decode('utf-8')
        
        # Check if one recipe exists
        self.assertIn(needed_title, content)
        
    def test_recipe_detail_view_function_is_correct(self):
        url = self.get_recipe_url(recipe_id=1)
        self.assertViewFunctionIsCorrect(url, views.recipe)
        
    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        url = self.get_recipe_url(recipe_id=1000)
        self.assert_404(url)