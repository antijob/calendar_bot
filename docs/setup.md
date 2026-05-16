# Setup

## Prerequisites

- Python 3.9+
- A Google Cloud project with **Google Calendar API** enabled
- A Telegram bot created via [BotFather](https://t.me/BotFather)

## Local development

```bash
# 1. Clone the repo
git clone <repo-url>
cd antijob_calendar

# 2. Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and fill in environment variables
cp .env.example .env
# Edit .env with your actual values

# 5. Run the bot once
python calendar_bot.py
```

## Updating dependencies

Dependencies are managed with `pip-compile`:

```bash
pip install pip-tools
# Edit requirements.in, then regenerate the lock file:
pip-compile requirements.in
pip install -r requirements.txt
```
