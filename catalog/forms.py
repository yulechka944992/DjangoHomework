import os
from django import forms
from django.core.exceptions import ValidationError
from .models import Product


FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта', 'биржа',
    'дешево', 'бесплатно', 'обман', 'полиция', 'радар'
]

def validate_no_forbidden_words(text):
    """Проверяет текст на наличие запрещенных слов (без учета регистра)."""
    if text:
        text_lower = text.lower()
        for word in FORBIDDEN_WORDS:
            if word in text_lower:
                raise ValidationError(
                    f'Слово "{word}" запрещено к использованию на нашем сайте.',
                    code='forbidden_word'
                )

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category', 'image']


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

            if field_name == 'name':
                field.widget.attrs['placeholder'] = 'Название товара'
            elif field_name == 'description':
                field.widget.attrs['placeholder'] = 'Описание товара'
            elif field_name == 'price':
                field.widget.attrs['placeholder'] = 'Цена'

    def clean_name(self):
        name = self.cleaned_data.get('name')
        validate_no_forbidden_words(name)
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        validate_no_forbidden_words(description)
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise ValidationError(
                'Цена не может быть отрицательной.',
                code='invalid_price'
            )
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            ext = os.path.splitext(image.name)[1].lower()
            valid_extensions = ['.jpg', '.jpeg', '.png']

            if ext not in valid_extensions:
                raise ValidationError(
                    'Недопустимый формат файла. Разрешены только JPEG и PNG.',
                    code='invalid_image_format'
                )

            max_size = 5 * 1024 * 1024
            if image.size > max_size:
                raise ValidationError(
                    'Размер файла не должен превышать 5 МБ.',
                    code='image_too_large'
                )

        return image
