from django.test import TestCase
from django.urls import reverse

class TestBaseUrlsAndViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.home_url = reverse('recipes:home')
        cls.category_url = reverse('recipes:recipe-by-category', kwargs={'category_id': 1})
        cls.recipe_url = reverse('recipes:recipe-detail', kwargs={'id': 1})