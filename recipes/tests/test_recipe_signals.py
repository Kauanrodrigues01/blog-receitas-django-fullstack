from .base.test_base import TestBaseRecipes, RecipeCreationMixin
from django.core.cache import cache
from django.urls import reverse

class RecipeSignalsTest(TestBaseRecipes, RecipeCreationMixin):
    @classmethod
    def setUpTestData(cls):
        cls.instance = cls()
        cls.category = cls.instance.make_category()
        cls.recipe = cls.instance.make_recipe()
    
    def setUp(self):
        cache.set('home_recipes', 'value_cache')
        cache.set('recipes-by-category', 'value-cache')
        return super().setUp()

    def test_clear_cache_when_saving_a_recipe(self):
        self.assertEqual(cache.get('home_recipes'), 'value_cache')
        self.assertEqual(cache.get('recipes-by-category'), 'value-cache')

        self.recipe.title = 'new title'
        self.recipe.save()

        self.assertIsNone(cache.get('home_recipes'))
        self.assertIsNone(cache.get('recipes-by-category'))

    def test_clear_cache_when_deleting_a_recipe(self):
        self.assertEqual(cache.get('home_recipes'), 'value_cache')
        self.assertEqual(cache.get('recipes-by-category'), 'value-cache')
        
        self.recipe.delete()
        
        self.assertIsNone(cache.get('home_recipes'))
        self.assertIsNone(cache.get('recipes-by-category'))
        
    def test_clear_cache_when_saving_a_category(self):
        self.assertEqual(cache.get('home_recipes'), 'value_cache')
        self.assertEqual(cache.get('recipes-by-category'), 'value-cache')

        self.category.name = 'new name'
        self.category.save()

        self.assertIsNone(cache.get('home_recipes'))
        self.assertIsNone(cache.get('recipes-by-category'))

    def test_clear_cache_when_deleting_a_category(self):
        self.assertEqual(cache.get('home_recipes'), 'value_cache')
        self.assertEqual(cache.get('recipes-by-category'), 'value-cache')
        
        self.category.delete()
        
        self.assertIsNone(cache.get('home_recipes'))
        self.assertIsNone(cache.get('recipes-by-category'))