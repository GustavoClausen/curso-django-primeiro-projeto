from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    @patch('recipes.views.ITEMS_PER_PAGE', new=2)
    def test_recipe_home_page_without_recipe_not_found_messages(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('Ainda não há receitas publicadas.', body.text)

    @patch('recipes.views.ITEMS_PER_PAGE', new=2)
    def test_user_can_find_a_recipe_with_the_wished_term(self):
        recipes = self.make_recipe_in_batch(3)

        title_needed = 'O valor desejado'
        recipes[0].title = title_needed
        recipes[0].save()

        # Usuário abre página
        self.browser.get(self.live_server_url)

        # Página inicial exibe um input de pesquisa
        search_input = self.browser.find_element(
            By.XPATH,
            '//input[@placeholder="Digite o que você está procurando..."]'
        )

        # Clicar no input e digitar o termo de busca "Recipe Title 1"
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        self.assertIn(
            title_needed,
            self.browser.find_element(By.CLASS_NAME, 'main-content-list').text
        )

    @patch('recipes.views.ITEMS_PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()

        # Usuário abre página
        self.browser.get(self.live_server_url)

        #  Verfica a paginação e clica na página desejada
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Vá para a página 2."]'
        )
        page2.click()

        # Verifica que tem mais 2 receitas na página 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )

        page3 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Vá para a página 3."]'
        )
        page3.click()

        # Verifica que tem mais 2 receitas na página 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )
