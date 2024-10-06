# Используем базовый образ Python
FROM python:3.9-slim

# Устанавливаем зависимости
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем скрипты
COPY . /app

# Устанавливаем cron
RUN apt-get update && apt-get install -y cron

# Добавляем задание в cron для выполнения скрипта каждые 10 минут
RUN echo "0 0 * * *  root /usr/local/bin/python /app/calendar_bot.py >> /var/log/cron.log 2>&1" > /etc/cron.d/calendar_bot

# Даём правильные права на cron задание
RUN chmod 0644 /etc/cron.d/calendar_bot

# Даем права на выполнение скрипта
RUN chmod +x /app/calendar_bot.py

# Создаем лог файл
RUN touch /var/log/cron.log

# Запускаем cron в foreground режиме
CMD ["cron", "-f"]
