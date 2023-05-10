from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthorLogoutTest(TestCase):
    def test_user_tries_to_logout_using_get_method(self):
        User.objects.create_user(username='My_user', password='My_password')

        self.client.login(username='My_user', password='My_password')

        response = self.client.get(
            reverse('authors:logout'),
            follow=True
        )

        self.assertIn(
            'Requisicao de logout invalida.',
            response.content.decode('utf-8')
        )

    def test_user_tries_to_logout_another_user(self):
        User.objects.create_user(username='My_user', password='My_password')

        self.client.login(username='My_user', password='My_password')

        response = self.client.post(
            reverse('authors:logout'),
            follow=True,
            data={
                'username': 'another_user'
            },
        )

        self.assertIn(
            'Requisicao de logout negada.',
            response.content.decode('utf-8')
        )

    def test_user_can_logout_successfuly(self):
        User.objects.create_user(username='My_user', password='My_password')

        self.client.login(username='My_user', password='My_password')

        response = self.client.post(
            reverse('authors:logout'),
            follow=True,
            data={
                'username': 'My_user'
            },
        )

        self.assertIn(
            'Deslogado com sucesso.',
            response.content.decode('utf-8')
        )
