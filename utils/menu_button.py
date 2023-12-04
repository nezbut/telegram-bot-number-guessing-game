from aiogram import Bot
from aiogram.types import BotCommand
from lexicon.lexicon_ru import LEXICON_COMMANDS_MENU

async def set_command_menu(bot: Bot):
    commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in LEXICON_COMMANDS_MENU.items()
    ]

    await bot.set_my_commands(commands=commands)

__all__ = (
    'set_command_menu',
)
