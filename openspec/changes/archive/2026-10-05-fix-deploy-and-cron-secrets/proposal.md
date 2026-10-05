# Proposal

## Why

Деплой в Swarm падает с `update out of sequence`: после `docker stack deploy` workflow сразу делает `docker service update --force`, пока первое обновление ещё идёт. Кроме того, образ с логированием и передачей окружения в cron (коммит `6daa0f9`) в продакшене не получит секреты: там они задаются как `GOOGLE_API_KEY_FILE` и `TELEGRAM_BOT_TOKEN_FILE`, а `entrypoint.sh` сохраняет для cron только прямые значения переменных. Наконец, ошибки Google API и Telegram выводятся вместе с URL запроса, в котором есть ключ API или токен бота, и теперь они попадают в `docker logs`.

## What Changes

- Деплой обновляет сервис один раз: лишний `docker service update --force` убирается, параллельные деплои не запускаются.
- `entrypoint.sh` сохраняет для cron также `GOOGLE_API_KEY_FILE` и `TELEGRAM_BOT_TOKEN_FILE`, поэтому бот читает секреты из Swarm secrets при запуске по cron.
- Необработанная ошибка запуска бота выводится в логи без значений секретов (ключа API, токена бота).
- Тесты на редактирование секретов в выводе ошибок и обновление `docs/deployment.md` и `docs/configuration.md`.

Вне объёма:
- Ротация секретов и схема именования Swarm secrets (`secret.NAME.<hash>`).
- Изменение расписания, логики уведомлений и формата сообщений.
- Структурированное логирование, временные метки, ротация логов контейнера.
- Закрытие ручной проверки 3.x из change `docker-container-logs`.

## Capabilities

### New Capabilities
- `production-deployment`: выкладка новой версии бота в Swarm проходит без конфликта обновлений сервиса.
- `secret-handling`: секреты, переданные файлами или переменными, доступны запускам по расписанию и не раскрываются в выводе ошибок.

### Modified Capabilities

## Impact

- `.github/workflows/deployment.yml`: шаг деплоя, блок `concurrency`.
- `entrypoint.sh`: список сохраняемых переменных.
- `calendar_bot.py`: обработка необработанных исключений при запуске.
- `tests/test_calendar_bot.py`, `docs/deployment.md`, `docs/configuration.md`.
- Зависимость от change `docker-container-logs`: `entrypoint.sh` и логирование появились в нём, и он ещё не заархивирован. Разумно заархивировать его первым.
