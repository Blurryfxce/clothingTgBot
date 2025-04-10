import asyncio
import logging
from aiogram import Bot, Dispatcher

from routers import router as main_router
import config
from database.models import async_main

dp = Dispatcher()
dp.include_router(main_router)
bot = Bot(token=config.TG_TOKEN)


async def main():
    await async_main()
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Stop')
