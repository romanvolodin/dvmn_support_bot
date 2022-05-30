import logging

from environs import Env
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from dialogflow import detect_intent_texts
from log_handlers import TelegramLogsHandler


logger = logging.getLogger("tg-bot")


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Здравствуйте!"
    )


def reply_to_user(update, context):
    answer = detect_intent_texts(
        project_id=context.bot_data["dialogflow_project_id"],
        session_id=update.effective_chat.id,
        text=update.message.text,
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=answer.fulfillment_text
    )


def run_bot(token, dialogflow_project_id):
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    dispatcher.bot_data["dialogflow_project_id"] = dialogflow_project_id
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, reply_to_user)
    )
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    env = Env()
    env.read_env()

    logging.basicConfig(level=env.str("LOGGING_LEVEL", "WARNING"))
    logger.addHandler(
        TelegramLogsHandler(env.str("TG_BOT_TOKEN"), env.str("TG_CHAT_ID"))
    )
    try:
        run_bot(env.str("TG_BOT_TOKEN"), env.str("DIALOGFLOW_PROJECT_ID"))
    except Exception as err:
        logger.exception(err)
