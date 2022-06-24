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


class Beans:

    GPT_MODEL = "text-davinci-002"
    GPT_TEMPERATURE = 1.0
    GPT_MAX_TOKENS = 1024

    async def message_callback(self, update: Update, _: CallbackContext) -> None:
        try:
            response = openai.Completion.create(
                model=self.GPT_MODEL,
                prompt=update.message.text,
                temperature=self.GPT_TEMPERATURE,
                max_tokens=self.GPT_MAX_TOKENS
            )

            await update.message.reply_text(response.choices[0].text)

        except:
            await update.message.reply_text("Bad API response")

    async def whoami_callback(self, update: Update, _: CallbackContext) -> None:
        await update.message.reply_text(f"Chat ID: {update.message.chat.id}")

    def __init__(self, application) -> None:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        message_filter = WhitelistFilter() & ~filters.REPLY & ~filters.FORWARDED

        # Handlers
        whoami = CommandHandler("whoami", self.whoami_callback)
        message = MessageHandler(message_filter, self.message_callback)

        # Dispatcher
        application.add_handler(whoami)
        application.add_handler(message)
