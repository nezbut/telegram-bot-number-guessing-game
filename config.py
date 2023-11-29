from os import getenv
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

BOT_TOKEN = getenv('BOT_TOKEN')
DATA_BASE_DIR = Path(__file__).resolve().parent / 'database' / 'db.db'

__all__ = (
    'BOT_TOKEN',
    'DATA_BASE_DIR'
)
