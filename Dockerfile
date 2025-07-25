FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

COPY wait-for-it.sh .
RUN chmod +x wait-for-it.sh
# Собираем статические файлы (при сборке контейнера)
RUN python manage.py collectstatic --noinput

CMD ["./wait-for-it.sh", "db:5432", "--", "gunicorn", "referral_system.wsgi:application", "--bind", "0.0.0.0:8000"]
