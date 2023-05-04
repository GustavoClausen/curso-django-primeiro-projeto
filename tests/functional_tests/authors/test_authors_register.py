from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import AuthorsBaseTest


class AuthorsRegisterTest(AuthorsBaseTest):

    def get_by_placeholder(self, web_element, placeholder):
        return web_element.find_element(
            By.XPATH,
            f'//input[@placeholder="{placeholder}"]'
        )

    def fill_form_dummy_data(self, form):
        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 10)

    def test_error_messages_empty_inputs(self):
        self.browser.get(self.live_server_url + '/authors/register/')

        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

        self.fill_form_dummy_data(form)

        form.find_element(By.NAME, 'email').send_keys('dummy@email.com')

        submit_button = form.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form/div[2]/div/button'
        )

        submit_button.send_keys(Keys.ENTER)

        form = self.browser.find_element(
            By.XPATH,
            '/html/body/main/div[2]/form'
        )

        self.assertIn('Este campo é obrigatório.', form.text)
