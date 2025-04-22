from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet, CategoriaViewSet, ClienteViewSet, rota_protegida, ProfileView

router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet)
router.register(r'categorias', CategoriaViewSet)
router.register(r'clientes', ClienteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('rota-protegida/', rota_protegida, name='rota-protegida'),
    path('profile/', ProfileView.as_view(), name='profile'),
]
