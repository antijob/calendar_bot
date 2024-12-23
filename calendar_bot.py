import os
import requests
from googleapiclient.discovery import build
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta

# Загружаем переменные окружения из .env файла
load_dotenv()

# Получаем значения из .env файла
API_KEY = os.getenv("GOOGLE_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_GROUP_ID = os.getenv("TELEGRAM_GROUP_ID")
CALENDAR_ID = os.getenv("CALENDAR_ID")

# Функция для отправки сообщения в Telegram


def escape_markdown_v2(text):
    escape_chars = r"_*[]()~`>#+-=|{}.!"
    return "".join(f"\\{char}" if char in escape_chars else char for char in text)


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_GROUP_ID,
            "text": message, "parse_mode": "MarkdownV2"}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Сообщение отправлено в Telegram группу")
    else:
        print(f"Ошибка при отправке сообщения: {response.status_code}")
        print(f"Ответ Telegram API: {response.text}")


# Функция для получения ближайших событий из Google Calendar


def get_calendar_events():
    service = build("calendar", "v3", developerKey=API_KEY)
    now = datetime.now(timezone.utc).isoformat()
    events_result = (
        service.events()
        .list(
            calendarId=CALENDAR_ID,
            timeMin=now,
            maxResults=100,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    return events_result.get("items", [])


# Фильтруем события по времени: 1 день и 7 дней до события


def filter_events(events):
    one_day_from_now = datetime.now(timezone.utc) + timedelta(days=1)
    one_week_from_now = datetime.now(timezone.utc) + timedelta(days=7)
    two_week_from_now = datetime.now(timezone.utc) + timedelta(days=14)

    events_for_today = []
    events_for_week = []
    events_for_two_week = []

    for event in events:
        start_str = event["start"].get("dateTime", event["start"].get("date"))
        start = datetime.fromisoformat(start_str.replace("Z", "+00:00"))

        # Проверяем, если событие через 1 день
        if one_day_from_now.date() == start.date():
            events_for_today.append(event)

        # Проверяем, если событие через 1 неделю
        if one_week_from_now.date() == start.date():
            events_for_week.append(event)

        # Проверяем, если событие через 2 недели
        if two_week_from_now.date() == start.date():
            events_for_two_week.append(event)

    return events_for_today, events_for_week, events_for_two_week


# Основная функция для получения событий и отправки уведомлений


def main():
    events = get_calendar_events()

    if not events:
        print("Нет предстоящих событий.")
    else:
        events_for_today, events_for_week, events_for_two_week = filter_events(
            events)

        # Отправляем уведомления о событиях за 1 день
        if events_for_today:
            for event in events_for_today:
                start = event["start"].get(
                    "dateTime", event["start"].get("date"))
                description = event.get("description", "Описание отсутствует")
                message = (
                    f"Событие через 1 день:\n"
                    f"*{escape_markdown_v2(event['summary'].strip())}*\n"
                    f"Описание: {escape_markdown_v2(description.strip())}\n"
                    f"Начало: {escape_markdown_v2(start)}"
                )
                send_telegram_message(message)
        else:
            print("Нет событий на завтра.")

        # Отправляем уведомления о событиях за 1 неделю
        if events_for_week:
            for event in events_for_week:
                start = event["start"].get(
                    "dateTime", event["start"].get("date"))
                description = event.get("description", "Описание отсутствует")
                message = (
                    f"Событие через 1 неделю:\n"
                    f"*{escape_markdown_v2(event['summary'].strip())}*\n"
                    f"Описание: {escape_markdown_v2(description.strip())}\n"
                    f"Начало: {escape_markdown_v2(start)}"
                )
                send_telegram_message(message)
        else:
            print("Нет событий через неделю.")

        # Отправляем уведомления о событиях за 2 недели
        if events_for_two_week:
            for event in events_for_two_week:
                start = event["start"].get(
                    "dateTime", event["start"].get("date"))
                description = event.get("description", "Описание отсутствует")
                message = (
                    f"Событие через 2 недели:\n"
                    f"*{escape_markdown_v2(event['summary'].strip())}*\n"
                    f"Описание: {escape_markdown_v2(description.strip())}\n"
                    f"Начало: {escape_markdown_v2(start)}"
                )
                send_telegram_message(message)
        else:
            print("Нет событий через 2 недели.")


# Запуск основного кода
if __name__ == "__main__":
    main()
