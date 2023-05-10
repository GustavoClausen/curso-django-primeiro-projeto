import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 10)

    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

    def get_submit_button(self):
        form = self.get_form()
        return form.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form/div[2]/div/button'
        )

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()
        self.fill_form_dummy_data(form)
        form.find_element(By.NAME, 'email').send_keys('dummy@email')

        callback(form)

        return form

    def test_error_messages_empty_input_name(self):

        def callback(form):
            submit_button = self.get_submit_button()
            submit_button.send_keys(Keys.ENTER)
            form = self.get_form()

            li_error_name_empty = form.find_element(
                By.XPATH,
                '/html/body/main/div[2]/form/div[1]/div[1]/ul/li'
            )

            self.assertIn('Este campo é obrigatório.',
                          li_error_name_empty.text)

        self.form_field_test_with_callback(callback)

    def test_error_messages_empty_input_lastname(self):

        def callback(form):
            submit_button = self.get_submit_button()
            submit_button.send_keys(Keys.ENTER)
            form = self.get_form()

            li_err_last_name = form.find_element(
                By.XPATH,
                '/html/body/main/div[2]/form/div[1]/div[2]/ul/li'
            )

            self.assertIn('Este campo é obrigatório.',
                          li_err_last_name.text)

        self.form_field_test_with_callback(callback)

    def test_error_messages_empty_input_username(self):

        def callback(form):
            submit_button = self.get_submit_button()
            submit_button.send_keys(Keys.ENTER)
            form = self.get_form()

            li_err_user = form.find_element(
                By.XPATH,
                '/html/body/main/div[2]/form/div[1]/div[3]/ul/li'
            )

            self.assertIn('Este campo é obrigatório.',
                          li_err_user.text)

        self.form_field_test_with_callback(callback)

    def test_error_messages_empty_input_password(self):

        def callback(form):
            submit_button = self.get_submit_button()
            submit_button.send_keys(Keys.ENTER)
            form = self.get_form()

            li_err_password = form.find_element(
                By.XPATH,
                '/html/body/main/div[2]/form/div[1]/div[5]/ul/li'
            )

            self.assertIn('Este campo é obrigatório.',
                          li_err_password.text)

        self.form_field_test_with_callback(callback)

    def test_error_messages_empty_input_password2(self):

        def callback(form):
            submit_button = self.get_submit_button()
            submit_button.send_keys(Keys.ENTER)
            form = self.get_form()

            li_err_password2 = form.find_element(
                By.XPATH,
                '/html/body/main/div[2]/form/div[1]/div[6]/ul/li'
            )

            self.assertIn('Este campo é obrigatório.',
                          li_err_password2.text)

        self.form_field_test_with_callback(callback)

    def test_error_messages_input_invalid_email(self):

        def callback(form):
            submit_button = self.get_submit_button()
            submit_button.send_keys(Keys.ENTER)

            form = self.get_form()

            li_err_email = form.find_element(
                By.XPATH,
                '/html/body/main/div[2]/form/div[1]/div[4]/ul/li'
            )

            self.assertIn('Informe um endereço de email válido.',
                          li_err_email.text)

        self.form_field_test_with_callback(callback)

    def test_error_passwords_do_not_match(self):

        def callback(form):
            password1 = self.get_by_placeholder(
                form,
                'Insira uma senha'
            )
            password2 = self.get_by_placeholder(
                form,
                'Repita a senha inserida'
            )
            password1.send_keys('TEste@123')
            password2.send_keys('TEste@123456')

            submit_button = self.get_submit_button()
            submit_button.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('As senhas inseridas são diferentes.',
                          form.text)

        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.get_by_placeholder(
            form, 'Insira o seu nome'
        ).send_keys('Manoel')

        self.get_by_placeholder(
            form, 'Insira o seu sobrenome'
        ).send_keys('Gomes')

        self.get_by_placeholder(
            form, 'Exemplo: João_Silva'
        ).send_keys('Manoel_Gomes')

        self.get_by_placeholder(
            form, 'Exemplo: seunome@email.com'
        ).send_keys('manelgomes@email.com')

        self.get_by_placeholder(
            form, 'Insira uma senha'
        ).send_keys('ABCDdef1234')

        self.get_by_placeholder(
            form, 'Repita a senha inserida'
        ).send_keys('ABCDdef1234')

        submit_button = self.get_submit_button()
        submit_button.send_keys(Keys.ENTER)

        self.assertIn(
            'Usuário criado com sucesso.',
            self.browser.find_element(By.TAG_NAME, 'body').text
        )
