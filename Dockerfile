# syntax=docker/dockerfile:1
FROM python:3.8
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip && pip3 install wheel && pip3 install -r requirements.txt
COPY . .
ENV TG_BOT_TOKEN=$TG_BOT_TOKEN \
    TG_CHAT_ID=$TG_CHAT_ID \
    DIALOGFLOW_PROJECT_ID=$DIALOGFLOW_PROJECT_ID \
    GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS \
    VK_ACCESS_KEY=$VK_ACCESS_KEY \
    LOGGING_LEVEL=$LOGGING_LEVEL
ENTRYPOINT ["sh", "./create_google_credentials_json_from_env.sh"]
CMD python vk.py & python tg.py