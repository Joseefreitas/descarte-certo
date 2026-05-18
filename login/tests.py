from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import PessoaFisica, PessoaJuridica


class EusouViewTest(TestCase):
    # verifica status 200 e template correto.
    def setUp(self):
        self.client = Client()

    def test_eusou_get_retorna_200(self):
        response = self.client.get(reverse('eusou'))
        self.assertEqual(response.status_code, 200)

    def test_eusou_usa_template_correto(self):
        response = self.client.get(reverse('eusou'))
        self.assertTemplateUsed(response, 'eusou.html')


class CadastroPessoaFisicaViewTest(TestCase):
    #Testa GET, criação de User e PessoaFisica, salvamento do nome completo,
    #redirecionamento para /login/ e bloqueio de username duplicado.
    def setUp(self):
        self.client = Client()
        self.url = reverse('cadastropessoafisica')
        self.dados_validos = {
            'username': 'joao123',
            'first_name': 'João',
            'last_name': 'Silva',
            'email': 'joao@email.com',
            'senha': 'senha_segura_123',
            'cpf': '123.456.789-00',
        }

    def test_get_retorna_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_usa_template_correto(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'cadastropessoafisica.html')

    def test_post_valido_cria_usuario(self):
        self.client.post(self.url, self.dados_validos)
        self.assertTrue(User.objects.filter(username='joao123').exists())

    def test_post_valido_cria_pessoa_fisica(self):
        self.client.post(self.url, self.dados_validos)
        user = User.objects.get(username='joao123')
        self.assertTrue(PessoaFisica.objects.filter(user=user, cpf='123.456.789-00').exists())

    def test_post_valido_salva_nome_completo(self):
        self.client.post(self.url, self.dados_validos)
        user = User.objects.get(username='joao123')
        self.assertEqual(user.first_name, 'João')
        self.assertEqual(user.last_name, 'Silva')

    def test_post_valido_redireciona_para_login(self):
        response = self.client.post(self.url, self.dados_validos)
        self.assertRedirects(response, '/login/')

    def test_post_username_duplicado_retorna_erro(self):
        User.objects.create_user(username='joao123', password='qualquer')
        response = self.client.post(self.url, self.dados_validos)
        self.assertEqual(response.status_code, 200)
        self.assertIn('erro', response.context)
        self.assertEqual(response.context['erro'], 'Usuário já existe')

    def test_post_username_duplicado_nao_cria_segundo_usuario(self):
        User.objects.create_user(username='joao123', password='qualquer')
        self.client.post(self.url, self.dados_validos)
        self.assertEqual(User.objects.filter(username='joao123').count(), 1)


class CadastroPessoaJuridicaViewTest(TestCase):
     #mesma estrutura, validando também os campos exclusivos de PJ
     #  (cnpj, razao_social, nome_fantasia). + 
     # bairros atendidos e tipo de resíduo .
    def setUp(self):
        self.client = Client()
        self.url = reverse('cadastropessoajuridica')
        self.dados_validos = {
            'username': 'empresa_xyz',
            'first_name': 'Carlos',
            'last_name': 'Souza',
            'email': 'contato@xyz.com',
            'senha': 'senha_segura_123',
            'cnpj': '12.345.678/0001-99',
            'razao_social': 'XYZ Comércio Ltda',
            'nome_fantasia': 'XYZ Store',
            'bairros_atendidos': 'Boa Viagem, Piedade',
            'tipos_residuo': ['organico', 'plastico'],
        }

    def test_get_retorna_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_usa_template_correto(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'cadastropessoajuridica.html')

    def test_post_valido_cria_usuario(self):
        self.client.post(self.url, self.dados_validos)
        self.assertTrue(User.objects.filter(username='empresa_xyz').exists())

    def test_post_valido_cria_pessoa_juridica(self):
        self.client.post(self.url, self.dados_validos)
        user = User.objects.get(username='empresa_xyz')
        pj = PessoaJuridica.objects.get(user=user)
        self.assertEqual(pj.cnpj, '12.345.678/0001-99')
        self.assertEqual(pj.razao_social, 'XYZ Comércio Ltda')
        self.assertEqual(pj.nome_fantasia, 'XYZ Store')

    def test_post_valido_salva_bairros_atendidos(self):
        #verifica se o campo de texto é persistido corretamente.
        self.client.post(self.url, self.dados_validos)
        user = User.objects.get(username='empresa_xyz')
        pj = PessoaJuridica.objects.get(user=user)
        self.assertEqual(pj.bairros_atendidos, 'Boa Viagem, Piedade')

    def test_post_valido_salva_tipos_residuo_como_string_separada_por_virgula(self):
        # valida o ','.join(tipos_residuo) que a view aplica antes de salvar.
        self.client.post(self.url, self.dados_validos)
        user = User.objects.get(username='empresa_xyz')
        pj = PessoaJuridica.objects.get(user=user)
        self.assertEqual(pj.tipos_residuo, 'organico,plastico')

    def test_post_valido_tipos_residuo_unico(self):
        """Garante que um único tipo de resíduo também é salvo corretamente."""
        dados = {**self.dados_validos, 'tipos_residuo': ['vidro']}
        self.client.post(self.url, dados)
        user = User.objects.get(username='empresa_xyz')
        pj = PessoaJuridica.objects.get(user=user)
        self.assertEqual(pj.tipos_residuo, 'vidro')

    def test_post_valido_sem_tipos_residuo_salva_vazio(self):
        # garante que nenhum tipo selecionado resulta em string vazia '', sem lançar erro.
        """Garante que ausência de tipos_residuo não quebra o cadastro."""
        dados = {**self.dados_validos}
        dados.pop('tipos_residuo')
        self.client.post(self.url, dados)
        user = User.objects.get(username='empresa_xyz')
        pj = PessoaJuridica.objects.get(user=user)
        self.assertEqual(pj.tipos_residuo, '')

    def test_post_valido_redireciona_para_login(self):
        response = self.client.post(self.url, self.dados_validos)
        self.assertRedirects(response, '/login/')

    def test_post_username_duplicado_retorna_erro(self):
        User.objects.create_user(username='empresa_xyz', password='qualquer')
        response = self.client.post(self.url, self.dados_validos)
        self.assertEqual(response.status_code, 200)
        self.assertIn('erro', response.context)
        self.assertEqual(response.context['erro'], 'Usuário já existe')

    def test_post_username_duplicado_nao_cria_segundo_usuario(self):
        User.objects.create_user(username='empresa_xyz', password='qualquer')
        self.client.post(self.url, self.dados_validos)
        self.assertEqual(User.objects.filter(username='empresa_xyz').count(), 1)


class LoginUsuarioViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('login_usuario')
        self.user = User.objects.create_user(
            username='testuser',
            password='senha_correta_123',
        )

    def test_get_retorna_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_usa_template_correto(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'login.html')

    def test_post_credenciais_validas_autentica_usuario(self):
        self.client.post(self.url, {'username': 'testuser', 'password': 'senha_correta_123'})
        user_id = self.client.session.get('_auth_user_id')
        self.assertEqual(int(user_id), self.user.id)

    def test_post_credenciais_validas_redireciona_para_home(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'senha_correta_123'})
        self.assertRedirects(response, '/home/')

    def test_post_senha_errada_retorna_erro(self):
        response = self.client.post(self.url, {'username': 'testuser', 'password': 'senha_errada'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('erro', response.context)
        self.assertEqual(response.context['erro'], 'Dados inválidos')

    def test_post_senha_errada_nao_autentica(self):
        self.client.post(self.url, {'username': 'testuser', 'password': 'senha_errada'})
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_post_usuario_inexistente_retorna_erro(self):
        response = self.client.post(self.url, {'username': 'naoexiste', 'password': 'qualquer'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('erro', response.context)

    def test_post_usuario_inexistente_usa_template_correto(self):
        response = self.client.post(self.url, {'username': 'naoexiste', 'password': 'qualquer'})
        self.assertTemplateUsed(response, 'login.html')


class LogoutUsuarioViewTest(TestCase):
    # valida encerramento de sessão, redirect para /login/ 
    # e que o logout sem sessão ativa não lança erro.
    def setUp(self):
        self.client = Client()
        self.url = reverse('logout_usuario')
        self.user = User.objects.create_user(username='testuser', password='senha123')

    def test_logout_encerra_sessao(self):
        self.client.login(username='testuser', password='senha123')
        self.client.get(self.url)
        self.assertNotIn('_auth_user_id', self.client.session)

    def test_logout_redireciona_para_login(self):
        self.client.login(username='testuser', password='senha123')
        response = self.client.get(self.url)
        self.assertRedirects(response, '/login/')

    def test_logout_sem_sessao_ativa_redireciona(self):
        """Logout sem usuário logado não deve lançar erro."""
        response = self.client.get(self.url)
        self.assertRedirects(response, '/login/')