from django.urls import path

from . import views


urlpatterns = [
    path('', views.lista_produtos, name='lista_produtos'),

    path(
        'produto/<int:id>/',
        views.detalhe_produto,
        name='detalhe_produto'
    ),

    path(
        'cadastrar/',
        views.cadastrar_produto,
        name='cadastrar_produto'
    ),

    path(
        'editar/<int:id>/',
        views.editar_produto,
        name='editar_produto'
    ),

    path(
        'excluir/<int:id>/',
        views.excluir_produto,
        name='excluir_produto'
    ),
]
