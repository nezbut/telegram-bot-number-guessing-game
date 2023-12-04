from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from database.main_class_db import BotDB
from lexicon.lexicon_ru import LEXICON_RU, LEXICON_KEYBOARD
from keyboards.keyboard_for_commands import get_keyboard_for_commands
import asyncio

router = Router()

@router.message(CommandStart())
async def start_command(message: Message):
    """
    A function that handles the start command.

    Args:
        message (Message): The message object that triggered the command.

    Returns:
        None
    """
    user = await BotDB.GIVE.give_user(message.from_user.username)
    if user:
        await message.answer(
            LEXICON_RU['start_old_user'](message.from_user.full_name),
            reply_markup=get_keyboard_for_commands()
        )

    else:

        await message.answer(
            LEXICON_RU['start_new_user'](message.from_user.full_name),
            reply_markup=get_keyboard_for_commands()
        )

        await asyncio.gather(
            BotDB.ADD.add_user(
                user=message.from_user.username,
                chat_id=message.chat.id
            ),
            BotDB.ADD.add_stat_user(
                user=message.from_user.username
            )
        )


@router.message(F.text.in_(LEXICON_RU['help_cmd'](LEXICON_KEYBOARD['/help'])))
async def help_command(message: Message):
    """
    A decorator that registers the function as a message handler for the "/help" command.

    Args:
        message (Message): The message object representing the incoming message.

    Returns:
        None
    """

    await message.answer(
        LEXICON_RU['help'],
        reply_markup=get_keyboard_for_commands()
    )


@router.message(F.text.in_(LEXICON_RU['stat_cmd'](LEXICON_KEYBOARD['/stat'])))
async def stat_command(message: Message):
    """
    Handles the 'stat' command.

    Args:
        message (Message): The message object that triggered the command.

    Returns:
        None
    """

    stat = await BotDB.GIVE.give_stat_user(message.from_user.username)
    await message.answer(
        text=LEXICON_RU['stat'](stat['count_games'], stat['wins']),
        reply_markup=get_keyboard_for_commands()
    )


@router.message(F.text.in_(LEXICON_RU['reset_cmd'](LEXICON_KEYBOARD['/reset'])))
async def reset_stat_command(message: Message):
    """
    Resets the user's statistics by updating the count of wins and count of games to zero.

    Parameters:
        message (Message): The message object containing information about the user who sent the command.

    Returns:
        None
    """

    result = await BotDB.UPDATE.update_stat_user(
        user=message.from_user.username,
        new_count_wins=0,
        new_count_games=0
    )

    if result:
        await message.answer(
            LEXICON_RU['reset_stat_good'],
            reply_markup=get_keyboard_for_commands()
        )

    else:
        await message.answer(
            LEXICON_RU['reset_stat_bad'],
            reply_markup=get_keyboard_for_commands()
        )


@router.message(F.text.in_(LEXICON_RU['stop_cmd'](LEXICON_KEYBOARD['/stop'])))
async def stop_game_command(message: Message):
    """
    Handles the 'stop' command.

    Args:
        message (Message): The incoming message object.

    Returns:
        None

    Raises:
        None
    """

    user = await BotDB.GIVE.give_user(message.from_user.username)
    if user and user.get('in_game'):

        result = await BotDB.stop_game(message.from_user.username)

        if result:
            await message.answer(
                LEXICON_RU['stop_game_good'],
                reply_markup=get_keyboard_for_commands()
            )

        else:
            await message.answer(
                LEXICON_RU['stop_game_bad'],
                reply_markup=get_keyboard_for_commands()
            )

    else:
        await message.answer(
            LEXICON_RU['stop_game_user_not_in_game'],
            reply_markup=get_keyboard_for_commands()
        )


@router.message(F.text.in_(LEXICON_RU['go_cmd'](LEXICON_KEYBOARD['/go'])))
async def start_game_command(message: Message):
    """
    Handles the "go" command and starts the game for the user.

    Args:
        message (Message): The message object containing information about the user.

    Returns:
        None
    """

    user = await BotDB.GIVE.give_user(message.from_user.username)
    if user and not user.get('in_game'):

        result = await BotDB.start_game(message.from_user.username)

        if result:
            await message.answer(
                LEXICON_RU['go_game_good'],
                reply_markup=get_keyboard_for_commands()
            )

        else:
            await message.answer(
                LEXICON_RU['go_game_bad'],
                reply_markup=get_keyboard_for_commands()
            )

    else:
        await message.answer(
            LEXICON_RU['go_game_user_in_game'],
            reply_markup=get_keyboard_for_commands()
        )


@router.message(F.text & (F.text.isdigit()) & (F.text.in_(tuple(map(lambda a: str(a), range(1, 101))))))
async def answer_user_game(message: Message):
    """
    A function that handles the user's game response.

    Parameters:
    - message: A Message object representing the user's message.

    Returns:
    - None
    """

    user = await BotDB.GIVE.give_user(message.from_user.username)
    if user and user.get('in_game'):
        win_rand_num = user['rand_num']
        attempt = user['attempt']

        try:
            user_num = int(message.text)
        except ValueError:
            return

        if attempt <= 0:
            await BotDB.stop_game(message.from_user.username)
            await message.answer(
                LEXICON_RU['user_lose'],
                reply_markup=get_keyboard_for_commands()
            )
            return

        if user_num == win_rand_num:
            await BotDB.stop_game(message.from_user.username, win=True)
            await message.answer(
                LEXICON_RU['user_win'](attempt),
                reply_markup=get_keyboard_for_commands()
            )
            return

        elif win_rand_num > user_num:
            await message.answer(
                LEXICON_RU['number_is_greater'](user_num),
            )

        elif win_rand_num < user_num:
            await message.answer(
                LEXICON_RU['number_is_less'](user_num),
            )

        await BotDB.UPDATE.update_user_attempt(
            user=message.from_user.username,
            attempt=attempt - 1
        )
