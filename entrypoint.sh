#!/bin/sh
# Cron запускает задания с пустым окружением, поэтому сохраняем конфигурацию
# контейнера в /app/.env (его читает load_dotenv() в calendar_bot.py).
# Значения не выводим в лог.
set -eu
umask 077

: > /app/.env
for name in GOOGLE_API_KEY TELEGRAM_BOT_TOKEN TELEGRAM_GROUP_ID CALENDAR_ID; do
    eval "value=\${$name-}"
    printf '%s="%s"\n' "$name" "$value" >> /app/.env
done

# exec оставляет cron процессом PID 1 (нужно для вывода в /proc/1/fd/*)
exec cron -f
