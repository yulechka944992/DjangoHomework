from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product


class Command(BaseCommand):
    help = 'Создает группу "Модератор продуктов" и назначает ей права'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name='Модератор продуктов')

        content_type = ContentType.objects.get_for_model(Product)

        permission_unpublish = Permission.objects.get(
            codename='can_unpublish_product',
            content_type=content_type
        )
        permission_delete = Permission.objects.get(
            codename='delete_product',
            content_type=content_type
        )

        group.permissions.add(permission_unpublish, permission_delete)

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Модератор продуктов" успешно создана!'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Модератор продуктов" уже существует. Права обновлены.'))

        self.stdout.write(self.style.SUCCESS('Права на отмену публикации и удаление назначены.'))