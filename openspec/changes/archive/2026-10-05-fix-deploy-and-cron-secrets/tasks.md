# Tasks

## 1. Деплой без конфликта обновлений

- [x] 1.1 В `.github/workflows/deployment.yml` удалить шаг `docker service update --force ...` из шага `Deploy stack`. Проверка: `grep -c "service update" .github/workflows/deployment.yml` равно 0, а `docker stack deploy --resolve-image always` остался.
- [x] 1.2 Добавить job `deploy` блок `concurrency: { group: deploy-prod, cancel-in-progress: false }`. Проверка: YAML валиден (`python3 -c "import yaml,sys; yaml.safe_load(open('.github/workflows/deployment.yml'))"`), блок присутствует в job `deploy`.
- [x] 1.3 Описать в `docs/deployment.md`, что деплой делает один `stack deploy`, а принудительный перезапуск выполняется запуском workflow с `Force build`. Проверка: `bash scripts/check-docs.sh` проходит, описание совпадает с workflow.

## 2. Секреты из файлов в cron-задаче

- [x] 2.1 В `entrypoint.sh` добавить `GOOGLE_API_KEY_FILE` и `TELEGRAM_BOT_TOKEN_FILE` в список сохраняемых переменных. Проверка: `sh -n entrypoint.sh`, локальный прогон копии скрипта с временным путём вместо `/app/.env` записывает обе переменные, права файла 600.
- [x] 2.2 Проверить связку на уровне контейнера: запустить тестовый контейнер с `GOOGLE_API_KEY_FILE` и `TELEGRAM_BOT_TOKEN_FILE`, указывающими на временные файлы с тестовыми значениями, и временной минутной cron-строкой (только внутри контейнера). Проверка: бот доходит до запроса к Google API, `DefaultCredentialsError` и `FileNotFoundError` в `docker logs` нет.
- [x] 2.3 Дополнить `docs/configuration.md`: переменные `*_FILE` и то, что для cron сохраняются пути, а не значения. Проверка: `bash scripts/check-docs.sh` проходит.

## 3. Секреты не попадают в вывод ошибок

- [x] 3.1 В `calendar_bot.py` добавить функцию, маскирующую значения `API_KEY` и `TELEGRAM_BOT_TOKEN` (и их URL-кодированные формы) в тексте, и использовать её в обработчике необработанных исключений в `__main__` (печать в stderr, код возврата 1). Проверка: тесты из 3.2 проходят.
- [x] 3.2 Добавить тесты в `tests/test_calendar_bot.py`: маскирование в строке с `key=<значение>`, в URL с `bot<токен>`, пустое значение секрета ничего не маскирует, код возврата 1 при исключении. Проверка: `bash scripts/run-tests.sh` проходит.
- [x] 3.3 Прогнать `bash scripts/verify.sh`. Проверка: скрипт проходит без ошибок.

## 4. Ручная проверка

- [x] 4.1 Собрать образ и запустить тестовый контейнер с заведомо неверным тестовым `GOOGLE_API_KEY`. Проверка: `docker logs` показывает ошибку Google API с `key=***`, самого значения ключа в выводе нет.
- [ ] 4.2 После слияния в `main` проверить деплой в Actions. Проверка: шаг `Deploy stack` зелёный, `docker service ps antijob_calendar_scheduler` показывает одно обновление и задачу в состоянии running.
- [ ] 4.3 В продакшене проверить ночной (или ручной) запуск бота. Проверка: `docker service logs antijob_calendar_scheduler` показывает работу бота без `DefaultCredentialsError` и без значений секретов.
