import os
import asyncio
from dotenv import load_dotenv # type: ignore
from aiogram import Bot, Dispatcher
from handlers import start
from handlers import auto
from handlers import home
from handlers import life
import logging
from aiogram.fsm.storage.memory import MemoryStorage

logging.basicConfig(level=logging.INFO)

# 1️⃣ .env faylni yuklash
load_dotenv()

# 2️⃣ Tokenni olish
BOT_TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
storage = MemoryStorage() 

# Routerlarni ulash
dp.include_router(start.router)
dp.include_router(auto.router)  
dp.include_router(home.router)
dp.include_router(life.router)


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
