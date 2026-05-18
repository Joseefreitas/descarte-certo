from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from agendamento.models import Agendamento
from login.models import PessoaJuridica


def criar_empresa(user, bairros='Boa Viagem', tipos='plastico'):
    return PessoaJuridica.objects.create(
        user=user,
        cnpj='12.345.678/0001-99',
        razao_social='Empresa Teste Ltda',
        nome_fantasia='Empresa Teste',
        bairros_atendidos=bairros,
        tipos_residuo=tipos,
    )


class CriarAgendamentoViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('criar_agendamento')

        self.user = User.objects.create_user(username='testuser', password='senha123')
        self.user_pj = User.objects.create_user(username='empresa', password='senha123')
        self.empresa = criar_empresa(self.user_pj, bairros='Boa Viagem', tipos='plastico')

        self.dados_validos = {
            'bairro': 'Boa Viagem',
            'data': '2026-06-01',
            'horario': '09:00',
            'tipo_residuo': 'plastico',
        }

    # --- Acesso não autenticado ---

    def test_visitante_e_redirecionado(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_visitante_redireciona_para_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/login/?next={self.url}')

    # --- GET autenticado ---

    def test_get_autenticado_retorna_200(self):
        self.client.login(username='testuser', password='senha123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_usa_template_correto(self):
        self.client.login(username='testuser', password='senha123')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'agendamento.html')

    def test_get_agendamentos_no_contexto(self):
        self.client.login(username='testuser', password='senha123')
        response = self.client.get(self.url)
        self.assertIn('agendamentos', response.context)

    def test_get_exibe_apenas_agendamentos_do_usuario(self):
        outro_user = User.objects.create_user(username='outro', password='senha123')
        Agendamento.objects.create(
            usuario=self.user,
            empresa=self.empresa,
            bairro='Boa Viagem',
            data='2026-06-01',
            horario='09:00',
            tipo_residuo='plastico',
        )
        Agendamento.objects.create(
            usuario=outro_user,
            empresa=self.empresa,
            bairro='Boa Viagem',
            data='2026-06-02',
            horario='10:00',
            tipo_residuo='plastico',
        )
        self.client.login(username='testuser', password='senha123')
        response = self.client.get(self.url)
        self.assertEqual(len(response.context['agendamentos']), 1)

    # --- POST válido ---

    def test_post_valido_cria_agendamento(self):
        self.client.login(username='testuser', password='senha123')
        self.client.post(self.url, self.dados_validos)
        self.assertEqual(Agendamento.objects.count(), 1)

    def test_post_valido_associa_usuario(self):
        self.client.login(username='testuser', password='senha123')
        self.client.post(self.url, self.dados_validos)
        agendamento = Agendamento.objects.first()
        self.assertEqual(agendamento.usuario, self.user)

    def test_post_valido_associa_empresa_correta(self):
        self.client.login(username='testuser', password='senha123')
        self.client.post(self.url, self.dados_validos)
        agendamento = Agendamento.objects.first()
        self.assertEqual(agendamento.empresa, self.empresa)

    def test_post_valido_salva_dados_corretamente(self):
        self.client.login(username='testuser', password='senha123')
        self.client.post(self.url, self.dados_validos)
        agendamento = Agendamento.objects.first()
        self.assertEqual(agendamento.bairro, 'Boa Viagem')
        self.assertEqual(agendamento.horario, '09:00')
        self.assertEqual(agendamento.tipo_residuo, 'plastico')

    def test_post_valido_redireciona_para_agendamento(self):
        self.client.login(username='testuser', password='senha123')
        response = self.client.post(self.url, self.dados_validos)
        self.assertRedirects(response, self.url)

    def test_post_valido_exibe_mensagem_de_sucesso(self):
        self.client.login(username='testuser', password='senha123')
        response = self.client.post(self.url, self.dados_validos)
        msgs = list(response.wsgi_request._messages)
        self.assertTrue(any('sucesso' in str(m) for m in msgs))

    # --- POST sem empresa disponível ---

    def test_post_bairro_sem_empresa_nao_cria_agendamento(self):
        self.client.login(username='testuser', password='senha123')
        dados = {**self.dados_validos, 'bairro': 'Piedade'}
        self.client.post(self.url, dados)
        self.assertEqual(Agendamento.objects.count(), 0)

    def test_post_tipo_residuo_sem_empresa_nao_cria_agendamento(self):
        self.client.login(username='testuser', password='senha123')
        dados = {**self.dados_validos, 'tipo_residuo': 'vidro'}
        self.client.post(self.url, dados)
        self.assertEqual(Agendamento.objects.count(), 0)

    def test_post_sem_empresa_exibe_mensagem_de_erro(self):
        self.client.login(username='testuser', password='senha123')
        dados = {**self.dados_validos, 'bairro': 'Piedade'}
        response = self.client.post(self.url, dados)
        msgs = list(response.wsgi_request._messages)
        self.assertTrue(any('disponível' in str(m) for m in msgs))

    def test_post_sem_empresa_redireciona_para_agendamento(self):
        self.client.login(username='testuser', password='senha123')
        dados = {**self.dados_validos, 'bairro': 'Piedade'}
        response = self.client.post(self.url, dados)
        self.assertRedirects(response, self.url)

    # --- buscar_empresa: case insensitive ---

    def test_post_bairro_maiusculo_encontra_empresa(self):
        self.client.login(username='testuser', password='senha123')
        dados = {**self.dados_validos, 'bairro': 'BOA VIAGEM'}
        self.client.post(self.url, dados)
        self.assertEqual(Agendamento.objects.count(), 1)

    def test_post_tipo_residuo_maiusculo_encontra_empresa(self):
        self.client.login(username='testuser', password='senha123')
        dados = {**self.dados_validos, 'tipo_residuo': 'PLASTICO'}
        self.client.post(self.url, dados)
        self.assertEqual(Agendamento.objects.count(), 1)

    # --- Múltiplas empresas ---

    def test_post_seleciona_empresa_correta_entre_multiplas(self):
        user_pj2 = User.objects.create_user(username='empresa2', password='senha123')
        criar_empresa(user_pj2, bairros='Piedade', tipos='vidro')

        self.client.login(username='testuser', password='senha123')
        self.client.post(self.url, self.dados_validos)

        agendamento = Agendamento.objects.first()
        self.assertEqual(agendamento.empresa, self.empresa)