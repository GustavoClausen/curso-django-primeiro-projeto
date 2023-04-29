from selenium.webdriver.common.by import By

from .base import RecipeBaseFunctionalTest


class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipe_home_page_without_recipe_not_found_messages(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Ainda não há receitas publicadas.', body.text)
