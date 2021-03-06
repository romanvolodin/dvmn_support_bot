import logging
import random

import vk_api
from environs import Env
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow import detect_intent_texts
from log_handlers import TelegramLogsHandler


logger = logging.getLogger("vk-bot")


def reply_to_user(event, vk_api, dialogflow_project_id):
    answer = detect_intent_texts(
        project_id=dialogflow_project_id,
        session_id=event.user_id,
        text=event.text,
    )
    if answer.intent.is_fallback:
        return

    vk_api.messages.send(
        user_id=event.user_id,
        message=answer.fulfillment_text,
        random_id=random.randint(1, 1000),
    )


def run_bot(token, dialogflow_project_id):
    vk_session = vk_api.VkApi(token=token)
    api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            reply_to_user(event, api, dialogflow_project_id)


if __name__ == "__main__":
    env = Env()
    env.read_env()

    logging.basicConfig(level=env.str("LOGGING_LEVEL", "WARNING"))
    logger.addHandler(
        TelegramLogsHandler(env.str("TG_BOT_TOKEN"), env.str("TG_CHAT_ID"))
    )

    try:
        run_bot(env.str("VK_ACCESS_KEY"), env.str("DIALOGFLOW_PROJECT_ID"))
    except Exception as err:
        logger.exception(err)
