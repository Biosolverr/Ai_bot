import aiohttp
from aiohttp_socks import ProxyConnector
import json

PROXY = "http://127.0.0.1:10809"
ANTHROPIC_KEY = "YOUR_ANTHROPIC_KEY"

NICHE_PROMPTS = {
    "недвижимость": "Оцени лид на покупку/аренду недвижимости",
    "юристы": "Оцени лид на юридическую консультацию",
    "услуги": "Оцени лид на бытовые услуги",
    "ремонт": "Оцени лид на ремонт квартиры/дома",
}

async def qualify_lead(data: dict) -> dict:
    niche_hint = NICHE_PROMPTS.get(data["niche"], "Оцени лид")
    prompt = f"""{niche_hint}.

Имя: {data['name']}
Телефон: {data['phone']}
Комментарий: {data['comment']}

Ответь ТОЛЬКО JSON без markdown:
{{"score": 0-100, "verdict": "горячий|тёплый|холодный", "reason": "1 предложение"}}"""

    connector = ProxyConnector.from_url(PROXY)
    async with aiohttp.ClientSession(connector=connector) as session:
        resp = await session.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": ANTHROPIC_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 200,
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        result = await resp.json()

    raw = result["content"][0]["text"]
    try:
        parsed = json.loads(raw)
    except Exception:
        parsed = {"score": 50, "verdict": "тёплый", "reason": "Не удалось разобрать ответ"}
    return parsed
