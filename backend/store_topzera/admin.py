from django.contrib import admin
from .models import Categoria, Produto, Cliente

# Customizações dos modelos
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'cpf', 'telefone']
    search_fields = ['user__username', 'cpf']

class ProdutoAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome', 'descricao', 'preco', 'estoque']
    search_fields = ['nome', 'descricao']
    list_filter = ['estoque']

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id', 'nome']
    search_fields = ['nome']

# Registro dos modelos com suas respectivas configurações
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Categoria, CategoriaAdmin)
