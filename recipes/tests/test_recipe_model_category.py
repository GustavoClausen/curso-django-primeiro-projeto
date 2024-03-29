from django.core.exceptions import ValidationError

from .test_recipe_base import RecipeTestBase


class CategoryModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category = self.make_category(
            name='Category testing'
        )
        return super().setUp()

    def test_recipe_category_model_string_representation_is_name_field(self):
        self.assertEqual(
            str(self.category),
            self.category.name
        )

    def test_recipe_category_model_name_max_length_is_100_chars(self):
        self.category.name = 'A' * 101
        with self.assertRaises(ValidationError):
            self.category.full_clean()
