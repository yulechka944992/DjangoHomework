from django.core.management import call_command
from django.core.management.base import BaseCommand
from catalog.models import Product, Category

class Command(BaseCommand):
    help = 'Add products to the database'

    def handle(self, *args, **options):
        self.stdout.write('Удаляем старые данные...')
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write('Загружаем фикстуру catalog_fixture.json...')
        call_command('loaddata', 'catalog_fixture.json')

        self.stdout.write(self.style.SUCCESS(
            f'Готово! Загружено категорий: {Category.objects.count()}, '
            f'продуктов: {Product.objects.count()}'
        ))