from unittest import TestCase

from django.test import TestCase as DjangoTestCase
from django.urls import reverse
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

    @parameterized.expand([
        ('password', 'A senha deve ter no mínimo 10 caracteres.'),
    ])
    def test_help_text_is_corret(self, field, helptext):
        form = RegisterForm()

        help_text = form[field].field.help_text

        self.assertEqual(help_text, helptext)

    @parameterized.expand([
        ('first_name', 'Nome'),
        ('last_name', 'Sobrenome'),
        ('username', 'Usuário'),
        ('email', 'E-mail'),
        ('password', 'Senha'),
        ('password2', 'Confirme a senha'),
    ])
    def test_label_is_corret(self, field, label):
        form = RegisterForm()

        label_field = form[field].field.label

        self.assertEqual(label_field, label)


class AuthorRegisterFormIntegrationTest(DjangoTestCase):
    def setUp(self, *args, **kwargs):
        self.form_data = {
            'username': 'userTest',
            'first_name': 'firstNameTest',
            'last_name': 'lastNameTest',
            'email': 'email@gmail.com',
            'password': 'StrongP4ssw0rd1',
            'password2': 'StrongP4ssw0rd1',
        }
        return super().setUp(*args, **kwargs)

    @parameterized.expand([
        ('first_name', 'Este campo é obrigatório.'),
        ('last_name', 'Este campo é obrigatório.'),
        ('username', 'Este campo é obrigatório.'),
        ('email', 'Este campo é obrigatório.'),
        ('password', 'Este campo é obrigatório.'),
        ('password2', 'Este campo é obrigatório.'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertIn(msg, response.context['form'].errors.get(field))
        self.assertIn(msg, response.content.decode('utf-8'))
