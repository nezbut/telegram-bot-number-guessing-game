from typing import Callable

LEXICON_RU: dict[str, str | Callable | tuple[str]] = {
    'start_old_user': lambda full_name: f"Снова приветствуем тебя👋, {full_name}!\nДля помощи нажмите /help",
    'start_new_user': lambda full_name: f"Добро пожаловать {full_name}!👋\nДля помощи нажмите /help",
    'help': f"Здравствуйте👋\nС этим ботом можно поиграть в \"Числовую угадайку\"\nВот список команд и их описание😁\n/help - Помощь по боту\n/stat - Ваша статистика по играм\n/go - Начать игру в Числовую угадайку\n/stop - Остановить игру в Числовую угадайку\n/reset - Обнулить вашу статистику по играм",
    'stat': lambda count_games, wins: f"Ваша статистика📊\nКоличество игр: {count_games}\nКоличество побед: {wins}",
    'reset_stat_good' : "Ваша статистика успешно обнулена!✅",
    'reset_stat_bad': "Произошла ошибка!❌ Статистика осталась прежней.",
    'stop_game_good': "Игра остановлена!✅",
    'stop_game_bad': "Произошла ошибка при остановке игры!❌",
    'stop_game_user_not_in_game': "Игра еще не начата.🤔",
    'go_game_good': "Игра началась!😄\nПишите число от 1 до 100!\nВам дано 10 попыток",
    'go_game_bad': "Произошла ошибка при начале игры.😱",
    'go_game_user_in_game': "Игра уже начата.🤔",
    'user_lose': "К сожалению вы проиграли😔\nВаши попытки закончились\nВ следующий раз обязательно получится!😁",
    'user_win': lambda attempt: f"Поздравляю вас🎉\nВы выиграли!\nВаши оставшиеся попытки: {attempt}",
    'number_is_greater': lambda num: f"Увы, мое число больше {num}",
    'number_is_less': lambda num: f"Увы, мое число меньше {num}",
    'other_messages_and_user_in_game': lambda attempt: f"У вас в данный момент начата игра\nПишите число от 1 до 100\nУ вас {attempt} попыток.",
    'help_cmd': ("/help", "Помощь"),
    'stat_cmd': ("/stat", "Моя статистика"),
    'go_cmd': ("/go", "Начать игру"),
    'stop_cmd': ("/stop", "Остановить игру"),
    'reset_cmd': ("/reset", "Обнулить мою статистику")
}

LEXICON_COMMANDS_MENU: dict[str, str] = {
    '/help': "Помощь по боту",
    '/stat': "Ваша статистика",
    '/go': "Начать игру",
    '/stop': "Остановить игру",
    '/reset': "Обнулить статистику"
}