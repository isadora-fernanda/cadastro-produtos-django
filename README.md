# Cadastro de Produtos com Django

Sistema web em **Python** e **Django** para cadastrar, listar, editar e excluir os produtos de uma loja, com imagem de cada produto. Foi um trabalho individual do curso **Python para Inteligência Artificial** do **Entra21** (Blusoft e ACATE), em 2026.

> **English:** Django CRUD app for a store's products (Entra21 Python for AI course, 2026), with image upload, name search, pagination and a delete confirmation page. Prices and stock are validated, old image files are removed when a product is edited or deleted, and every operation is covered by automated tests.

<img src="docs/lista.png" alt="Lista de produtos" width="700">

*Lista com produtos de demonstração. As imagens foram desenhadas só para esta captura.*

## O que o enunciado pedia

| Requisito | Como foi atendido |
|---|---|
| Projeto Django com a aplicação `produtos` | Projeto `config` e app `produtos`, com banco SQLite |
| Modelo `Produto` com nome, descrição, preço, estoque e imagem | `produtos/models.py` |
| Listar, cadastrar, visualizar, editar e excluir | Uma view para cada operação em `produtos/views.py` |
| Nome obrigatório, preço decimal, estoque inteiro e imagem opcional | `CharField`, `DecimalField`, `PositiveIntegerField` e `ImageField(blank=True)` |
| Imagem exibida na listagem e nos detalhes | Miniatura na tabela e imagem grande na página do produto |
| Formulário com `multipart/form-data` usando Django Forms | `ModelForm` em `produtos/forms.py`, usado no cadastro e na edição |
| `MEDIA_URL` e `MEDIA_ROOT` configurados | Imagens salvas em `media/produtos/` e servidas em `/media/` |
| Voltar para a lista depois de cadastrar, editar ou excluir | Redirecionamento para a lista, com uma mensagem sobre o que foi feito |
| Desafio extra: pesquisa pelo nome | Campo de busca na lista, que ignora maiúsculas e minúsculas |
| Segundo desafio: confirmação antes de excluir | Página de confirmação, e o produto só é apagado depois de confirmar |

Além do enunciado, a lista mostra 10 produtos por página e o projeto tem o painel administrativo do Django.

## Telas

| Detalhes | Cadastro | Exclusão |
|---|---|---|
| ![Detalhes](docs/detalhe.png) | ![Cadastro](docs/cadastro.png) | ![Exclusão](docs/exclusao.png) |

## Modelo

| Campo | Tipo | Regra |
|---|---|---|
| `nome` | `CharField(200)` | Obrigatório |
| `descricao` | `TextField` | Opcional |
| `preco` | `DecimalField(10, 2)` | Obrigatório, não aceita valor negativo |
| `estoque` | `PositiveIntegerField` | Obrigatório, só números inteiros a partir de 0 |
| `imagem` | `ImageField` | Opcional |

Quando a imagem de um produto é trocada, ou o produto é excluído, o arquivo antigo também é apagado da pasta `media/`. Assim não sobram imagens sem dono.

## Rotas

| URL | O que faz |
|---|---|
| `/` | Lista, com busca (`?busca=`) e páginas (`?pagina=`) |
| `/produto/<id>/` | Detalhes de um produto |
| `/cadastrar/` | Novo produto |
| `/editar/<id>/` | Edição |
| `/excluir/<id>/` | Pede confirmação (GET) e exclui (POST) |
| `/admin/` | Painel administrativo |

## Como rodar

Requer Python 3.12 ou mais recente.

```bash
python -m venv venv
source venv/bin/activate        # no Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # opcional, para usar o /admin/
python manage.py runserver
```

Depois é só abrir http://127.0.0.1:8000/.

A `SECRET_KEY` e o modo de depuração podem ser definidos pelas variáveis de ambiente `DJANGO_SECRET_KEY` e `DJANGO_DEBUG`. Sem elas, o projeto usa uma chave de desenvolvimento e roda com `DEBUG` ligado, o que só serve para uso local.

## Testes

```bash
python manage.py test
```

São 10 testes: listagem com o preço no formato brasileiro, busca, paginação, cadastro com imagem, nome obrigatório, estoque inteiro, preço e estoque negativos, edição, troca de imagem apagando o arquivo antigo e exclusão em duas etapas apagando a imagem.

## Estrutura

```
cadastro-produtos-django/
├── config/            # configurações e URLs do projeto
├── produtos/          # modelo, formulário, views, templates, CSS e testes
├── docs/              # capturas de tela
├── manage.py
└── requirements.txt
```

## O que eu faria diferente hoje

Revisei o projeto depois da entrega. Troquei o estoque para `PositiveIntegerField` e coloquei um valor mínimo no preço, passei a apagar as imagens antigas, acrescentei a paginação e os testes e refiz o visual das telas de um jeito mais simples. Ainda daria para melhorar:

- **Login.** Hoje qualquer pessoa com acesso ao site pode cadastrar e excluir. Eu exigiria login nas telas que alteram dados.
- **Views baseadas em classe.** `ListView`, `CreateView`, `UpdateView` e `DeleteView` fariam o mesmo CRUD com menos código.
- **Tamanho das imagens.** O upload aceita qualquer tamanho. Eu limitaria o tamanho do arquivo e reduziria a imagem ao salvar.

---

Desenvolvido por **Isadora Fernanda Zappe Schmidt** · [LinkedIn](https://www.linkedin.com/in/isadora-fernanda)
