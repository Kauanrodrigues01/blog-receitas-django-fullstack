from .base.test_base import RecipeCreationMixin, TestBaseRecipes
from django.core.exceptions import ValidationError

class CategoryModelTest(TestBaseRecipes, RecipeCreationMixin):
    @classmethod
    def setUpTestData(cls):
        cls.instance = cls()
        cls.category = cls.instance.make_category(name='Category Test')
        
    def test_recipe_category_model_string_representarion_is_name_field(self):
        self.assertEqual(
            str(self.category),
            self.category.name
        )

    def test_recipe_category_model_name_max_length_is_65_chars(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()
