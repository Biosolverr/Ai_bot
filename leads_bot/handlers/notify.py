from aiogram import Router, Bot, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

router = Router()
OPERATOR_CHAT_ID = -1001234567890

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
    kb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Принять", callback_data=f"lead_accept:{lead_id}"),
        InlineKeyboardButton(text="❌ Отклонить", callback_data=f"lead_reject:{lead_id}"),
        InlineKeyboardButton(text="🔁 Перезвонить", callback_data=f"lead_callback:{lead_id}"),
    ]])
    await bot.send_message(OPERATOR_CHAT_ID, text, reply_markup=kb)

@router.callback_query(F.data.startswith("lead_accept:"))
async def cb_accept(call: CallbackQuery):
    lead_id = int(call.data.split(":")[1])
    from storage.database import update_stage
    await update_stage(lead_id, "done")
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.reply(f"✅ Заявка #{lead_id} принята оператором @{call.from_user.username}")
    await call.answer()

@router.callback_query(F.data.startswith("lead_reject:"))
async def cb_reject(call: CallbackQuery):
    lead_id = int(call.data.split(":")[1])
    from storage.database import update_stage
    await update_stage(lead_id, "rejected")
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.reply(f"❌ Заявка #{lead_id} отклонена — @{call.from_user.username}")
    await call.answer()

@router.callback_query(F.data.startswith("lead_callback:"))
async def cb_callback(call: CallbackQuery):
    lead_id = int(call.data.split(":")[1])
    from storage.database import update_stage
    await update_stage(lead_id, "callback")
    await call.message.edit_reply_markup(reply_markup=None)
    await call.message.reply(f"🔁 Заявка #{lead_id} — перезвон. Оператор: @{call.from_user.username}")
    await call.answer()
