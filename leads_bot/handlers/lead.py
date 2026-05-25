# в step_done заменить save_lead на:

async def step_done(msg: Message, state: FSMContext, bot: Bot):
    import time, asyncio
    uid = msg.from_user.id
    now = time.time()
    if uid in _last_submit and now - _last_submit[uid] < 60:
        await state.clear()
        return await msg.answer("⏳ Подождите минуту перед следующей заявкой.")
    _last_submit[uid] = now

    data = await state.get_data()
    data["comment"] = msg.text
    data["user_id"] = uid

    await msg.answer("⏳ Анализируем заявку...")

    # AI-квалификация
    from ai.qualify import qualify_lead
    verdict = await qualify_lead(data)
    data["ai_score"] = verdict["score"]
    data["ai_verdict"] = verdict["verdict"]

    # Сохраняем в БД
    from storage.database import insert_lead
    lead_id = await insert_lead(data)

    # Уведомляем оператора
    from handlers.notify import notify_operator
    await notify_operator(bot, data, verdict, lead_id)

    # Запускаем автоворонку
    from handlers.funnel import schedule_followup
    asyncio.create_task(schedule_followup(bot, uid, lead_id, data["niche"]))

    await state.clear()
    await msg.answer(
        f"✅ Заявка принята!\n"
        f"Статус: *{verdict['verdict']}*\n"
        f"Менеджер свяжется в ближайшее время.",
        parse_mode="Markdown"
    )
