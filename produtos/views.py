from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProdutoForm
from .models import Produto

PRODUTOS_POR_PAGINA = 10


def lista_produtos(request):
    busca = request.GET.get('busca', '').strip()
    produtos = Produto.objects.all()
    if busca:
        produtos = produtos.filter(nome__icontains=busca)

    pagina = Paginator(produtos, PRODUTOS_POR_PAGINA).get_page(request.GET.get('pagina'))
    return render(request, 'produtos/lista.html', {'pagina': pagina, 'busca': busca})


def detalhe_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    return render(request, 'produtos/detalhe.html', {'produto': produto})


def cadastrar_produto(request):
    form = ProdutoForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        produto = form.save()
        messages.success(request, f'"{produto.nome}" foi cadastrado.')
        return redirect('lista_produtos')
    return render(request, 'produtos/form.html', {'form': form, 'titulo': 'Novo produto'})


def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    form = ProdutoForm(request.POST or None, request.FILES or None, instance=produto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, f'"{produto.nome}" foi atualizado.')
        return redirect('lista_produtos')
    return render(request, 'produtos/form.html', {'form': form, 'titulo': 'Editar produto', 'produto': produto})


def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)
    if request.method == 'POST':
        nome = produto.nome
        produto.delete()
        messages.success(request, f'"{nome}" foi excluído.')
        return redirect('lista_produtos')
    return render(request, 'produtos/confirmar_exclusao.html', {'produto': produto})
