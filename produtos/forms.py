from django import forms
from .models import Produto


class ProdutoForm(forms.ModelForm):

    class Meta:
        model = Produto

        fields = [
            'nome',
            'descricao',
            'preco',
            'estoque',
            'imagem'
        ]

        labels = {
            'nome': 'Nome do produto',
            'descricao': 'Descrição',
            'preco': 'Preço',
            'estoque': 'Estoque',
            'imagem': 'Imagem do produto',
        }

        widgets = {
            'nome': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Digite o nome do produto'
                }
            ),

            'descricao': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Digite uma descrição para o produto',
                    'rows': 5
                }
            ),

            'preco': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': '0,00',
                    'step': '0.01'
                }
            ),

            'estoque': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Quantidade em estoque',
                    'min': '0'
                }
            ),

            'imagem': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }