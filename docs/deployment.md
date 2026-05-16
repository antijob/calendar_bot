# Deployment

The bot runs once per execution and is intended to be triggered on a schedule (cron). The Docker image sets up a daily cron job automatically.

## Docker (recommended)

```bash
# Build and start
docker-compose up -d

# View logs
docker logs -f scheduler

# Stop
docker-compose down
```

The container runs `calendar_bot.py` every day at midnight via cron. Logs are written to `/var/log/cron.log` inside the container.

## Systemd timer (alternative)

Create `/etc/systemd/system/calendar-bot.service`:

```ini
[Unit]
Description=antijob calendar bot

[Service]
Type=oneshot
WorkingDirectory=/opt/antijob_calendar
EnvironmentFile=/opt/antijob_calendar/.env
ExecStart=/opt/antijob_calendar/venv/bin/python calendar_bot.py
```

Create `/etc/systemd/system/calendar-bot.timer`:

```ini
[Unit]
Description=Run antijob calendar bot daily

[Timer]
OnCalendar=daily
Persistent=true

[Install]
WantedBy=timers.target
```

```bash
systemctl daemon-reload
systemctl enable --now calendar-bot.timer
```

## Environment variables

Pass all variables from `.env.example` to the container or service. Never commit `.env` to version control.
