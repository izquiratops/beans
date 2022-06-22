import os
import openai

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, filters

from src.modules.whitelist import Whitelisted


async def run_callback(update: Update, _: CallbackContext) -> None:
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=update.message.text[5:],
        temperature=0,
        max_tokens=1024)

    reply = response.choices[0].text
    await update.message.reply_text(reply)


async def whoami_callback(update: Update, _: CallbackContext) -> None:
    reply = str(update.message.chat.id)
    await update.message.reply_text(reply)


class Beans:

    def __init__(self, application) -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        message_filter = Whitelisted()

        # Handlers
        whoami = CommandHandler("whoami", whoami_callback)
        run = CommandHandler("run", run_callback, message_filter)
        # TODO: message = MessageHandler(message_filters, message_callback)

        # Dispatcher
        application.add_handler(whoami)
        application.add_handler(run)
        # TODO: application.add_handler(message)
