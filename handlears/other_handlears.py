from aiogram import Router
from aiogram.types import Message

from database.main_class_db import BotDB
from lexicon.lexicon_ru import LEXICON_RU

router = Router()

@router.message()
async def other_messages(message: Message):
    """
    An async function that handles other messages received by the bot.

    Args:
        message (Message): The message received by the bot.

    Returns:
        None
    """

    user = await BotDB.GIVE.give_user(user=message.from_user.username)
    if user and user.get('in_game'):
        await message.answer(LEXICON_RU['other_messages_and_user_in_game'](user['attempt']))
