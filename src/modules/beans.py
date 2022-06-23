import os
import openai

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, filters

from whitelist import Whitelisted


async def whoami_callback(update: Update, _: CallbackContext) -> None:
    reply = str(update.message.chat.id)
    await update.message.reply_text(reply)


class Beans:

    max_tokens = 1024
    temperature = 5

    async def message_callback(self, update: Update, _: CallbackContext) -> None:
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=update.message.text,
            temperature=self.temperature,
            max_tokens=self.max_tokens)

        reply = response.choices[0].text
        await update.message.reply_text(reply)

    async def change_temp_callback(self, update: Update, _: CallbackContext) -> None:
        value = update.message.text.replace('/temperature', '')
        self.temperature = int(value)

        await update.message.reply_text('Done')

    def __init__(self, application) -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        message_filter = Whitelisted() & ~filters.REPLY & ~filters.FORWARDED

        # Handlers
        whoami = CommandHandler("whoami", whoami_callback)
        change_temp = CommandHandler("temperature", self.change_temp_callback)
        message = MessageHandler(message_filter, self.message_callback)

        # Dispatcher
        application.add_handler(whoami)
        application.add_handler(change_temp)
        application.add_handler(message)
