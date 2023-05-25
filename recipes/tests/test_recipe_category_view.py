from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):

    def test_if_category_function_is_correct(self):
        view = resolve(reverse('recipes:category',
                       kwargs={'category_id': 1}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_if_category_function_returns_404_if_there_not_category_req(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 100})
        )
        self.assertEqual(response.status_code, 404)

    def test_if_category_templates_loads_recipes(self):

        needed_title = 'This is a category test'

        self.make_recipe(title=needed_title)

        response = self.client.get(reverse('recipes:category', args=(1,)))

        content = response.content.decode('utf-8')

        self.assertIn(needed_title, content)

    def test_if_category_templates_not_loads_recipe_not_published(self):
        """
        Tests that unpublished recipes are actually not rendered.
        Testa se receitas não publicadas realmente não são renderizadas.
        """

        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse(
            'recipes:recipe',
            kwargs={'id': recipe.category.id}
        )
        )

        self.assertEqual(response.status_code, 404)
