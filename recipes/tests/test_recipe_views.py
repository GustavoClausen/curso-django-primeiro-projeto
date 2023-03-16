from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import resolve, reverse

from recipes import views
from recipes.models import Category, Recipe


class RecipeViewsTest(TestCase):

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
        category = Category.objects.create(name='Category')
        author = User.objects.create_user(
            first_name='User first name',
            last_name='User last name',
            username='UserName',
            password='password21321',
            email='email@email.com',
        )
        recipe = Recipe.objects.create(
            category=category,
            author=author,
            title='Recipe title',
            description='Recipe description',
            slug='recipe-slug',
            preparation_time=10,
            preparation_time_unit='Minutos',
            servings=5,
            servings_unit='Porções',
            preparation_steps='Recipe preparation steps',
            preparation_steps_is_html=False,
            is_published=True,
            cover='recipes/covers/2023/03/08/pexels-team-picsfast-8753672.jpg',
        )

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

    def test_if_category_function_is_correct(self):
        view = resolve(reverse('recipes:category',
                       kwargs={'category_id': 1}))
        self.assertIs(view.func, views.category)

    def test_if_category_function_returns_404_if_there_not_category_req(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'category_id': 100})
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
