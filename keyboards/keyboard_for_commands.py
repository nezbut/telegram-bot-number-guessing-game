from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon_ru import LEXICON_KEYBOARD

def get_keyboard_for_commands() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [KeyboardButton(text=text) for text in LEXICON_KEYBOARD.values()]

    builder.add(*buttons)
    builder.adjust(2, 2, 1)
    return builder.as_markup(resize_keyboard=True)

__all__ = (
    'get_keyboard_for_commands',
)
