import asyncio
from aiogram import Bot
import aiosqlite
from storage.database import DB_PATH

FOLLOWUP_DELAY = 86400  # 24 часа

async def schedule_followup(bot: Bot, user_id: int, lead_id: int, niche: str):
    await asyncio.sleep(FOLLOWUP_DELAY)
    # Проверяем — вдруг уже закрыт
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute(
            "SELECT stage FROM leads WHERE id=?", (lead_id,)
        ) as cur:
            row = await cur.fetchone()
    if row and row[0] == "new":
        texts = {
            "недвижимость": "🏠 Ещё не выбрали объект? Наши эксперты готовы помочь прямо сейчас.",
            "юристы": "⚖️ Вопрос ещё актуален? Юрист онлайн, ответим за 15 минут.",
            "услуги": "🔧 Задача ещё открыта? Подберём исполнителя сегодня.",
            "ремонт": "🏗️ Планируете ремонт? Пришлём смету бесплатно.",
        }
        text = texts.get(niche, "👋 Ваша заявка ещё актуальна? Мы готовы помочь.")
        try:
            await bot.send_message(user_id, text)
        except Exception:
            pass  # пользователь заблокировал бота
