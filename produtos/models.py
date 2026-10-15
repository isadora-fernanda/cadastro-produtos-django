from django.core.validators import MinValueValidator
from django.db import models


class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    estoque = models.PositiveIntegerField()
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

    def save(self, *args, **kwargs):
        # Guarda o nome da imagem antiga para apagar o arquivo se ela for trocada ou removida
        imagem_antiga = None
        if self.pk:
            imagem_antiga = Produto.objects.filter(pk=self.pk).values_list('imagem', flat=True).first()

        super().save(*args, **kwargs)

        if imagem_antiga and imagem_antiga != self.imagem.name:
            self.imagem.storage.delete(imagem_antiga)

    def delete(self, *args, **kwargs):
        imagem = self.imagem.name
        resultado = super().delete(*args, **kwargs)
        if imagem:
            self.imagem.storage.delete(imagem)
        return resultado
