from .base.test_base import TestBaseUrlsAndViews

class RecipeURLsTest(TestBaseUrlsAndViews):
    def test_recipe_home_url_is_correct(self):
        self.assertEqual(self.home_url, '/')
        
    def test_recipe_category_url_is_correct(self):
        self.assertEqual(self.get_category_url(), '/recipes/category/1/')
        
    def test_recipe_detail_url_is_correct(self):
        self.assertEqual(self.get_recipe_url(), '/recipes/1/')