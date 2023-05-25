from unittest.mock import patch

from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeHomeViewTest(RecipeTestBase):

    def test_if_rootpage_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func.view_class, views.RecipeListViewHome)

    def test_if_rootpage_function_returns_status_code_200(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_if_rootpage_function_loads_correct_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_home_template_shows_no_recipes_found_if_there_not_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'Ainda não há receitas publicadas.',
            response.content.decode('utf-8')
        )

    def test_if_home_templates_loads_recipes(self):

        self.make_recipe(author_data={
            'first_name': 'Jose'
        })

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        self.assertIn('10 Minutos', content)
        self.assertIn('Recipe description', content)
        self.assertIn('Recipe title', content)
        self.assertIn('5 Porções', content)
        self.assertIn('Jose', content)

    def test_if_home_templates_not_loads_recipe_not_published(self):
        """
        Tests that unpublished recipes are actually not rendered.
        Testa se receitas não publicadas realmente não são renderizadas.
        """

        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipes:home'))
        content = response.content.decode('utf-8')

        self.assertIn('Ainda não há receitas publicadas.', content)

    # @patch('recipes.views.ITEMS_PER_PAGE', new=3)
    # Podemos usar de 2 formas. Como decorator ou abaixo na função
    def test_if_home_is_paginated(self):

        self.make_recipe_in_batch(qtd=8)

        with patch('recipes.views.ITEMS_PER_PAGE', new=3):
            response = self.client.get(reverse('recipes:home'))

            recipes = response.context['recipes']

            paginator = recipes.paginator

            self.assertEqual(paginator.num_pages, 3)
            self.assertEqual(len(paginator.get_page(1)), 3)
            self.assertEqual(len(paginator.get_page(2)), 3)
            self.assertEqual(len(paginator.get_page(3)), 2)

    def test_invalid_page_query_uses_page_one(self):

        self.make_recipe_in_batch(qtd=8)

        with patch('recipes.views.ITEMS_PER_PAGE', new=3):

            response = self.client.get(reverse('recipes:home') + '?page=1A')

            self.assertEqual(
                response.context['recipes'].number,
                1
            )

            response = self.client.get(reverse('recipes:home') + '?page=2')

            self.assertEqual(
                response.context['recipes'].number,
                2
            )
