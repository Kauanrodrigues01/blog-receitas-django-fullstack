from .base.test_base import TestBaseRecipes, RecipeURLMixin, RecipeAssertionsMixin, RecipeCreationMixin
from recipes import views

class RecipeCategoryViewTest(TestBaseRecipes, RecipeURLMixin, RecipeCreationMixin, RecipeAssertionsMixin):
    
    def test_recipe_category_view_function_is_correct(self):
        self.assertViewFunctionIsCorrect(self.get_category_url(), views.recipes_by_category)
        
    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        url = self.get_category_url(1000)
        self.assert_404(url)
        
    def test_recipe_category_template_loads_recipes(self):
        needed_title = 'This is a category test'
        recipe = self.make_recipe(title=needed_title)
        
        response = self.client.get(self.get_category_url(recipe.category.id))
        content = response.content.decode('utf-8')
        
        self.assertIn(needed_title, content)
        
    def test_recipe_category_template_dont_load_recipes_not_published(self):
        recipe = self.make_recipe(is_published=False)
        
        response = self.client.get(self.get_category_url(recipe.category.id))
        content = response.content.decode('utf-8')
        
        self.assertIn('<h2>No recipes found here</h2>', content)