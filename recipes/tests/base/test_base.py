from django.test import TestCase
from django.urls import reverse, resolve
from recipes.models import Recipe, Category 
from django.contrib.auth.models import User
from django.core.cache import cache

class TestBaseUrlsAndViews(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.home_url = reverse('recipes:home')
        
    def setUp(self):
        cache.clear()
        return super().setUp()
        
    def make_category(self, name='Category'):
        return Category.objects.create(name=name)

    def make_author(
        self,
        first_name='user',
        last_name='name',
        username='username',
        password='123456',
        email='username@email.com',
    ):
        return User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title='Recipe Title',
        description='Recipe Description',
        slug='recipe-slug',
        preparation_time=10,
        preparation_time_unit='Minutos',
        servings=5,
        servings_unit='Porções',
        preparation_steps='Recipe Preparation Steps',
        preparation_steps_is_html=False,
        is_published=True,
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published,
        )
    
    def get_category_url(self, category_id=1):
        return reverse('recipes:recipe-by-category', kwargs={'category_id': category_id})
    
    def get_recipe_url(self, recipe_id=1):
        return reverse('recipes:recipe-detail', kwargs={'id': recipe_id})
    
    def assert_404(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        
    def assertViewFunctionIsCorrect(self, url, expected_view):
        response = resolve(url)
        self.assertEqual(response.func, expected_view)