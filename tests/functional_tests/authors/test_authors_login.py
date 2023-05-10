import pytest
from django.contrib.auth.models import User
from django.urls import reverse
from selenium.webdriver.common.by import By

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):
    def test_user_valid_data_can_login_successfully(self):

        string_password = 'Mypassword123'

        user = User.objects.create_user(
            username='My_user',
            password=string_password
        )

        self.browser.get(self.live_server_url + reverse('authors:login'))

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username_field = self.get_by_placeholder(form, 'Insira o seu usuário')
        password_field = self.get_by_placeholder(form, 'Insira a sua senha')

        username_field.send_keys(user.username)
        password_field.send_keys(string_password)

        form.submit()

        self.assertIn(
            f'Seja bem vindo(a), {user.username}. Clique aqui para sair.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_create_raises_404_if_not_POST_method(self):
        self.browser.get(self.live_server_url +
                         reverse('authors:login_create'))

        self.assertIn(
            'Not Found',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_is_invalid(self):

        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username = self.get_by_placeholder(form, 'Insira o seu usuário')
        password = self.get_by_placeholder(form, 'Insira a sua senha')

        username.send_keys(' ')
        password.send_keys(' ')

        form.submit()

        self.assertIn(
            'Erro na validação do formulário.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )

    def test_login_invalid_credentials(self):

        self.browser.get(
            self.live_server_url + reverse('authors:login')
        )

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username = self.get_by_placeholder(form, 'Insira o seu usuário')
        password = self.get_by_placeholder(form, 'Insira a sua senha')

        username.send_keys('invalid_user')
        password.send_keys('invalid_password')

        form.submit()

        self.assertIn(
            'Usuário ou senha inválido.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
