import os
import logging

from telegram.ext import Application

from src.modules.beans import Beans


def main() -> None:
    logging.getLogger('root')
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )

    # Telegram Bot init
    telegram_key = os.getenv("TELEGRAM_BOT_KEY")
    application = Application\
        .builder()\
        .token(telegram_key)\
        .build()

    # OpenAI Telegram Handlers
    Beans(application)

    # 🥳
    application.run_polling()


if __name__ == '__main__':
    main()
