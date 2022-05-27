import random

import vk_api
from environs import Env
from vk_api.longpoll import VkEventType, VkLongPoll

from dialogflow import detect_intent_texts


def dialog(event, vk_api):
    answer = detect_intent_texts(
        project_id=env.str("DIALOGFLOW_PROJECT_ID"),
        session_id=event.user_id,
        text=event.text,
    )
    vk_api.messages.send(
        user_id=event.user_id,
        message=answer,
        random_id=random.randint(1, 1000),
    )


if __name__ == "__main__":
    env = Env()
    env.read_env()

    vk_session = vk_api.VkApi(token=env.str("VK_ACCESS_KEY"))
    api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            dialog(event, api)
