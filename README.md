# ai_store_backend

Данный проект является частью программной инфраструктуры ai_store. Это веб-приложение обеспечивает клиенту доступ к ИС и другим веб-приложениям.

## Рекомендации по разработке

При разработке проекта используется автоформатировщик кода Black (https://pypi.org/project/black/)

## Параметры пользователей

Пользовательские имена и электронные почтовые ящики не могут длиннее 255 символов.
Пользовательские пароли не могут быть короче 8 и длиннее 128 символов.

# REST API

Документация:
1) */api/swagger/ (GUI в стиле Swagger)

Другие форматы документации:
2) */api/swagger/?format=.json (Файл в формате json)
3) */api/swagger/?format=.yaml (Файл в формате yaml)
4) */api/redoc/ (GUI в стиле ReDoc)
5) */api/redoc-old/ (GUI в стиле ReDoc 1.x.x)
6) */api/cached/swagger(?format=.json (Кэшированный файл в формате json)
7) */api/cached/swagger(?format=.yaml (Кэшированный файл в формате yaml)
8) */api/cached/swagger/ (Кэшированное GUI в стиле Swagger)
9) */api/cached/redoc/ (Кэшированное GUI в стиле ReDoc)

## Create user

### Request:

`POST */api/v1/users/`

#### Body:

```json
{
    "user": {
        "username": "user1",
        "email": "user1@user.user",
        "password": "*"
    }
}
```

### Response:

`HTTP/1.1 201 Created`

#### Cookie:

```refresh_token=*; Path=/; HttpOnly; Expires=ddd, dd mmm yyyy hh:mm:ss GMT```

#### Body:

```json
{
    "user": {
        "email": "user1@user.user",
        "username": "user1",
        "token": "*",
        "logo": "/media/default/auth/default.jpg"
    }
}
```

## Login

`POST */api/v1/users/login/`

### Request:

#### Body:

```json
{
    "user": {
        "email": "user1@user.user",
        "password": "*"
    }
}
```

### Response:

`HTTP/1.1 200 OK`

#### Cookie:

```refresh_token=*; Path=/; HttpOnly; Expires=ddd, dd mmm yyyy hh:mm:ss GMT```

#### Body:

```json
{
    "user": {
        "email": "user1@user.user",
        "username": "user1",
        "token": "*",
        "logo": "/media/default/auth/default.jpg"
    }
}
```

## Get current user 

`GET: */api/v1/user/`

### Request:

#### Header:

`Authorization: Bearer *`

### Response:

`HTTP/1.1 200 OK`

#### Body:

```json
{
    "user": {
        "email": "user1@user.user",
        "username": "user1",
        "logo": "/media/default/auth/default.jpg"
    }
}
```

## Update user 

`PATCH: */api/v1/user/`

### Request:

#### Header:

`Authorization: Bearer *`

#### Body:

```json
{
    "user": {
        "email": "new_user1@user.user",
        "username": "new_user1",
        "password": "*"
    }
}
```

### Response:

`HTTP/1.1 200 OK`

#### Body:

```json
{
    "user": {
        "email": "user1@user.user",
        "username": "user1",
        "logo": "/media/default/auth/default.jpg"
    }
}
```

## Resfresh token

`POST: */api/v1/users/refresh/`

### Request:

#### Cookie:
```refresh_token=*; Path=/; HttpOnly; Expires=ddd, dd mmm yyyy hh:mm:ss GMT```

### Response (HTTP 200 OK):

`HTTP/1.1 200 OK`

#### Cookie:

```refresh_token=*; Path=/; HttpOnly; Expires=ddd, dd mmm yyyy hh:mm:ss GMT```

#### Body:

```json
{
    "user": {
        "token": "*"
    }
}
```
## Upload logo

`POST: */api/v1/user/logo/`

### Request:

#### Header:

```
Authorization: Bearer *
Content-Type: multipart/form-data; boundary=*
```

#### Body:

##### TypeScript:

```typescript
// FormData: append(name: string, value: string | Blob, fileName?: string): void
const formData = new FormData()
formData.append("logo", file)
```

##### Raw:
```
------*
Content-Disposition: form-data; name="logo"; filename="*"
Content-Type: *

(file)
------*
```

### Response:

`HTTP/1.1 200 OK`

#### Body:

```json
{
    "logo": "*"
}
```

## Upload neural network

`POST: */api/v1/neural_networks/` 

### Request:

#### Header:

`Authorization: Bearer *`

#### Body:

```json
{
    "neural_network": {
        "name": "nn_name",
        "summary": "...",
        "desc": "...",
        "instruction": "...",
        "is_hidden": false
    }
}
```

### Response:

`HTTP/1.1 201 Created`

#### Body:

```json
{
    "neural_network": {
        "id": 1234,
        "name": "nn_name",
        "summary": "...",
        "desc": "...",
        "instruction": "...",
        "logo": "/media/default/neural_network/default.jpg",
        "is_hidden": false,
        "author": {
            "email": "new_user1@user.user",
            "username": "new_user1"
        }
    }
}
```

## Get neural network 

`GET: */api/v1/neural_networks/<id>/`

### Response:

`HTTP/1.1 200 OK`

#### Body:

```json
{
    "neural_network": {
        "id": 1234,
        "name": "nn_name",
        "summary": "...",
        "desc": "...",
        "instruction": "...",
        "logo": "/media/default/neural_network/default.jpg",
        "is_hidden": false,
        "author": {
            "email": "new_user1@user.user",
            "username": "new_user1"
        }
    }
}
```

## Get neural networks

`GET: */api/v1/neural_networks/`

### Request:

#### Header:

##### (Optional. For hidden NN):

`Auhorization: Bearer *`

### Response:

`HTTP/1.1 200 OK`

#### Body:

```json
{
    "neural_networks": [
        {
            "id": 1234,
            "name": "nn_name",
            "summary": "...",
            "desc": "...",
            "instruction": "...",
            "logo": "/media/default/neural_network/default.jpg",
            "is_hidden": false,
            "author": {
                "email": "new_user1@user.user",
                "username": "new_user1"
            }
        }
    ]
}
```

## Get neural networks of author 

`GET: */api/v1/neural_networks/author_list/`

### Request:

#### Header:

`Authorization: Bearer *`

### Response:

`HTTP/1.1 200 OK`

#### Body:

```json
{
    "neural_networks": [
        {
            "id": 1234,
            "name": "nn_name",
            "summary": "...",
            "desc": "...",
            "instruction": "...",
            "logo": "/media/default/neural_network/default.jpg",
            "is_hidden": false,
            "author": {
                "email": "new_user1@user.user",
                "username": "new_user1"
            }
        }
    ]
}
```

## Update neural network

`PATCH: */api/v1/neural_networks/<id>/`

### Request:

#### Header:

`Authorization: Bearer *`

#### Body:

```json
{
    "neural_network": {
        "name": "nn_name",
        "summary": "...",
        "desc": "...",
        "instruction": "...",
        "is_hidden": false
    }
}
```

### Response:

`HTTP/1.1 200 OK`

#### Body:

```json
{
    "neural_network": {
        "id": 1234,
        "name": "nn_name",
        "summary": "...",
        "desc": "...",
        "instruction": "...",
        "logo": "/media/default/neural_network/default.jpg",
        "is_hidden": false,
        "author": {
            "email": "new_user1@user.user",
            "username": "new_user1"
        }
    }
}
```

## Upload neural network's logo

`POST */api/v1/neural_networks/<id>/logo/`

### Request:

#### Header:

```
Authorization: Bearer *
Content-Type: multipart/form-data; boundary=*
```

#### Body:

##### TypeScript:

```typescript
// FormData: append(name: string, value: string | Blob, fileName?: string): void
const formData = new FormData()
formData.append("logo", file)
```

##### Raw:
```
------*
Content-Disposition: form-data; name="logo"; filename="*"
Content-Type: *

(file)
------*
```

### Response:

`HTTP/1.1 200 OK`

#### Body:

```json
{
    "neural_network": {
        "id": 1234,
        "name": "nn_name",
        "summary": "...",
        "desc": "...",
        "instruction": "...",
        "logo": "/media/neural_network/yyyy/dd/mm/filename_*.jpg",
        "is_hidden": false,
        "author": {
            "email": "new_user1@user.user",
            "username": "new_user1"
        }
    }
}
```

## Delete neural network

`DELETE: */api/v1/neural_networks/<id>/`

### Request:

#### Header:

`Authorization: Bearer *`

### Response:

`HTTP/1.1 204 No content`
# Развёртывание проекта

1) Клонировать репозиторий
2) Добавить файл переменных среды (.env file)
3) Установить Python 3.11.4
4) Обновить pip: python -m pip install --upgrade pip
5) Установить зависимости с помощью файла зависимостей (requirements.txt): python -m pip install -r requirements.txt
6) Запустить миграции БД: python manage.py migrate
7) Подготовить все статичные файлы: python manage.py collectstatic
8) Запустить веб-приложение: python manage.py runserver

## Параметры окружения:

#### Для удобства разработки параметры безопасности по умолчанию **отключены**. Но при развёртывании проекта на боевом сервере необходимо передавать через **ai_store_back/\*.env файл** (*Шаблон: ai_store_back/.env.example*) следующие параметры:
    1) *SECRET_KEY* - ключ для криптографической подписи ([сайт-генератор](https://djecrety.ir))
    2) *DEBUG* (по умолчанию: True) - Включен ли режим отладки?
    3) *CSRF_COOKIE_SECURE* (по умолчанию: False) - CSRF куки файлы - безопасны (переданы по HTTPS)?
    4) *SESSION_COOKIE_SECURE* (по умолчанию: False) - Куки файлы сеанса - безопасны (переданы по HTTPS)?
    5) *SECURE_SSL_REDIRECT* (по умолчанию: False) - Перенаправить все запросы на HTTPS (за исключением URL в SecurityMiddleware: SECURE_REDIRECT_EXEMPT)?
    6) *SECURE_HSTS_SECONDS* (по умолчанию: 1 год)) - срок действия HSTS заголовка
    7) *SECURE_HSTS_INCLUDE_SUBDOMAINS* (по умолчанию: False) - включать ли поддомены в HSTS-заголовок?
    8) *SECURE_HSTS_PRELOAD* (по умолчанию: False) - Добавлять ли сайта в в список прдверительной загрузки для HSTS?
    9) *SECURE_CONTENT_TYPE_NOSNIFF* (по умолчанию: False) - Запретить браузерам "угадывать" (небезопасно преобразовывать) тип содержимого Content-Type?
    10) *JWT_VALIDITY_PERIOD_IN_DAYS* (по умолчанию: 1 день) - Время действия токена доступа в днях
    10) *RT_VALIDITY_PERIOD_IN_DAYS* (по умолчанию: 7 дней) - Время действия токена обновления в днях
    11) *JWT_ENCRYPTION_ALGORITHM* (по умолчанию: HS256) - Алгоритм шифрования токенов по умолчанию (https://pyjwt.readthedocs.io/en/latest/algorithms.html)