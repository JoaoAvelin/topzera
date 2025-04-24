from rest_framework import serializers
from .models import Categoria, Produto, Cliente, ItemPedido, Pedido
from django.contrib.auth.models import User


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'

class ProdutoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)

    class Meta:
        model = Produto
        fields = '__all__'

class ClienteSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Cliente
        fields = ['id', 'username', 'email', 'cpf', 'telefone', 'endereco']

class ItemPedidoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.ReadOnlyField(source='produto.nome')

    class Meta:
        model = ItemPedido
        fields = ['id', 'pedido', 'produto', 'produto_nome', 'quantidade', 'preco']

    def validate(self, data):
        if data['quantidade'] <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")
        return data

class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, read_only=True)
    cliente_username = serializers.ReadOnlyField(source='cliente.username')

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'cliente_username', 'data_pedido', 'status', 'total', 'itens']
        read_only_fields = ['cliente', 'data_pedido', 'total']