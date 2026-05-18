from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from comunidade.models import Topic, Post
from login.models import PessoaJuridica


class ComunidadeViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('comunidade')

        self.user_pf = User.objects.create_user(username='pessoa_fisica', password='senha123')
        self.user_pj = User.objects.create_user(username='empresa', password='senha123')
        PessoaJuridica.objects.create(
            user=self.user_pj,
            cnpj='12.345.678/0001-99',
            razao_social='Empresa Teste Ltda',
            nome_fantasia='Empresa Teste',
        )
        self.topic = Topic.objects.create(
            title='Tópico de teste',
            content='Conteúdo de teste',
            author=self.user_pf,
        )

    # --- Acesso não autenticado ---

    def test_visitante_e_redirecionado(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)

    def test_visitante_redireciona_para_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/login/?next={self.url}')

    # --- GET autenticado ---

    def test_usuario_autenticado_retorna_200(self):
        self.client.login(username='pessoa_fisica', password='senha123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_usa_template_correto(self):
        self.client.login(username='pessoa_fisica', password='senha123')
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'comunidade.html')

    def test_topics_no_contexto(self):
        self.client.login(username='pessoa_fisica', password='senha123')
        response = self.client.get(self.url)
        self.assertIn('topics', response.context)
        self.assertEqual(len(response.context['topics']), 1)

    def test_empresas_ids_no_contexto(self):
        self.client.login(username='pessoa_fisica', password='senha123')
        response = self.client.get(self.url)
        self.assertIn('empresas_ids', response.context)

    # --- Tag is_empresa ---

    def test_pessoa_fisica_nao_e_empresa(self):
        self.client.login(username='pessoa_fisica', password='senha123')
        response = self.client.get(self.url)
        self.assertFalse(response.context['is_empresa'])

    def test_pessoa_juridica_e_empresa(self):
        self.client.login(username='empresa', password='senha123')
        response = self.client.get(self.url)
        self.assertTrue(response.context['is_empresa'])

    def test_empresas_ids_contem_id_da_pj(self):
        self.client.login(username='pessoa_fisica', password='senha123')
        response = self.client.get(self.url)
        self.assertIn(self.user_pj.id, response.context['empresas_ids'])

    def test_empresas_ids_nao_contem_id_da_pf(self):
        self.client.login(username='pessoa_fisica', password='senha123')
        response = self.client.get(self.url)
        self.assertNotIn(self.user_pf.id, response.context['empresas_ids'])

    # --- POST: criar tópico ---

    def test_post_valido_cria_topic(self):
        self.client.login(username='pessoa_fisica', password='senha123')
        self.client.post(self.url, {'titulo': 'Novo tópico', 'conteudo': 'Conteúdo'})
        self.assertEqual(Topic.objects.count(), 2)

    def test_post_valido_associa_author(self):
        self.client.login(username='pessoa_fisica', password='senha123')
        self.client.post(self.url, {'titulo': 'Novo tópico', 'conteudo': 'Conteúdo'})
        topic = Topic.objects.get(title='Novo tópico')
        self.assertEqual(topic.author, self.user_pf)

    def test_post_valido_redireciona_para_comunidade(self):
        self.client.login(username='pessoa_fisica', password='senha123')
        response = self.client.post(self.url, {'titulo': 'Novo tópico', 'conteudo': 'Conteúdo'})
        self.assertRedirects(response, self.url)


class TopicDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='senha123')
        self.user_pj = User.objects.create_user(username='empresa', password='senha123')
        PessoaJuridica.objects.create(
            user=self.user_pj,
            cnpj='12.345.678/0001-99',
            razao_social='Empresa Teste Ltda',
            nome_fantasia='Empresa Teste',
        )
        self.topic = Topic.objects.create(
            title='Tópico de teste',
            content='Conteúdo de teste',
            author=self.user,
        )
        self.url = reverse('topic_detail', kwargs={'topic_id': self.topic.id})

    # --- GET ---

    def test_visitante_retorna_200(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_usa_template_correto(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'topic_detail.html')

    def test_topic_no_contexto(self):
        response = self.client.get(self.url)
        self.assertEqual(response.context['topic'], self.topic)

    def test_posts_no_contexto(self):
        response = self.client.get(self.url)
        self.assertIn('posts', response.context)

    def test_empresas_ids_no_contexto(self):
        response = self.client.get(self.url)
        self.assertIn('empresas_ids', response.context)

    def test_topic_inexistente_retorna_404(self):
        url = reverse('topic_detail', kwargs={'topic_id': 9999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    # --- Tag is_empresa ---

    def test_visitante_nao_e_empresa(self):
        response = self.client.get(self.url)
        self.assertFalse(response.context['is_empresa'])

    def test_pessoa_juridica_e_empresa(self):
        self.client.login(username='empresa', password='senha123')
        response = self.client.get(self.url)
        self.assertTrue(response.context['is_empresa'])

    # --- POST: criar resposta ---

    def test_post_autenticado_cria_resposta(self):
        self.client.login(username='testuser', password='senha123')
        self.client.post(self.url, {'conteudo': 'Minha resposta'})
        self.assertEqual(self.topic.posts.count(), 1)

    def test_post_autenticado_associa_author(self):
        self.client.login(username='testuser', password='senha123')
        self.client.post(self.url, {'conteudo': 'Minha resposta'})
        post = self.topic.posts.first()
        self.assertEqual(post.author, self.user)

    def test_post_visitante_nao_cria_resposta(self):
        self.client.post(self.url, {'conteudo': 'Tentativa anônima'})
        self.assertEqual(self.topic.posts.count(), 0)

    def test_post_redireciona_apos_resposta(self):
        self.client.login(username='testuser', password='senha123')
        response = self.client.post(self.url, {'conteudo': 'Minha resposta'})
        self.assertRedirects(response, self.url)


class DeletarTopicViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = User.objects.create_user(username='author', password='senha123')
        self.outro = User.objects.create_user(username='outro', password='senha123')
        self.topic = Topic.objects.create(
            title='Tópico para deletar',
            content='Conteúdo',
            author=self.author,
        )
        self.url = reverse('deletar_topic', kwargs={'topic_id': self.topic.id})

    # --- Acesso não autenticado ---

    def test_visitante_e_redirecionado(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    # --- Deleção pelo autor ---

    def test_author_pode_deletar(self):
        self.client.login(username='author', password='senha123')
        self.client.post(self.url)
        self.assertFalse(Topic.objects.filter(id=self.topic.id).exists())

    def test_author_e_redirecionado_para_comunidade(self):
        self.client.login(username='author', password='senha123')
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('comunidade'))

    # --- Deleção por outro usuário ---

    def test_outro_usuario_nao_pode_deletar(self):
        self.client.login(username='outro', password='senha123')
        self.client.post(self.url)
        self.assertTrue(Topic.objects.filter(id=self.topic.id).exists())

    # --- Topic inexistente ---

    def test_topic_inexistente_retorna_404(self):
        self.client.login(username='author', password='senha123')
        url = reverse('deletar_topic', kwargs={'topic_id': 9999})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
