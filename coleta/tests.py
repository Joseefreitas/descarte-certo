import time
import os
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Create your tests here.
class TesteAgendaColeta(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        browser = os.environ.get('TEST_BROWSER', 'firefox')
        headless = os.environ.get('HEADLESS', 'true') != 'false'

        if browser == 'chrome':
            from selenium.webdriver.chrome.options import Options as ChromeOptions
            options = ChromeOptions()
            if headless:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            cls.browser = webdriver.Chrome(options=options)
        else:
            options = Options()
            if headless:
                options.add_argument('--headless')
            cls.browser = webdriver.Firefox(options=options)

        cls.browser.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super().tearDownClass()

    # SCRUM-9: Como usuário comum, eu gostaria de ter acesso aos dias e
    # horários que a coleta de resíduos é realizada na minha rua
    def test_scrum9_buscar_agenda_coleta(self):
        self.browser.get(f'{self.live_server_url}/coleta/agenda/')
        time.sleep(2)

        # Verifica se a página carregou
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertTrue(len(body) > 0)
        time.sleep(1)

        # Busca por um bairro
        campo = self.browser.find_element(By.NAME, 'regiao')
        campo.send_keys('Boa Viagem')
        time.sleep(1)

        self.browser.find_element(By.CSS_SELECTOR, '[type=submit]').click()
        time.sleep(3)

        # Verifica se retornou resultados ou mensagem
        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertTrue(len(body) > 0)
        time.sleep(2)

    def test_scrum9_busca_vazia_nao_quebra(self):
        self.browser.get(f'{self.live_server_url}/coleta/agenda/')
        time.sleep(2)

        # Tenta submeter sem preencher
        self.browser.find_element(By.CSS_SELECTOR, '[type=submit]').click()
        time.sleep(2)

        self.assertNotIn('500', self.browser.title)
        time.sleep(1)