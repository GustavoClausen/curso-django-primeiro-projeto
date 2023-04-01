from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def test_returns_error_if_title_has_more_than_65_characters(self):
        self.recipe.title = 'A' * 101

        with self.assertRaises(ValidationError):
            self.recipe.full_clean()
