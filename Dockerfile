FROM python:3.10

# Установка зависимостей для сборки psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc

# Копируем файлы проекта
WORKDIR /app
COPY . .

# Устанавливаем зависимости из requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт и запускаем приложение
EXPOSE 5000
CMD ["python", "app.py"]
