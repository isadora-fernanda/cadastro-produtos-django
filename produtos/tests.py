import os
import shutil
import tempfile
from io import BytesIO

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Produto
from .views import PRODUTOS_POR_PAGINA

MEDIA_TESTE = tempfile.mkdtemp()


def imagem_teste(nome='teste.png'):
    """Gera uma imagem PNG pequena em memória para simular o upload."""
    buffer = BytesIO()
    Image.new('RGB', (10, 10), 'blue').save(buffer, format='PNG')
    return SimpleUploadedFile(nome, buffer.getvalue(), content_type='image/png')


@override_settings(MEDIA_ROOT=MEDIA_TESTE)
class CrudProdutoTests(TestCase):

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_TESTE, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.produto = Produto.objects.create(
            nome='Caneca', descricao='Caneca de cerâmica', preco='29.90', estoque=10
        )

    def test_lista_mostra_produtos_com_preco_formatado(self):
        resposta = self.client.get(reverse('lista_produtos'))
        self.assertContains(resposta, 'Caneca')
        self.assertContains(resposta, 'R$ 29,90')

    def test_busca_por_nome(self):
        Produto.objects.create(nome='Garrafa', preco='45.00', estoque=3)
        resposta = self.client.get(reverse('lista_produtos'), {'busca': 'garr'})
        self.assertContains(resposta, 'Garrafa')
        self.assertNotContains(resposta, 'Caneca')

    def test_paginacao(self):
        for i in range(PRODUTOS_POR_PAGINA + 2):
            Produto.objects.create(nome=f'Item {i:02d}', preco='1.00', estoque=1)
        resposta = self.client.get(reverse('lista_produtos'))
        self.assertContains(resposta, 'Página 1 de 2')

    def test_cadastro_com_imagem_redireciona_para_lista(self):
        dados = {'nome': 'Camiseta', 'descricao': '', 'preco': '59.90', 'estoque': 5,
                 'imagem': imagem_teste()}
        resposta = self.client.post(reverse('cadastrar_produto'), dados)
        self.assertRedirects(resposta, reverse('lista_produtos'))
        produto = Produto.objects.get(nome='Camiseta')
        self.assertTrue(produto.imagem.name.startswith('produtos/'))

    def test_nome_obrigatorio(self):
        resposta = self.client.post(reverse('cadastrar_produto'),
                                    {'nome': '', 'preco': '10.00', 'estoque': 1})
        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(Produto.objects.filter(preco='10.00').exists())

    def test_estoque_aceita_apenas_inteiros(self):
        resposta = self.client.post(reverse('cadastrar_produto'),
                                    {'nome': 'Lápis', 'preco': '2.50', 'estoque': '1.5'})
        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(Produto.objects.filter(nome='Lápis').exists())

    def test_estoque_e_preco_nao_aceitam_negativos(self):
        for dados in ({'nome': 'Borracha', 'preco': '1.00', 'estoque': '-3'},
                      {'nome': 'Borracha', 'preco': '-1.00', 'estoque': '3'}):
            self.client.post(reverse('cadastrar_produto'), dados)
        self.assertFalse(Produto.objects.filter(nome='Borracha').exists())

    def test_edicao_atualiza_dados(self):
        url = reverse('editar_produto', args=[self.produto.id])
        resposta = self.client.post(url, {'nome': 'Caneca Grande', 'descricao': '',
                                          'preco': '34.90', 'estoque': 8})
        self.assertRedirects(resposta, reverse('lista_produtos'))
        self.produto.refresh_from_db()
        self.assertEqual(self.produto.nome, 'Caneca Grande')
        self.assertEqual(self.produto.estoque, 8)

    def test_trocar_imagem_apaga_o_arquivo_antigo(self):
        self.produto.imagem = imagem_teste('antiga.png')
        self.produto.save()
        caminho_antigo = self.produto.imagem.path

        url = reverse('editar_produto', args=[self.produto.id])
        self.client.post(url, {'nome': 'Caneca', 'descricao': '', 'preco': '29.90',
                               'estoque': 10, 'imagem': imagem_teste('nova.png')})
        self.assertFalse(os.path.exists(caminho_antigo))

    def test_exclusao_pede_confirmacao_e_apaga_a_imagem(self):
        self.produto.imagem = imagem_teste()
        self.produto.save()
        caminho = self.produto.imagem.path
        url = reverse('excluir_produto', args=[self.produto.id])

        resposta = self.client.get(url)
        self.assertContains(resposta, 'Excluir produto?')
        self.assertTrue(Produto.objects.filter(id=self.produto.id).exists())

        resposta = self.client.post(url)
        self.assertRedirects(resposta, reverse('lista_produtos'))
        self.assertFalse(Produto.objects.filter(id=self.produto.id).exists())
        self.assertFalse(os.path.exists(caminho))
