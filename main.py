from handlears import dp, bot
import asyncio
import logging


async def main():
    """
    Main entry point of the program.
    """
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
