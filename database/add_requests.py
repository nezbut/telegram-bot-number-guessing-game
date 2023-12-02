from config.config_data import Config
import aiosqlite
import logging


class AddDataBase:

    @staticmethod
    async def add_stat_user(user: str, count_games: int = 0, wins: int = 0):
        """
        Add the game statistics for a user to the database.

        Args:
            user (str): The username of the user.
            count_games (int, optional): The number of games played. Defaults to 0.
            wins (int, optional): The number of wins. Defaults to 0.
        """
        try:
            async with aiosqlite.connect(Config.bot_db.data_base_path) as db:
                db.row_factory = aiosqlite.Row
                await db.execute('INSERT INTO users_stat (user, count_games, wins) VALUES (?, ?, ?)',
                                 (user.lower().strip(), str(count_games), str(wins)))
                await db.commit()

        except Exception as e:
            logging.error(e)
            return False

        else:
            return True

    @staticmethod
    async def add_user(user: str, chat_id: str):
        """
        Add the user to the database.

        Args:
            user (str): The username of the user.
            chat_id (str): The chat id of the user.
        """

        try:
            async with aiosqlite.connect(Config.bot_db.data_base_path) as db:
                db.row_factory = aiosqlite.Row

                await db.execute('INSERT INTO users (username, chat_id) VALUES (?, ?)',
                                 (user.lower().strip(), chat_id))

                await db.commit()

        except Exception:
            logging.error(e)
            return False

        else:
            return True
