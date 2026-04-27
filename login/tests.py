import time
import os
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

# Create your tests here.

class TesteCadastroUsuario(LiveServerTestCase):

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

    # SCRUM-19: Como usuário comum, eu gostaria de fazer cadastro no site
    def test_cadastro_usuario(self):
        self.browser.get(f'{self.live_server_url}/cadastro/')
        time.sleep(2)

        self.browser.find_element(By.NAME, 'username').send_keys('novousuario')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'first_name').send_keys('João')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'last_name').send_keys('Silva')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'email').send_keys('joao@teste.com')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'senha').send_keys('senhaforte123')
        time.sleep(1)

        self.browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]').click()
        time.sleep(3)

        self.assertTrue(User.objects.filter(username='novousuario').exists())