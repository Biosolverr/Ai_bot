from aiogram import Router, F
from aiogram.types import Message
from storage.database import get_stats

router = Router()
ADMIN_IDS = {123456789}  # ваш Telegram ID

@router.message(F.text == "/stats")
async def cmd_stats(msg: Message):
    if msg.from_user.id not in ADMIN_IDS:
        return
    rows = await get_stats()
    if not rows:
        return await msg.answer("Пока нет данных.")

    lines = ["📊 Аналитика по нишам\n"]
    for r in rows:
        conv = r["converted"] or 0
        total = r["total"] or 1
        pct = round(conv / total * 100)
        score = round(r["avg_score"] or 0)
        lines.append(
            f"*{r['niche'].capitalize()}*\n"
            f"  Заявок: {r['total']} | Конверсия: {pct}% | AI-балл: {score}/100\n"
        )
    await msg.answer("\n".join(lines), parse_mode="Markdown")
