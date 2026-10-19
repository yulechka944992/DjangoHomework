# DjangoHomework — проект "Catalog"

Учебный Django-проект с приложением `catalog`, реализующий главную страницу 
и страницу контактов с формой обратной связи.

## Описание

Проект создан в рамках выполнения домашнего задания по Django.
Включает в себя:

- Главную страницу — она же каталог товаров (`home`)
- Каталог всех товаров (`product_list`) с пагинацией (по 6 товаров на страницу)
- Детальную страницу товара (`product_detail`) со всей информацией
- Форму добавления нового товара (`product_create`) с валидацией
- Страницу контактов (`contacts`) с формой обратной связи
- Модели `Category`, `Product`, `Contact`
- Регистрацию моделей в админ-панели
- Загрузку и отображение изображений товаров (`Media`)
- Базовый шаблон (`base.html`), вынесенные меню и карточки товаров (`includes/`)
- Обработку POST-запроса от формы контактов
- Вывод последних 5 товаров в консоль сервера
- Вывод контактных данных из БД на страницу `/contacts/`
- Кастомную management-команду для загрузки тестовых данных из фикстуры
- Подключение статических файлов (CSS, JS)

##  Переменные окружения

Все секретные данные (`SECRET_KEY`, параметры БД, режим отладки) вынесены
в файл `.env`, который **не попадает в git**.

### 1. Создать `.env` на основе шаблона:
Скопируйте содержимое файла .env.sample в новый файл .env
в корне проекта и заполните его своими значениями.

* Пример содержимого .env

SECRET_KEY=your-secret-key-here
DEBUG=True

DB_NAME=your_db_name
DB_USER=user_name
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

#### Использование в `settings.py`
```python
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv(override=True)

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = True if os.getenv('DEBUG')=='True' else False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST', 'localhost'),
        'PORT': os.getenv('DATABASE_PORT', '5432'),
    }
}
```
*.gitignore*
Убедитесь, что .env в .gitignore, чтобы секреты не попали в репозиторий:
   - .env
   - *.pyc
   - __pycache__/
   - .venv/
   - media/
   - db.sqlite3
   - .idea/

## 🚀 Установка и запуск

### 1. Клонировать репозиторий

```
git clone https://github.com/yulechka944992/DjangoHomework/tree/feature_django_homework1
cd DjangoHomework
```

### 2. Создать и активировать виртуальное окружение
```

python -m venv .venv
```
Windows:
```
.venv\Scripts\activate
```
Linux / macOS:
```
source .venv/bin/activate
```

### 3. Установить зависимости
```
pip install -r requirements.txt
```

### 4.Настроить переменные окружения

Скопируйте содержимое файла .env.sample в новый файл .env в корне проекта
и заполните его своими значениями (SECRET_KEY, DB_NAME, DB_USER, DB_PASSWORD и т.д.).

Подробнее — в разделе «Переменные окружения».

### 5.Применить миграции
```
python manage.py migrate
```

### 6. Создать суперпользователя (для доступа в админку)
```
python manage.py createsuperuser
```

### 7. Загрузить тестовые данные
```
python manage.py add_products
```
Команда удаляет все существующие данные и загружает фикстуру catalog_fixture.json
(3 категории и 5 товаров).

### 8. Запустить сервер разработки
```
python manage.py runserver
```

### 9.Открыть в браузере
- Главная страница: http://127.0.0.1:8000/home/

- Каталог товаров: http://127.0.0.1:8000/products/

- Добавление товара: http://127.0.0.1:8000/products/create/

- Контакты: http://127.0.0.1:8000/contacts/

- Админ-панель: http://127.0.0.1:8000/admin/

## Модели

Category — категория товаров

    name — наименование категории

    description — описание

Product — товар

    name — наименование продукта

    description — описание продукта

    image — изображение (загружается в media/products/images/)

    price — цена (DecimalField, 10 знаков, 2 после запятой)

    category — внешний ключ на Category (on_delete=CASCADE, related_name='products')

    created_at — дата создания (auto_now_add)

    updated_at — дата последнего изменения (auto_now)

Contact — контактные данные

    email — Email

    phone — телефон

    address — адрес

## Реализованный функционал
*Главная страница (home)*
Отображает 5 последних добавленных товаров. В шаблон передаётся контекст, реализован цикл вывода карточек.

*Каталог (product_list)*
Выводит все товары с помощью Paginator (по 6 штук на страницу). Внизу реализованы кнопки перехода между страницами («Первая», «Назад», «Вперед», «Последняя»).

*Детальная страница товара (product_detail)*
Выводит полную информацию о товаре: название, описание, цена, категория, изображение, даты создания и изменения. Используется get_object_or_404.

*Добавление товара (product_create)*
Форма на основе ModelForm. Включает защиту от ошибок (валидация обязательных полей и типов данных), защиту CSRF, поддерживает загрузку изображений (через request.FILES и enctype="multipart/form-data"). После успешного сохранения перенаправляет в каталог.

*Форма контактов (contacts)*
GET — отображает форму обратной связи. POST — принимает поля name, phone, message и возвращает приветственное сообщение.

*Кастомная команда add_products*
Management-команда, которая удаляет все существующие данные (Product и Category) и загружает фикстуру catalog_fixture.json через call_command('loaddata', ...).

Запуск:
```
python manage.py add_products
```
Пример вывода:

Удаляем старые данные...
Загружаем фикстуру catalog_fixture.json...
Installed 8 object(s) from 1 fixture(s)
Готово! Загружено категорий: 3, продуктов: 5

*Шаблоны*

    base.html — общий каркас (шапка, подвал, стили).

    includes/_menu.html — главное меню.

    includes/_product_card.html — переиспользуемая карточка товара (с обрезкой описания через truncatechars:100).



### Зависимости
Полный список зависимостей — в файле requirements.txt.
Django==6.1.1
psycopg2-binary==2.9.13
python-dotenv==1.2.4
pillow==12.3.0
ipython==9.17.1
black==26.10.1

### Автор
Кряжева Юлия

### Лицензия
Учебный проект.
