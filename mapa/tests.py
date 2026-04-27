import time
import os
from django.test import LiveServerTestCase
from django.contrib.auth.models import User
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from .models import PontoColeta


class TesteMapaPontosColeta(LiveServerTestCase):

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
        PontoColeta.objects.create(
            nome='Ecoponto Boa Viagem',
            endereco='Av. Boa Viagem, 1000',
            latitude=-8.1190,
            longitude=-34.9000,
            tipo_residuo='Eletrônicos'
        )

    # SCRUM-10: Como usuário comum, eu gostaria de acessar
    # o mapa para visualizar os pontos de coleta e rotas
    def test_acessar_mapa_visualizar_pontos(self):
        self.browser.get(f'{self.live_server_url}/mapa/')
        time.sleep(2)

        mapa = self.browser.find_element(By.ID, 'mapa-container')
        self.assertTrue(mapa.is_displayed())
        time.sleep(2)

        titulo = self.browser.find_element(By.TAG_NAME, 'h2').text
        self.assertIn('Pontos de Descarte', titulo)
        time.sleep(1)

    # SCRUM-8: Como usuário comum, eu gostaria de localizar
    # o ponto de descarte mais próximo
    def test_localizar_ponto_mais_proximo(self):
        self.browser.get(f'{self.live_server_url}/mapa/')
        time.sleep(2)

        btn = self.browser.find_element(By.ID, 'btn-localizar')
        self.assertTrue(btn.is_displayed())
        time.sleep(1)

        lista = self.browser.find_element(By.ID, 'lista-proximos')
        self.assertTrue(lista.is_displayed())
        time.sleep(1)

        # Clica no botão e trata o alert de geolocalização
        btn.click()
        time.sleep(2)
        try:
            alert = self.browser.switch_to.alert
            alert.dismiss()
            time.sleep(1)
        except:
            pass

        # Verifica se o status de localização foi atualizado
        status = self.browser.find_element(By.ID, 'status-localizacao')
        self.assertTrue(status.is_displayed())
        time.sleep(2)

    # SCRUM-12: Como responsável por um ponto de coleta,
    # eu gostaria de cadastrá-lo
    def test_cadastrar_ponto_coleta(self):
        self.browser.get(f'{self.live_server_url}/mapa/adicionar/')
        time.sleep(2)

        self.browser.find_element(By.NAME, 'nome').send_keys('Cooperativa Verde')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'endereco').send_keys('Rua do Futuro, 42')
        time.sleep(1)
        self.browser.find_element(By.NAME, 'tipo_residuo').send_keys('Papel e Papelão')
        time.sleep(1)

        self.browser.execute_script(
            "document.querySelector('[name=latitude]').value = '-8.0500';"
        )
        self.browser.execute_script(
            "document.querySelector('[name=longitude]').value = '-34.8800';"
        )
        time.sleep(1)

        self.browser.find_element(By.CSS_SELECTOR, '.btn-salvar').click()
        time.sleep(2)

        self.assertIn('/mapa/', self.browser.current_url)
        self.assertTrue(PontoColeta.objects.filter(nome='Cooperativa Verde').exists())