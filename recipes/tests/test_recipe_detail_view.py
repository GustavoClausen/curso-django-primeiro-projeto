from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):

    def test_if_recipe_function_is_correct(self):
        view = resolve(reverse('recipes:recipe', kwargs={'id': 1}))
        self.assertIs(view.func, views.recipe)

    def test_if_recipe_function_returns_404_if_there_not_recipe_required(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'id': 100})
        )
        self.assertEqual(response.status_code, 404)

    def test_if_recipe_template_loads_correct_recipe(self):

        needed_title = 'This is detail page - It loads a recipe'

        # Need a recipe for this recipe
        self.make_recipe(title=needed_title)

        response = self.client.get(reverse(
            'recipes:recipe',
            kwargs={
                'id': 1,
            }
        )
        )

        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_if_recipe_detail_template_not_loads_recipe_not_published(self):
        """
        Tests that unpublished recipes are actually not rendered.
        Testa se receitas não publicadas realmente não são renderizadas.
        """

        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse(
            'recipes:recipe',
            kwargs={
                'id': recipe.id,
            }
        )
        )

        self.assertEqual(response.status_code, 404)
