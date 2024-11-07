from .base.test_base import TestBaseRecipes, RecipeURLMixin, RecipeAssertionsMixin, RecipeCreationMixin
from recipes.models import Recipe
from recipes import views

class RecipeViewTest(TestBaseRecipes, RecipeURLMixin, RecipeCreationMixin, RecipeAssertionsMixin):
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
        
    def test_recipe_category_view_function_is_correct(self):
        self.assertViewFunctionIsCorrect(self.get_category_url(), views.recipes_by_category)
        
    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        url = self.get_category_url(1000)
        self.assert_404(url)
        
    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        # Need a recipe for this test
        recipe = self.make_recipe(title=needed_title)
        
        response = self.client.get(self.get_category_url(recipe.category.id))
        content = response.content.decode('utf-8')
        
        # Check if one recipe exists
        self.assertIn(needed_title, content)
        
    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        
        response = self.client.get(self.get_category_url(recipe.category.id))
        content = response.content.decode('utf-8')
        
        self.assertIn('<h2>No recipes found here</h2>', content)
        
    def test_recipe_detail_view_function_is_correct(self):
        self.assertViewFunctionIsCorrect(self.get_recipe_url(), views.recipe)
        
    def test_recipe_detail_view_returns_404_if_no_recipes_found(self):
        url = self.get_recipe_url(1000)
        self.assert_404(url)
        
    def test_recipe_detail_template_loads_the_correct_recipe(self):
        needed_title = 'This is a detail page - It load one recipe'
        
        recipe = self.make_recipe(title=needed_title)
        
        response = self.client.get(self.get_recipe_url(recipe.id))
        content = response.content.decode('utf-8')
        
        self.assertIn(needed_title, content)
        
    def test_recipe_recipe_detail_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        
        response = self.client.get(self.get_recipe_url(recipe.id))
        content = response.content.decode('utf-8')
        
        self.assertIn('<h2>Recipe Not Found</h2>', content)