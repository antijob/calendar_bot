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

The container runs `calendar_bot.py` every day at midnight via cron. The output of every run (stdout and stderr) goes to the container logs, so `docker logs scheduler` shows it.

## Docker Swarm (production)

The `deploy` job in `.github/workflows/deployment.yml` runs a single `docker stack deploy --resolve-image always` with `docker-compose.prod.yml`. Swarm performs one rolling update of `antijob_calendar_scheduler`; the workflow does not call `docker service update` afterwards, because a second update started while the first one is still running fails with `update out of sequence`.

Deployments to production never run in parallel: a second deployment waits for the running one instead of cancelling it.

To restart the service when the image tag has not changed, run the workflow manually with `Force build`, which builds and pushes a new image.

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
