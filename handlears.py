from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command

from database.main_class_db import BotDB
import config
import asyncio

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
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
            f"Снова приветствуем тебя👋, {message.from_user.full_name}!\nДля помощи нажмите /help"
        )

    else:

        await message.answer(
            f"Добро пожаловать {message.from_user.full_name}!👋\nДля помощи нажмите /help"
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


@dp.message(Command(commands=["help"]))
async def help_command(message: Message):
    """
    A decorator that registers the function as a message handler for the "/help" command.

    Args:
        message (Message): The message object representing the incoming message.

    Returns:
        None
    """

    await message.answer(
        f"Здравствуйте👋\nС этим ботом можно поиграть в \"Числовую угадайку\"\nВот список команд и их описание😁\n/help - Помощь по боту\n/stat - Ваша статистика по играм\n/go - Начать игру в Числовую угадайку\n/stop - Остановить игру в Числовую угадайку\n/reset - Обнулить вашу статистику по играм"
    )


@dp.message(Command(commands=["stat"]))
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
        f"Ваша статистика📊\nКоличество игр: {stat['count_games']}\nКоличество побед: {stat['wins']}"
    )


@dp.message(Command(commands=["reset"]))
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
        await message.answer('Ваша статистика успешно обнулена!✅')

    else:
        await message.answer('Произошла ошибка!❌ Статистика осталась прежней.')


@dp.message(Command(commands=["stop"]))
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
            await message.answer(f"Игра остановлена!✅")

        else:
            await message.answer(f"Произошла ошибка при остановке игры!❌")

    else:
        await message.answer(f"Игра еще не начата.🤔")


@dp.message(Command(commands=["go"]))
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
            await message.answer(f"Игра началась!😄\nПишите число от 1 до 100!\nВам дано 10 попыток")

        else:
            await message.answer(f"Произошла ошибка при начале игры.😱")

    else:
        await message.answer(f"Игра уже начата.🤔")


@dp.message(F.text & (F.text.isdigit()) & (F.text.in_(tuple(map(lambda a: str(a), range(1, 101))))))
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
                'К сожалению вы проиграли😔\nВаши попытки закончились\nВ следующий раз обязательно получится!😁'
            )
            return

        if user_num == win_rand_num:
            await BotDB.stop_game(message.from_user.username, win=True)
            await message.answer(f'Поздравляю вас🎉\nВы выиграли!\nВаши оставшиеся попытки: {attempt}')
            return

        elif win_rand_num > user_num:
            await message.answer(f'Увы, мое число больше {user_num}')

        elif win_rand_num < user_num:
            await message.answer(f'Увы, мое число меньше {user_num}')

        await BotDB.UPDATE.update_user_attempt(
            user=message.from_user.username,
            attempt=attempt - 1
        )


@dp.message()
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
        await message.answer(
            f"У вас в данный момент начата игра\nПишите число от 1 до 100\nУ вас {user['attempt']} попыток."
        )
