import logging

from environs import Env
from telegram import Bot
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from dialogflow import detect_intent_texts


logger = logging.getLogger("tg-bot")


class TelegramLogsHandler(logging.Handler):
    def __init__(self, token, chat_id):
        super().__init__()
        self.bot = Bot(token=token)
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(self.chat_id, "Бот упал с ошибкой:")
        self.bot.send_message(self.chat_id, log_entry)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Здравствуйте!"
    )


def reply_to_user(update, context):
    answer = detect_intent_texts(
        project_id=env.str("DIALOGFLOW_PROJECT_ID"),
        session_id=update.effective_chat.id,
        text=update.message.text,
    )
    context.bot.send_message(
        chat_id=update.effective_chat.id, text=answer.fulfillment_text
    )


def run_bot(token):
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
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
        run_bot(env.str("TG_BOT_TOKEN"))
    except Exception as err:
        logger.exception(err)
