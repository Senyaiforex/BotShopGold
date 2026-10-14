import os
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()
TOKEN_BOT: str = os.getenv("BOT_TOKEN")

bot = Bot(TOKEN_BOT)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


async def main():
    from handlers import router
    await bot.delete_webhook(drop_pending_updates=True)
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
