import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .models import PontoColeta
import os

# Create your tests here.

class MapaTesteE2E(LiveServerTestCase):

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
            options.add_argument('--disable-dev-shm-usage')
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
        PontoColeta.objects.create(
            nome='Ponto Teste',
            endereco='Rua Teste, 123',
            latitude=-8.0592,
            longitude=-34.8725,
            tipo_residuo='Eletrônicos'
        )

    def test_pagina_mapa_carrega(self):
        self.browser.get(f'{self.live_server_url}/mapa/')
        time.sleep(2)
        self.assertIn('Descarte Certo', self.browser.title)

    def test_mapa_tem_titulo_correto(self):
        self.browser.get(f'{self.live_server_url}/mapa/')
        time.sleep(2)
        titulo = self.browser.find_element(By.TAG_NAME, 'h2').text
        time.sleep(1)
        self.assertIn('Pontos de Descarte', titulo)

    def test_botao_adicionar_redireciona(self):
        self.browser.get(f'{self.live_server_url}/mapa/')
        time.sleep(2)
        btn = self.browser.find_element(By.ID, 'btn-add-ponto')
        time.sleep(1)
        btn.click()
        time.sleep(2)
        self.assertIn('/mapa/adicionar/', self.browser.current_url)

    def test_formulario_cadastro_exibe_campos(self):
        self.browser.get(f'{self.live_server_url}/mapa/adicionar/')
        time.sleep(2)
        self.assertTrue(self.browser.find_element(By.NAME, 'nome'))
        time.sleep(0.5)
        self.assertTrue(self.browser.find_element(By.NAME, 'endereco'))
        time.sleep(0.5)
        self.assertTrue(self.browser.find_element(By.NAME, 'tipo_residuo'))
        time.sleep(0.5)
        self.assertTrue(self.browser.find_element(By.NAME, 'latitude'))
        time.sleep(0.5)
        self.assertTrue(self.browser.find_element(By.NAME, 'longitude'))
        time.sleep(1)

    def test_cadastro_ponto_com_sucesso(self):
        self.browser.get(f'{self.live_server_url}/mapa/adicionar/')
        time.sleep(2)

        campo_nome = self.browser.find_element(By.NAME, 'nome')
        campo_nome.send_keys('Ecoponto Teste')
        time.sleep(1)

        campo_endereco = self.browser.find_element(By.NAME, 'endereco')
        campo_endereco.send_keys('Av. Boa Viagem, 1000')
        time.sleep(1)

        campo_tipo = self.browser.find_element(By.NAME, 'tipo_residuo')
        campo_tipo.send_keys('Plástico')
        time.sleep(1)

        self.browser.execute_script(
            "document.querySelector('[name=latitude]').value = '-8.1190';"
        )
        self.browser.execute_script(
            "document.querySelector('[name=longitude]').value = '-34.9000';"
        )
        time.sleep(1)

        self.browser.find_element(By.CSS_SELECTOR, '.btn-salvar').click()
        time.sleep(2)

        self.assertIn('/mapa/', self.browser.current_url)
        self.assertTrue(PontoColeta.objects.filter(nome='Ecoponto Teste').exists())