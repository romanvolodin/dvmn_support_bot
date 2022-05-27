# dvmn_support_bot

## Требования

Для работы с Dialogflow понадобится:

- Создайть проект в Google Cloud и сохранить его id. Подробнее [здесь](https://cloud.google.com/dialogflow/es/docs/quick/setup#project).
- Создайте "агента", который будет отвечать на вопросы. При создания агента понадобится ввести id проекта из предыдущего пункта. Укажите язык агента "русский", иначе он вас не поймет. Подробнее [здесь](https://cloud.google.com/dialogflow/es/docs/quick/build-agent).
- Зарегистрируйте сервисный аккаунт для проекта и скачайте JSON-ключ. Подробнее [здесь](https://cloud.google.com/docs/authentication/getting-started).

## Переменные окружения

Настройки берутся из переменных окружения. Чтобы их определить, создайте файл `.env` в корне проекта и запишите туда данные в таком формате: `ПЕРЕМЕННАЯ=значение`.

Доступные переменные:

- `DIALOGFLOW_PROJECT_ID` — id проекта в Google Cloud, указанный при создании агента.
- `GOOGLE_APPLICATION_CREDENTIALS` — путь до файла с ключами для подключения к Google API.

Пример:

```env
DIALOGFLOW_PROJECT_ID=example-project-157495
GOOGLE_APPLICATION_CREDENTIALS=/path/to/example-project-157495-32834a814fa6.json
```
