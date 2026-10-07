# DjangoHomework — проект "Catalog"

Учебный Django-проект с приложением `catalog`, реализующий главную страницу 
и страницу контактов с формой обратной связи.

## Описание

Проект создан в рамках выполнения домашнего задания по Django.
Включает в себя:

- Главную страницу — она же каталог товаров (`home`)
- Страницу контактов (`contacts`) с формой обратной связи
- Обработку POST-запроса от формы контактов
- Подключение статических файлов (CSS, JS)

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

### 4. Запустить сервер разработки
```
python manage.py runserver
```

### 5.Открыть в браузере
- Главная страница: http://127.0.0.1:8000/home/

- Контакты: http://127.0.0.1:8000/contacts/

- Админ-панель: http://127.0.0.1:8000/admin/

## Реализованный функционал
*home(request)*

Отображает главную страницу через шаблон home.html.

*contacts(request)*

    GET — отображает форму обратной связи (contacts.html)

    POST — принимает поля name, phone, message и возвращает
    приветственное сообщение пользователю

### Зависимости
См. файл requirements.txt:
asgiref==3.12.1
Django==6.1.1
sqlparse==0.6.0
tzdata==2026.5

### Автор
Кряжева Юлия

### Лицензия
Учебный проект.
