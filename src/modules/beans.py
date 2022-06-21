import os
import openai

from telegram import Update
from telegram.ext import MessageHandler, CallbackContext, filters

from src.modules.whitelist import Whitelisted


async def process_message(update: Update, _: CallbackContext) -> None:
    response = openai.Completion.create(
        model="text-davinci-002",
        prompt=update.message.text,
        temperature=0,
        max_tokens=512)

    print(update.message.chat.id)

    reply = response.choices[0].text
    await update.message.reply_text(reply)


class Beans:

    def __init__(self, application) -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # Handlers
        filter_whitelist = Whitelisted()
        message = MessageHandler(
            filters=filter_whitelist & filters.TEXT,
            callback=process_message
        )

        # Dispatcher
        application.add_handler(message)
