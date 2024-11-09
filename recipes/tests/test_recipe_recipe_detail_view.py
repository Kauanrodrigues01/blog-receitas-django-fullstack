from .base.test_base import TestBaseRecipes, RecipeURLMixin, RecipeAssertionsMixin, RecipeCreationMixin
from recipes import views

class RecipeDetailViewTest(TestBaseRecipes, RecipeURLMixin, RecipeCreationMixin, RecipeAssertionsMixin):
        
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