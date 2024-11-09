from .base.test_base import TestBaseRecipes, RecipeURLMixin, RecipeAssertionsMixin, RecipeCreationMixin
from recipes import views

class RecipeSearchViewTest(TestBaseRecipes, RecipeURLMixin, RecipeCreationMixin, RecipeAssertionsMixin):
    def test_recipe_search_view_function_is_correct(self):
        self.assertViewFunctionIsCorrect(self.get_search_url(), views.search)
        
    def test_recipe_search_loads_correct_template(self):
        response = self.client.get(self.get_search_url(q='test'))
        self.assertTemplateUsed(response, 'recipes/pages/search.html')
        
    def test_recipe_search_raises_404_if_no_search_term(self):
        self.assert_404(self.get_search_url())
        
    def test_recipe_search_raises_404_if_search_term_is_an_empty_string(self):
        self.assert_404(self.get_search_url(q='         '))
        
    def test_recipe_search_term_is_on_page_title_and_escaped(self):
        url = self.get_search_url(q='<Teste>')
        response = self.client.get(url)
        self.assertIn(
            'Search for &quot;&lt;Teste&gt;&quot;',
            response.content.decode('utf-8')
        )
        
    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'
        
        recipe1 = self.make_recipe(
            slug='one', title=title1, author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            slug='two', title=title2, author_data={'username': 'two'}
        )
        
        search_url = self.get_search_url()
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')
        
        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])
        
        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])
        
        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])