from aiogram import Bot, Dispatcher
from handlears import commands_handlears, other_handlears
from config.config_data import Config
import asyncio
import logging


async def main():
    """
    Main entry point of the program.
    """
    bot = Bot(token=Config.telegram_bot.bot_token)
    dp = Dispatcher()

    dp.include_routers(
        commands_handlears.router,
        other_handlears.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
