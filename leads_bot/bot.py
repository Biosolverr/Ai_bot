import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.session.aiohttp import AiohttpSession

from handlers import lead, notify
from storage.database import init_db
from analytics.stats import router as stats_router

TOKEN = "YOUR_BOT_TOKEN"
PROXY = "http://127.0.0.1:10809"


async def main():
    await init_db()

    session = AiohttpSession(proxy=PROXY)
    bot = Bot(token=TOKEN, session=session)
    dp = Dispatcher()

    dp.include_router(lead.router)
    dp.include_router(notify.router)
    dp.include_router(stats_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
