import os
import openai

from telegram import Update
from telegram.ext import CommandHandler, CallbackContext, MessageHandler, filters
from telegram.ext.filters import MessageFilter


class WhitelistFilter(MessageFilter):

    def parse_whitelist(self):
        string_list = os.getenv("WHITELIST_IDS").split(",")
        return [int(x) for x in string_list]

    def filter(self, message):
        return message.chat.id in self.parse_whitelist()


async def whoami_callback(update: Update, _: CallbackContext) -> None:
    reply = str(update.message.chat.id)
    await update.message.reply_text(reply)


class Beans:

    async def message_callback(self, update: Update, _: CallbackContext) -> None:
        response = openai.Completion.create(
            model="text-davinci-002",
            prompt=update.message.text,
            temperature=0.1,
            max_tokens=1024)

        reply = response.choices[0].text
        await update.message.reply_text(reply)

    def __init__(self, application) -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        message_filter = WhitelistFilter() & ~filters.REPLY & ~filters.FORWARDED

        # Handlers
        whoami = CommandHandler("whoami", whoami_callback)
        message = MessageHandler(message_filter, self.message_callback)

        # Dispatcher
        application.add_handler(whoami)
        application.add_handler(message)
