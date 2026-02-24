from fastapi import APIRouter, Depends
from bson import ObjectId
from backend.auth import get_current_user
from backend.db import db

router = APIRouter()

@router.get("/sessions")
async def get_sessions(user_id=Depends(get_current_user)):
    sessions = db.sessions.find({"user_id": user_id}).sort("created_at", -1)

    result = []

    async for s in sessions:
        result.append({
            "id": str(s["_id"]),
            "title": s.get("title", "New Chat")
        })

    return {"sessions": result}