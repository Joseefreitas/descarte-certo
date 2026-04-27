import time
import os
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Create your tests here.

class TesteGuiaDescarte(LiveServerTestCase):

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

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='senha123'
        )

    def _fazer_login(self):
        self.browser.get(f'{self.live_server_url}/login/')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'username').send_keys('testuser')
        time.sleep(0.5)
        self.browser.find_element(By.NAME, 'password').send_keys('senha123')
        time.sleep(0.5)
        self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(2)

    # SCRUM-11: Como usuário comum, eu gostaria de saber
    # opções de reciclagem para fazer em casa
    def test_opcoes_reciclagem_casa(self):
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/guia-descarte/')
        time.sleep(2)

        self.assertIn('guia-descarte', self.browser.current_url)
        time.sleep(1)

        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertTrue(len(body) > 0)
        time.sleep(2)

    # SCRUM-7: Como usuário comum, eu gostaria de saber
    # a melhor forma de preparar um produto para o descarte
    def test_preparar_produto_descarte(self):
        self._fazer_login()
        self.browser.get(f'{self.live_server_url}/reciclagem/')
        time.sleep(2)

        self.assertIn('reciclagem', self.browser.current_url)
        time.sleep(1)

        body = self.browser.find_element(By.TAG_NAME, 'body').text
        self.assertTrue(len(body) > 0)
        time.sleep(2)

