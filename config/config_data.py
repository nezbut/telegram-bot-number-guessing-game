from os import getenv
from dotenv import load_dotenv
from pathlib import Path
from dataclasses import dataclass

load_dotenv()

@dataclass
class TelegramBot:
    bot_token: str

@dataclass
class BotDataBase:
    data_base_path: Path

@dataclass
class ConfigData:
    telegram_bot: TelegramBot
    bot_db: BotDataBase
    command_menu: bool

def _get_choose_command_menu() -> bool:
    menu = getenv('COMMAND_MENU').upper()
    menu_choose = menu if menu in ('YES', 'NO') else 'NO'

    match menu_choose:

        case "YES":
            return True

        case "NO":
            return False

def _load_config() -> ConfigData:
    return ConfigData(
        telegram_bot=TelegramBot(
            bot_token=getenv('BOT_TOKEN')
        ),
        bot_db=BotDataBase(
            data_base_path=Path(__file__).resolve().parent.parent / 'database' / 'db.db'
        ),
        command_menu=_get_choose_command_menu()
    )

Config = _load_config()

__all__ = (
    'Config',
)
