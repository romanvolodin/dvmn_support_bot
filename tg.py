import logging

from environs import Env
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Здравствуйте!"
    )


def echo(update, context):
    context.bot.send_message(update.message.text)


def bot(token):
    updater = Updater(token=token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command, echo)
    )
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    env = Env()
    env.read_env()
    bot(env.str("TG_BOT_TOKEN"))
