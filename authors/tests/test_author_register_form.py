from django.test import TestCase
from parameterized import parameterized

from authors.forms import RegisterForm


class AuthorRegisterFormUnitTest(TestCase):
    @parameterized.expand([
        ('first_name', 'Insira o seu nome'),
        ('last_name', 'Insira o seu sobrenome'),
        ('username', 'Exemplo: João_Silva'),
        ('email', 'Exemplo: seunome@email.com'),
        ('password', 'Insira uma senha'),
        ('password2', 'Repita a senha inserida'),
    ])
    def test_place_holder_is_corret(self, field, placeholder):
        form = RegisterForm()

        place_holder = form[field].field.widget.attrs['placeholder']

        self.assertEqual(placeholder, place_holder)
