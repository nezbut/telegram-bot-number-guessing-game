import aiosqlite
from config.config_data import Config

class GiveDataBase:

    @staticmethod
    async def give_stat_user(user: str):
        """
        Retrieve the game statistics for a user from the database.

        Args:
            user (str): The username of the user.

        Returns:
            dict: A dictionary containing the game statistics for the user, including the count of games played and the number of wins.
        """
        async with aiosqlite.connect(Config.bot_db.data_base_path) as db:
            db.row_factory = aiosqlite.Row

            async with db.execute('SELECT * FROM users_stat') as cursor:
                async for row in cursor:
                    if row['user'] == user.lower().strip():
                        return {
                            'count_games': row['count_games'],
                            'wins': row['wins']
                        }

    @staticmethod
    async def give_user(user: str):

        """
        Retrieves the user's information from the database.

        Args:
            user (str): The username of the user.

        Returns:
            dict: A dictionary containing the user's information, including the username, chat ID, and in-game status.
                  Returns None if the user is not found in the database.
        """

        async with aiosqlite.connect(Config.bot_db.data_base_path) as db:
            db.row_factory = aiosqlite.Row

            async with db.execute('SELECT * FROM users') as cursor:
                async for row in cursor:
                    if row['username'] == user.lower().strip():
                        return {
                            'username': row['username'],
                            'chat_id': row['chat_id'],
                            'in_game': row['in_game'],
                            'attempt': row['attempt'],
                            'rand_num': row['num']
                        }
