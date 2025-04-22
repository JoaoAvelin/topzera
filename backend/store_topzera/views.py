from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .models import Produto, Categoria, Cliente
from .serializers import ProdutoSerializer, CategoriaSerializer, ClienteSerializer
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
