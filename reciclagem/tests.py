from django.test import TestCase

# Create your tests here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# @login_required(login_url='/login/')
# a tag loguin_required serve para dizer que só usa essa função quem tem loguin
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class ReciclagemViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('reciclagem')

    def test_visitante_retorna_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_visitante_usa_template_correto(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'reciclagem.html')

    def test_usuario_autenticado_retorna_200(self):
        user = User.objects.create_user(username='testuser', password='senha123')
        self.client.login(username='testuser', password='senha123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_usuario_autenticado_usa_template_correto(self):
        user = User.objects.create_user(username='testuser', password='senha123')
        self.client.login(username='testuser', password='senha123')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'reciclagem.html')
