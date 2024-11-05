from .base.test_base import TestBaseUrlsAndViews
from django.urls import resolve
from recipes import views

class RecipeViewTest(TestBaseUrlsAndViews):
    def test_recipe_home_view_function_is_correct(self):
        view = resolve(self.home_url)
        self.assertEqual(view.func, views.home)
        
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(self.category_url)
        self.assertEqual(view.func, views.recipes_by_category)
        
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(self.recipe_url)
        self.assertEqual(view.func, views.recipe)