from django.urls import resolve, reverse

from recipes.views import site

from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):

    def test_recipe_search_uses_the_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func.view_class, site.RecipeListViewSearch)

    def test_recipe_search_loads_correct_template(self):
        url = reverse('recipes:search') + '?s=teste'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raiseis_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_page_title_and_scaped(self):
        url = reverse('recipes:search') + '?s=<teste>'
        response = self.client.get(url)
        self.assertIn(
            'Pesquisa por &quot;&lt;teste&gt;&quot;',
            response.content.decode('utf-8')
        )

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is a recipe one'
        title2 = 'This is a recipe two'

        recipe1 = self.make_recipe(
            slug='one', title=title1, author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            slug='two', title=title2, author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?s={title1}')
        response2 = self.client.get(f'{search_url}?s={title2}')
        response_both = self.client.get(f'{search_url}?s=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])

    def test_recipe_search_can_find_recipe_by_description(self):
        desc1 = 'Description of recipe one'
        desc2 = 'Description of recipe two'

        recipe1 = self.make_recipe(
            slug='one', description=desc1, author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            slug='two', description=desc2, author_data={'username': 'two'}
        )

        search_url = reverse('recipes:search')
        response1 = self.client.get(f'{search_url}?s={desc1}')
        response2 = self.client.get(f'{search_url}?s={desc2}')
        response_both = self.client.get(f'{search_url}?s=Description of')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])
