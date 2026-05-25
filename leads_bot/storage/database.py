import aiosqlite
import asyncio

DB_PATH = "leads.db"

async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                niche TEXT,
                name TEXT,
                phone TEXT,
                comment TEXT,
                ai_score INTEGER,
                ai_verdict TEXT,
                stage TEXT DEFAULT 'new',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.commit()

async def insert_lead(data: dict) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute("""
            INSERT INTO leads (user_id, niche, name, phone, comment, ai_score, ai_verdict)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            data["user_id"], data["niche"], data["name"],
            data["phone"], data["comment"],
            data.get("ai_score", 0), data.get("ai_verdict", "")
        ))
        await db.commit()
        return cursor.lastrowid

async def get_stats() -> dict:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT niche,
                   COUNT(*) as total,
                   AVG(ai_score) as avg_score,
                   SUM(CASE WHEN stage='done' THEN 1 ELSE 0 END) as converted
            FROM leads GROUP BY niche
        """) as cur:
            rows = await cur.fetchall()
        return [dict(r) for r in rows]

async def update_stage(lead_id: int, stage: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("UPDATE leads SET stage=? WHERE id=?", (stage, lead_id))
        await db.commit()
