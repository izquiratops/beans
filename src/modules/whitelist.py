import os

from telegram.ext.filters import MessageFilter


def parse_whitelist():
    string_list = os.getenv("WHITELIST_IDS").split(",")
    return [int(x) for x in string_list]


class Whitelisted(MessageFilter):
    whitelist_telegram_ids = parse_whitelist()

    def filter(self, message):
        return message.chat.id in self.whitelist_telegram_ids
