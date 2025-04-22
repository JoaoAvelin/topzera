from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Admin').exists()

class IsGestor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Gestor').exists()

class IsFuncionario(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='Funcionario').exists()

class PermissaoProdutoPorGrupo(permissions.BasePermission):
    """
    - Admin e Gestor têm acesso total
    - Funcionário tem acesso somente leitura (GET, HEAD, OPTIONS)
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name__in=['Admin', 'Gestor', 'Funcionario']).exists()

        return request.user.groups.filter(name__in=['Admin', 'Gestor']).exists()

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class PermissaoCategoriaPorGrupo(permissions.BasePermission):
    """
    - Admin e Gestor têm acesso total
    - Funcionário tem acesso somente leitura (GET, HEAD, OPTIONS)
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name__in=['Admin', 'Gestor', 'Funcionario']).exists()

        return request.user.groups.filter(name__in=['Admin', 'Gestor']).exists()

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)

class PermissaoClientePorGrupo(permissions.BasePermission):
    """
    - Admin e Gestor têm acesso total
    - Funcionário tem acesso somente leitura (GET, HEAD, OPTIONS)
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.groups.filter(name__in=['Admin', 'Gestor', 'Funcionario']).exists()

        return request.user.groups.filter(name__in=['Admin', 'Gestor']).exists()

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)
