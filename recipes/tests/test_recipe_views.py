from django.urls import resolve, reverse

from recipes import views

from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):

    def test_if_rootpage_function_is_correct(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.root_page)

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
        recipes = response.context['recipes']
        recipe = recipes.first()

        content = response.content.decode('utf-8')

        self.assertEqual(len(recipes), 1)
        self.assertEqual(recipe.title, 'Recipe title')

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

    def test_if_category_function_is_correct(self):
        view = resolve(reverse('recipes:category',
                       kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

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

    def test_recipe_search_uses_the_correct_view_function(self):
        url = reverse('recipes:search')
        resolved = resolve(url)
        self.assertIs(resolved.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        url = reverse('recipes:search') + '?s=teste'
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raiseis_404_if_no_search_term(self):
        url = reverse('recipes:search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
