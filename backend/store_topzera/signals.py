# store_topzera/signals.py

from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from .models import Cliente

@receiver(post_migrate)
def create_groups_and_permissions(sender, **kwargs):
    # Definição de grupos e permissões
    groups_permissions = {
        'Admin': ['add', 'change', 'delete', 'view'],
        'Gestor': ['add', 'change', 'view'],
        'Funcionario': ['view'],
    }


    for group_name, actions in groups_permissions.items():
        group, _ = Group.objects.get_or_create(name=group_name)

        for content_type in ContentType.objects.all():
            for action in actions:
                codename = f"{action}_{content_type.model}"
                try:
                    permission = Permission.objects.get(
                        content_type=content_type,
                        codename=codename
                    )
                    group.permissions.add(permission)
                except Permission.DoesNotExist:
                    continue
def criar_cliente_automaticamente(sender, instance, created, **kwargs):
    if created:
        Cliente.objects.create(user=instance)