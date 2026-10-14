from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProdutoForm
from .models import Produto


def lista_produtos(request):
    busca = request.GET.get('busca', '')

    produtos = Produto.objects.all().order_by('nome')

    if busca:
        produtos = produtos.filter(nome__icontains=busca)

    return render(request, 'produtos/lista.html', {
        'produtos': produtos,
        'busca': busca,
    })


def detalhe_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    return render(request, 'produtos/detalhe.html', {
        'produto': produto,
    })


def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Produto cadastrado com sucesso!'
            )
            return redirect('lista_produtos')

    else:
        form = ProdutoForm()

    return render(request, 'produtos/form.html', {
        'form': form,
        'titulo': 'Cadastrar Produto',
    })


def editar_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        form = ProdutoForm(
            request.POST,
            request.FILES,
            instance=produto
        )

        if form.is_valid():
            form.save()
            messages.success(
                request,
                'Produto atualizado com sucesso!'
            )
            return redirect('lista_produtos')

    else:
        form = ProdutoForm(instance=produto)

    return render(request, 'produtos/form.html', {
        'form': form,
        'titulo': 'Editar Produto',
        'produto': produto,
    })


def excluir_produto(request, id):
    produto = get_object_or_404(Produto, id=id)

    if request.method == 'POST':
        produto.delete()

        messages.success(
            request,
            'Produto excluído com sucesso!'
        )

        return redirect('lista_produtos')

    return render(request, 'produtos/confirmar_exclusao.html', {
        'produto': produto,
    })
