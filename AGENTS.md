# antijob_calendar

Python bot that polls Google Calendar and sends event reminders (1 day, 1 week, 2 weeks ahead) to a Telegram group.

## Essentials

- Package manager: `pip` (pin deps with `pip-compile requirements.in`)
- Install: `pip install -r requirements.txt`
- Run: `python calendar_bot.py`
- Docker: `docker-compose up -d`
- Verify: `bash scripts/verify.sh`
- Check docs: `bash scripts/check-docs.sh`

## Required environment variables

Defined in `.env.example`:

| Variable | Purpose |
|---|---|
| `GOOGLE_API_KEY` | Google Calendar API key |
| `CALENDAR_ID` | Calendar to watch |
| `TELEGRAM_BOT_TOKEN` | Bot token from BotFather |
| `TELEGRAM_GROUP_ID` | Target Telegram group/chat ID |

Copy `.env.example` to `.env` and fill in values before running.

## Docs

- [Setup](docs/setup.md)
- [Configuration](docs/configuration.md)
- [Deployment](docs/deployment.md)
