# Используем базовый образ Python
FROM python:3.9-slim AS build

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# --- runtime ---
FROM python:3.9-slim

WORKDIR /app

# Копируем установленные пакеты из build-стадии
COPY --from=build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Копируем исходный код
COPY calendar_bot.py .

# Устанавливаем cron
RUN apt-get update && apt-get install -y --no-install-recommends cron \
    && rm -rf /var/lib/apt/lists/*

# Добавляем задание в cron для выполнения скрипта каждый день в полночь
# Вывод уходит в stdout/stderr PID 1, чтобы он был виден через docker logs
# (-u нужен, т.к. cron не передаёт заданию ENV PYTHONUNBUFFERED)
RUN echo "0 0 * * *  root /usr/local/bin/python -u /app/calendar_bot.py >> /proc/1/fd/1 2>> /proc/1/fd/2" \
    > /etc/cron.d/calendar_bot \
    && chmod 0644 /etc/cron.d/calendar_bot

ENV PYTHONUNBUFFERED=1

# Entrypoint сохраняет переменные окружения для cron и запускает его в foreground режиме
COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
