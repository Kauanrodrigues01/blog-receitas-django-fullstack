from .base.test_base import TestBaseRecipes, RecipeCreationMixin
from django.core.exceptions import ValidationError

class RecipeModelTest(TestBaseRecipes, RecipeCreationMixin):
    def setUp(self):
        self.recipe = self.make_recipe()
        return super().setUp()
    
    def test_recipe_title_raises_error_if_title_has_more_than_65_chars(self):
        self.recipe.title = 'A' * 70
        
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
            
    def test_recipe_fields_max_lenght(self):
        fields = [
            ('title', 65),
            ('description', 165),
            ('preparation_time_unit', 65),
            ('servings_unit', 65),
        ]
        
        for field, value_max_lenght in fields:
            with self.subTest(field=field, value_max_lenght=value_max_lenght):
                setattr(self.recipe, field, 'A' * (value_max_lenght + 1))
                with self.assertRaises(ValidationError):
                    self.recipe.full_clean()
                setattr(self.recipe, field, 'A')
                