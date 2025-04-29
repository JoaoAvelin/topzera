from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, CategoriaViewSet, ClienteViewSet, rota_protegida, ProfileView, PedidoViewSet, ItemPedidoViewSet, CadastroClienteView

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'clientes', ClienteViewSet)
router.register(r'pedidos', PedidoViewSet)
router.register(r'itens-pedido', ItemPedidoViewSet, basename='itempedido')

urlpatterns = [
    path('', include(router.urls)),
    path('rota-protegida/', rota_protegida, name='rota-protegida'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('cadastro/', CadastroClienteView.as_view(), name='cadastro_cliente'),
]
