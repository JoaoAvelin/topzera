from rest_framework import serializers
from .models import Categoria, Produto, Cliente, ItemPedido, Pedido, CupomDesconto
from django.contrib.auth.models import User


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'


class ProdutoSerializer(serializers.ModelSerializer):
    categoria = CategoriaSerializer(read_only=True)
    categoria_id = serializers.PrimaryKeyRelatedField(
        queryset=Categoria.objects.all(), write_only=True
    )

    class Meta:
        model = Produto
        fields = '__all__'

    def create(self, validated_data):
        categoria = validated_data.pop('categoria_id')
        return Produto.objects.create(categoria=categoria, **validated_data)

    def update(self, instance, validated_data):
        categoria = validated_data.pop('categoria_id', None)
        if categoria:
            instance.categoria = categoria
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ClienteSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Cliente
        fields = ['id', 'username', 'email', 'cpf', 'telefone', 'endereco']


class CupomDescontoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CupomDesconto
        fields = ['id', 'codigo', 'desconto_percentual', 'ativo']


class ItemPedidoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.ReadOnlyField(source='produto.nome')
    cupom_codigo = serializers.CharField(write_only=True, required=False, allow_blank=True)
    preco_com_desconto = serializers.SerializerMethodField()
    cupom = CupomDescontoSerializer(read_only=True)

    class Meta:
        model = ItemPedido
        fields = [
            'id', 'produto', 'produto_nome', 'quantidade', 'preco',
            'cupom_codigo', 'preco_com_desconto', 'cupom'
        ]

    def get_preco_com_desconto(self, obj):
        return obj.preco_com_desconto()

    def validate(self, data):
        if data['quantidade'] <= 0:
            raise serializers.ValidationError("A quantidade deve ser maior que zero.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        cliente = getattr(user, 'cliente', None)
        if not cliente:
            raise serializers.ValidationError("Apenas clientes podem criar itens de pedido.")

        codigo = validated_data.pop('cupom_codigo', None)
        cupom = None
        if codigo:
            try:
                cupom = CupomDesconto.objects.get(codigo=codigo, ativo=True)
            except CupomDesconto.DoesNotExist:
                raise serializers.ValidationError({"cupom_codigo": "Cupom inválido ou inativo."})

        pedido, _ = Pedido.objects.get_or_create(cliente=cliente, status='pendente')

        item = ItemPedido.objects.create(
            pedido=pedido,
            cupom=cupom,
            **validated_data
        )

        self._atualizar_total_pedido(pedido)

        return item

    def update(self, instance, validated_data):
        codigo = validated_data.pop('cupom_codigo', None)

        if codigo == "":
            instance.cupom = None  # Remove cupom
        elif codigo:
            try:
                cupom = CupomDesconto.objects.get(codigo=codigo, ativo=True)
                instance.cupom = cupom
            except CupomDesconto.DoesNotExist:
                raise serializers.ValidationError({"cupom_codigo": "Cupom inválido ou inativo."})

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        self._atualizar_total_pedido(instance.pedido)

        return instance

    def _atualizar_total_pedido(self, pedido):
        total = sum(i.preco_com_desconto() * i.quantidade for i in pedido.itens.all())
        pedido.total = total
        pedido.save()


class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True, read_only=True)
    cliente_username = serializers.ReadOnlyField(source='cliente.user.username')

    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'cliente_username', 'data_pedido', 'status', 'total', 'itens']
        read_only_fields = ['cliente', 'data_pedido', 'total']

    def create(self, validated_data):
        itens_data = validated_data.pop('itens', [])
        cliente = self.context['request'].user.cliente

        pedido = Pedido.objects.create(cliente=cliente)
        total = 0

        for item_data in itens_data:
            produto = item_data['produto']
            quantidade = item_data['quantidade']
            preco = produto.preco

            ItemPedido.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=quantidade,
                preco=preco
            )

            total += preco * quantidade

        pedido.total = total
        pedido.save()
        return pedido


class CadastroClienteSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    email = serializers.EmailField(source='user.email')
    password = serializers.CharField(write_only=True, source='user.password')

    class Meta:
        model = Cliente
        fields = ['username', 'email', 'password', 'cpf', 'telefone', 'endereco']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.create_user(**user_data)
        return Cliente.objects.create(user=user, **validated_data)
