from backend.db import db
from bson import ObjectId

async def get_summary(session_id):
    s = await db.sessions.find_one({"_id": ObjectId(session_id)})
    return s.get("summary", "") if s else ""

async def update_summary(session_id, summary):
    await db.sessions.update_one(
        {"_id": ObjectId(session_id)},
        {"$set": {"summary": summary}}
    )