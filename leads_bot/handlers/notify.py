async def notify_operator(bot: Bot, data: dict, verdict: dict, lead_id: int):
    emoji = {"горячий": "🔥", "тёплый": "🟡", "холодный": "🔵"}.get(verdict["verdict"], "⚪")
    text = (
        f"{emoji} Новая заявка #{lead_id}\n"
        f"Ниша: {data['niche']}\n"
        f"Имя: {data['name']} | Тел: {data['phone']}\n"
        f"Задача: {data['comment']}\n\n"
        f"AI-оценка: {verdict['score']}/100 — {verdict['verdict']}\n"
        f"Причина: {verdict['reason']}"
    )
    await bot.send_message(OPERATOR_CHAT_ID, text)
