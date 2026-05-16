# Configuration

All configuration is loaded from environment variables. Copy `.env.example` to `.env` and populate each value.

## Variables

| Variable | Required | Description |
|---|---|---|
| `GOOGLE_API_KEY` | Yes | API key for Google Calendar API (no OAuth needed for public calendars) |
| `CALENDAR_ID` | Yes | The Google Calendar ID to watch (e.g. `abc@group.calendar.google.com`) |
| `TELEGRAM_BOT_TOKEN` | Yes | Token from BotFather (`123456:ABC-DEF...`) |
| `TELEGRAM_GROUP_ID` | Yes | Numeric chat ID of the Telegram group (negative for groups, e.g. `-1001234567890`) |

## Getting the values

### Google API key

1. Go to [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project → enable **Google Calendar API**.
3. Go to **APIs & Services → Credentials → Create Credentials → API Key**.

### Calendar ID

1. Open Google Calendar → Settings for the calendar.
2. Scroll to **Integrate calendar** → copy **Calendar ID**.

### Telegram bot token

1. Message [@BotFather](https://t.me/BotFather) → `/newbot`.
2. Copy the token it gives you.

### Telegram group ID

1. Add the bot to your group.
2. Call `https://api.telegram.org/bot<TOKEN>/getUpdates` after sending a message in the group.
3. The `chat.id` field (negative number) is the group ID.
