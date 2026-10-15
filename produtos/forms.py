from django import forms

from .models import Produto


class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'preco', 'estoque', 'imagem']
        labels = {
            'nome': 'Nome',
            'descricao': 'Descrição',
            'preco': 'Preço (R$)',
            'estoque': 'Estoque',
            'imagem': 'Imagem',
        }
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'preco': forms.NumberInput(attrs={'step': '0.01', 'min': '0'}),
            'estoque': forms.NumberInput(attrs={'min': '0'}),
        }
