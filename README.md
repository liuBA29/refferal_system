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

- Python 3.11
- Django 5.2
- Django REST Framework
- Docker, docker-compose
- SQLite (по умолчанию)
- Django Templates

---

## 🧪 Установка и запуск

### 🔧 Локально без Docker:

```bash
git clone https://github.com/yourusername/refferal_system.git
cd refferal_system
python -m venv venv
source venv/bin/activate   # для Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
🐳 С Docker:
bash
Копировать
Редактировать
git clone https://github.com/yourusername/refferal_system.git
cd refferal_system
docker-compose up --build
🔐 Авторизация
1. 📲 Запрос кода
POST /users/api/request-code/

json
Копировать
Редактировать
{
  "phone_number": "+375291112233"
}
✅ Ответ: 200 OK, на сервере сработает задержка 2 секунды и сгенерируется 4-значный код.

2. 🔑 Подтверждение кода
POST /users/api/verify-code/

json
Копировать
Редактировать
{
  "phone_number": "+375291112233",
  "code": "1234"
}
✅ Если код корректный, будет создан или подтверждён пользователь, привязан к сессии по заголовку X-Phone-Number.

👤 Профиль пользователя
GET /users/api/profile/

🔸 Заголовок: X-Phone-Number: +375291112233

✅ Пример ответа:

json
Копировать
Редактировать
{
  "phone_number": "+375291112233",
  "invite_code": "2HG6KJ",
  "activated_code": "A2D91B",
  "invited_users": ["+375296667788", "+375299998877"]
}
✏️ Активация чужого инвайт-кода
POST /users/profile/activate-invite/

🔸 Заголовок: X-Phone-Number: +375291112233

json
Копировать
Редактировать
{
  "code": "A2D91B"
}
✅ Ответ: 200 OK
🚫 Повторная попытка: 400 — Code already activated

🌐 Интерфейс
Доступен по адресу:


Копировать
Редактировать
http://localhost:8000/
(или на порту 4000, если запущено через Docker)

Позволяет:

Ввести номер телефона

Подтвердить код

Посмотреть профиль

Ввести инвайт-код вручную

📦 Postman коллекция
Файл postman_collection.json лежит в корне проекта — импортируйте его в Postman для тестирования всех эндпоинтов.

✅ Дополнительно
 Мини-интерфейс на Django Templates

 Docker-окружение

 Postman коллекция

 (опционально) Документация API через ReDoc

✍️ Автор
Liubov Kovaleva (@liuBA29)
🌍
📧 luba.sentino@gmail.com