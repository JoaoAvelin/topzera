from django.db import models
from django.contrib.auth.models import User

class CupomDesconto(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    desconto_percentual = models.DecimalField(max_digits=5, decimal_places=2)
    ativo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo} - {self.desconto_percentual}%"

class Categoria(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    estoque = models.PositiveIntegerField()
    imagem = models.ImageField(upload_to='produtos/', blank=True, null=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='produtos')

    def __str__(self):
        return self.nome

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    endereco = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Pedido(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('enviado', 'Enviado'),
        ('concluido', 'Concluído'),
        ('cancelado', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    data_pedido = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Pedido {self.id} - {getattr(self.cliente.user, "username", str(self.cliente))}'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, related_name='itens', on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    cupom = models.ForeignKey(CupomDesconto, on_delete=models.SET_NULL, null=True, blank=True)

    def preco_com_desconto(self):
        if self.cupom and self.cupom.ativo:
            return self.preco * (1 - self.cupom.desconto_percentual / 100)
        return self.preco

    def get_total(self):
        return self.preco_com_desconto() * self.quantidade
