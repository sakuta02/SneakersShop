from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from packages.handlers import rt
from environs import Env
import asyncio


env = Env()
storage = MemoryStorage()
env.read_env()
token = env("Token")


async def run_bot():
    bot: Bot = Bot(token=token, parse_mode="HTML")
    dp = Dispatcher(storage=storage)
    dp.include_router(rt)
    await dp.start_polling(bot, polling_timeout=20)


if __name__ == "__main__":
    asyncio.run(run_bot())
