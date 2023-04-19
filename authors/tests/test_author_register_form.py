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
        ('username', 'De 4 a 150 caracteres. Letras, números ou @/./+/-/_ apenas.'),  # noqa: E501
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

    def test_username_field_min_length_should_be_4(self):
        self.form_data['username'] = 'a'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Usuário deve possuir no mínimo 4 caracteres.'

        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_username_field_max_length_should_be_150(self):
        self.form_data['username'] = 'a' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'Usuário deve possuir no máximo 150 caracteres.'

        self.assertIn(msg, response.context['form'].errors.get('username'))
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_password_field_have_lower_upper_case_letters_and_numbers(self):
        self.form_data['password'] = 'a' * 10
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'A senha precisa ter letras maísculas, minúsculas e números.'

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = 'ABCdef12356@#$'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.context['form'].errors.get('password'))
        self.assertNotIn(msg, response.content.decode('utf-8'))

    def test_password_and_password2_are_equal(self):
        self.form_data['password'] = 'ABCdef123' * 2
        self.form_data['password2'] = 'ABCdef123' * 3

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        msg = 'As senhas inseridas são diferentes.'

        self.assertIn(msg, response.context['form'].errors.get('password'))
        self.assertIn(msg, response.content.decode('utf-8'))

        self.form_data['password'] = 'ABCdef123'
        self.form_data['password2'] = 'ABCdef123'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)

        self.assertNotIn(msg, response.content.decode('utf-8'))
