import aiosqlite
import config
import logging


class UpdateDataBase:

    @staticmethod
    async def update_stat_user(user: str, new_count_games: int, new_count_wins: int):
        """
        Update the statistics for a user in the database.

        Args:
            user (str): The name of the user.
            new_count_games (int): The new count of games for the user.
            new_count_wins (int): The new count of wins for the user.

        Returns:
            bool: True if the update was successful, False otherwise.
        """

        try:

            async with aiosqlite.connect(config.DATA_BASE_DIR) as db:

                db.row_factory = aiosqlite.Row
                await db.execute("UPDATE users_stat SET count_games = ?, wins = ? WHERE user = ?",
                                 (new_count_games, new_count_wins, user.lower().strip()))
                await db.commit()

        except Exception as e:
            logging.error(e)
            return False

        else:
            return True

    @staticmethod
    async def update_user_in_game(user: str, status_in_game: bool, attempt: int = 0, num: int = 0):
        """
        Update the user's status in the game.

        Args:
            user (str): The username of the user.
            status_in_game (bool): The new status of the user in the game.
            attempt (int, optional): The number of attempts made by the user (default is 0).
            num (int, optional): The number associated with the user (default is 0).

        Returns:
            bool: True if the user was successfully updated in the game, False otherwise.
        """

        try:

            async with aiosqlite.connect(config.DATA_BASE_DIR) as db:

                db.row_factory = aiosqlite.Row
                await db.execute("UPDATE users SET in_game = ?, attempt = ?, num = ? WHERE username = ?",
                                 (status_in_game, attempt, num, user.lower().strip()))
                await db.commit()

        except Exception as e:
            logging.error(e)
            return False

        else:
            return True

    @staticmethod
    async def update_user_attempt(user: str, attempt: int):
        """
        Update the number of attempts made by a user in the database.

        Args:
            user (str): The username of the user.
            attempt (int): The number of attempts made by the user.

        Returns:
            bool: True if the user's attempts were updated successfully, False otherwise.
        """

        try:

            async with aiosqlite.connect(config.DATA_BASE_DIR) as db:

                db.row_factory = aiosqlite.Row
                await db.execute("UPDATE users SET attempt = ? WHERE username = ?",
                                 (attempt, user.lower().strip()))
                await db.commit()

        except Exception as e:
            logging.error(e)
            return False

        else:
            return True
