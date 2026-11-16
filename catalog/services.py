from django.core.cache import cache
from django.shortcuts import get_object_or_404
from .models import Product, Category

def get_products_by_category(category_id):
    """Сервисная функция: возвращает список всех продуктов в указанной категории"""
    cache_key = f"category_{category_id}"

    products = cache.get(cache_key)

    if products is None:
        get_object_or_404(Category, id=category_id)

        products = list(Product.objects.filter(category_id=category_id))

        cache.set(cache_key, products, timeout=300)

    return products


def get_cached_products_list():
    """Возвращает список всех продуктов (с низкоуровневым кэшированием)."""
    cache_key = 'all_products_list'
    products = cache.get(cache_key)

    if products is None:
        products = list(Product.objects.all().order_by('-created_at'))
        cache.set(cache_key, products, timeout=300)

    return products