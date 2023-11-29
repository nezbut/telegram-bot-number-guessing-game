from database.add_requests import AddDataBase
from database.give_requests import GiveDataBase
from database.remove_requests import RemoveDataBase
from database.update_requests import UpdateDataBase
from random import randint


class BotDB:
    GIVE = GiveDataBase()
    ADD = AddDataBase()
    REMOVE = RemoveDataBase()
    UPDATE = UpdateDataBase()

    @classmethod
    async def start_game(cls, user: str):
        """
        Start a new game for the given user.

        Args:
            user (str): The username of the user starting the game.

        Returns:
            The result of updating the user's game information.
        """

        random_number = randint(1, 100)
        res = await cls.UPDATE.update_user_in_game(
            user=user,
            status_in_game=True,
            attempt=10,
            num=random_number
        )
        return res

    @classmethod
    async def stop_game(cls, user: str, win=False):
        """
        Stop the game for a user.

        This method updates the user's status in the game, the user's statistics, and returns a boolean indicating whether all updates were successful.

        Parameters:
            user (str): The username of the user.
            win (bool, optional): A boolean indicating whether the user won the game. Defaults to False.

        Returns:
            bool: A boolean indicating whether all updates were successful.
        """

        res_update_in_game = await cls.UPDATE.update_user_in_game(
            user=user,
            status_in_game=False,
            attempt=0,
            num=0
        )

        user_stat = await cls.GIVE.give_stat_user(user)

        res_update_stat = await cls.UPDATE.update_stat_user(
            user=user,
            new_count_games=user_stat['count_games'] + 1,
            new_count_wins=user_stat['wins'] + 1 if win else user_stat['wins']
        )

        return all([res_update_in_game, user_stat, res_update_stat])
