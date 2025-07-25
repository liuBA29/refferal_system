# 📲 Реферальная система на Django

Тестовое задание для Python-разработчика: реализована простая реферальная система с авторизацией по номеру телефона, генерацией инвайт-кодов и возможностью отслеживания приглашённых пользователей.

## 🚀 Функциональность

- Авторизация по номеру телефона с 4-значным кодом подтверждения
- Создание пользователя при первой авторизации
- Генерация уникального 6-значного инвайт-кода
- Возможность один раз активировать чужой инвайт-код
- Отображение активированного кода в профиле
- Отображение списка пользователей, которые ввели твой инвайт-код
- Интерфейс на Django Templates (минимальный)
- API-документация (опционально ReDoc)
- Docker + docker-compose
- Postman коллекция для тестирования

---

## 🧱 Технологии

- Python 3.11+
- Django 5.2
- Django REST Framework
- Docker, docker-compose
- PostgreSQL
- Django Templates

---

## 🧪 Установка и запуск

### 🔧 Локально без Docker:

```bash
git clone https://github.com/liuBA29/refferal_system.git
cd refferal_system
python -m venv venv
source venv/bin/activate   # для Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### 🐳 С Docker:

```bash
git clone https://github.com/liuBA29/refferal_system.git
cd refferal_system
docker-compose up --build -d
```

> Проект выложен на сайте:  
> `http://testsite.web.cloudcenter.ovh/`  
> Там можно тестировать API и пользоваться интерфейсом напрямую, без локального запуска.

---

## 🔐 Авторизация

### 1. 📲 Запрос кода  
`POST /api/request-code/`

Пример запроса:
```json
{
  "phone_number": "+375291112233"
}
```

✅ Ответ: 200 OK, с задержкой 2 секунды. Код подтверждения будет выведен в консоль:
- При локальной установке — в командной строке.
- При использовании Docker — доступен через логи контейнера.

---

### 2. 🔑 Подтверждение кода  
`POST /api/verify-code/`

Пример запроса:
```json
{
  "phone_number": "+375291112233",
  "code": "1234"
}
```

✅ Ответ: пользователь будет создан или подтверждён. Привязка по заголовку `X-Phone-Number`.

---

## 👤 Профиль пользователя  
`GET /api/profile/`

🔸 Заголовок: `X-Phone-Number: +375291112233`

Пример ответа:
```json
{
  "phone_number": "+375291112233",
  "invite_code": "2HG6KJ",
  "activated_code": "A2D91B",
  "invited_users": ["+375296667788", "+375299998877"]
}
```

---

## ✏️ Активация чужого инвайт-кода  
`POST /profile/activate-invite/`

🔸 Заголовок: `X-Phone-Number: +375291112233`

Пример запроса:
```json
{
  "code": "A2D91B"
}
```

✅ Ответ: 200 OK  
🚫 Повторная попытка: 400 — Code already activated

---

## 🌐 Интерфейс

Доступен по адресу:  
`http://127.0.0.1:8000/` — при локальном запуске и при работе через Docker

Позволяет:
- Ввести номер телефона
- Увидеть код подтверждения:
   - при запуске локально — код выводится прямо в консоли (терминале)
   - при запуске через Docker — код можно увидеть через команду `docker logs <container_name>`
- Подтвердить код
- Посмотреть профиль
- Ввести инвайт-код вручную

---

## 📦 Postman коллекция

Файл `postman_collection.json` лежит в корне проекта — импортируйте его в Postman для тестирования всех API-эндпоинтов.

Для тестирования также можно использовать сайт:  
`http://testsite.web.cloudcenter.ovh/`

---

## ✅ Дополнительно

- Мини-интерфейс на Django Templates  
- Docker-окружение  
- Postman коллекция  


---

## ✍️ Автор

**Liubov Kovaleva** (@liuBA29)  
📧 luba.sentino@gmail.com