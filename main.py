from aiogram import Bot, Dispatcher
from handlears import commands_handlears, other_handlears
from config.config_data import Config
from utils.menu_button import set_command_menu
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

    if Config.command_menu:
        await set_command_menu(bot=bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    if Config.logs:
        logging.basicConfig(level=logging.INFO)
        
    asyncio.run(main())
