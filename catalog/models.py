from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование продукта")
    description = models.TextField(verbose_name="Описание продукта")
    image = models.ImageField(
        upload_to="products/images", verbose_name="Изображение", null=True, blank=True
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Категория",
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Цена", default=0
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name="Дата последнего изменения"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "продукт"
        verbose_name_plural = "продукты"
        ordering = ["name"]


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Наименование категории")
    description = models.TextField(
        verbose_name="Описание категории", null=True, blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"
        ordering = ["name"]


class Contact(models.Model):
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    address = models.CharField(max_length=200, verbose_name='Адрес')

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Контакт'
        verbose_name_plural = 'Контакты'
