# calendar_bot

Python script that reads Google Calendar and sends Telegram group notifications about events 1 day, 1 week and 2 weeks ahead. All code lives in `calendar_bot.py`.

## Run

- Locally: `pip install -r requirements.txt && python calendar_bot.py` (requires `.env`).
- Docker: `docker compose up -d --build`. Inside the container, cron runs the script once a day at 00:00 (see `Dockerfile`).
- Edit dependencies in `requirements.in`, then regenerate `requirements.txt`.

## Rules

- The script is one-shot (run by cron), not a long-running service.
- Messages use `parse_mode=MarkdownV2`: pass every dynamic value through `escape_markdown_v2`, otherwise Telegram returns HTTP 400.
- Secrets (`GOOGLE_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_GROUP_ID`, `CALENDAR_ID`) come only from the environment or `.env`. Never hardcode or log them, never commit `.env`.
- There are no tests: verify by running against a test calendar and a test Telegram group.
- Code comments, README and bot messages are in Russian.

## OpenSpec

Changes go through OpenSpec: `/opsx:propose`, `/opsx:apply`, `/opsx:archive`. Context and artifact rules are in `openspec/config.yaml`.
