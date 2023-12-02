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


def load_config() -> ConfigData:
    return ConfigData(
        telegram_bot=TelegramBot(
            bot_token=getenv('BOT_TOKEN')
        ),

        bot_db=BotDataBase(
            data_base_path=Path(__file__).resolve().parent.parent / 'database' / 'db.db'
        )
    )

Config = load_config()

__all__ = (
    'Config',
)
