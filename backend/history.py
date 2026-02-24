from fastapi import APIRouter, Depends
from bson import ObjectId
from backend.auth import get_current_user
from backend.db import db

router = APIRouter()

@router.get("/history/{session_id}")
async def get_history(session_id: str, user_id=Depends(get_current_user)):
    messages = db.messages.find({
        "user_id": user_id,
        "session_id": ObjectId(session_id)
    }).sort("created_at", 1)

    result = []
    async for m in messages:
        result.append({
            "question": m["question"],
            "response": m["response"]
        })

    return {"history": result}