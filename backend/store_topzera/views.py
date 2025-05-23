from django.shortcuts import render
from django.db import transaction
from rest_framework import viewsets, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Produto, Categoria, Cliente, Pedido, ItemPedido
from .serializers import ProdutoSerializer, CategoriaSerializer, ClienteSerializer, PedidoSerializer, ItemPedidoSerializer, CadastroClienteSerializer
from .permissions import IsAdmin, IsGestor, IsFuncionario
from .permissions import (
    PermissaoProdutoPorGrupo,
    PermissaoCategoriaPorGrupo,
    PermissaoClientePorGrupo
)


class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer
    permission_classes = [PermissaoCategoriaPorGrupo]


class ProdutoViewSet(viewsets.ModelViewSet):
    queryset = Produto.objects.all()
    serializer_class = ProdutoSerializer
    permission_classes = [PermissaoProdutoPorGrupo]


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [PermissaoClientePorGrupo]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rota_protegida(request):
    return Response({"mensagem": "Você está autenticado!"})


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email
        })


class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method in ['DELETE', 'PUT', 'PATCH']:
            if self.request.user.groups.filter(name='Admin').exists():
                return [IsAdmin()]
            elif self.request.user.groups.filter(name='Gestor').exists():
                return [IsGestor()]
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Funcionario').exists():
            return Pedido.objects.none()
        elif user.groups.filter(name='Admin').exists() or user.groups.filter(name='Gestor').exists():
            return Pedido.objects.all()
        return Pedido.objects.filter(cliente=user.cliente)  # Clientes veem apenas seus pedidos

    def perform_create(self, serializer):
        cliente = self.request.user.cliente
        serializer.save(cliente=cliente)


class ItemPedidoViewSet(viewsets.ModelViewSet):
    serializer_class = ItemPedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Funcionario').exists():
            return ItemPedido.objects.none()
        return ItemPedido.objects.filter(pedido__cliente=user)

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user

        # Busca ou cria um pedido pendente
        pedido, created = Pedido.objects.get_or_create(
            cliente=user,
            status='pendente'
        )

        produto = serializer.validated_data['produto']
        quantidade = serializer.validated_data['quantidade']
        preco = produto.preco  # puxando preço do modelo Produto

        # Cria o item e salva
        item = serializer.save(pedido=pedido, preco=preco)

        # Atualiza total do pedido
        pedido.total += preco * quantidade
        pedido.save()
    

class CadastroClienteView(generics.CreateAPIView):
    queryset = Cliente.objects.all()
    serializer_class = CadastroClienteSerializer
    permission_classes = []  # Pública (sem autenticação)
