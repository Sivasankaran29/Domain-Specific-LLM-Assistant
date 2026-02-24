from fastapi import APIRouter, Request, Depends
from bson import ObjectId
import json, re
from datetime import datetime

from backend.utils.retry import retry_async
from backend.cache import get_cache, set_cache
from backend.auth import get_current_user
from backend.db import db
from backend.llm import generate_llm_response
from backend.memory import get_summary
from backend.session_llm import generate_title, generate_summary

router = APIRouter()


# ---------- CLEAN JSON ----------
def clean_response(text: str):
    try:
        # remove markdown blocks
        text = re.sub(r"```json|```", "", text).strip()

        # extract first JSON object
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise ValueError("No JSON found")

        data = json.loads(match.group(0))

        if "type" not in data:
            raise ValueError("Missing type")

        if data["type"] not in ["legal", "refusal"]:
            raise ValueError("Invalid type")

        return data

    except Exception as e:
        print("JSON PARSE ERROR:", e)
        print("MODEL RAW:", text)

        # fallback → treat model text as answer
        return {
            "type": "legal",
            "data": {
                "answer": text[:2000],
                "relevant_laws": [],
                "general_process": "",
                "confidence": "low",
                "disclaimer": "General legal information only."
            }
        }


# ---------- SUMMARY TEXT ----------
def response_to_text(resp_json):
    if resp_json["type"] == "legal":
        return resp_json["data"].get("answer", "")
    return resp_json["data"].get("message", "")


@router.post("/chat")
async def chat(request: Request, user_id=Depends(get_current_user)):
    body = await request.json()
    session_id = body.get("session_id")
    query = (body.get("query") or "").strip()

    if not query:
        return {
            "session_id": session_id,
            "response": {
                "type": "refusal",
                "data": {"message": "Please enter a valid question."}
            }
        }

    # ---------- CREATE SESSION ----------
    if not session_id:
        title = await retry_async(generate_title, query)

        r = await db.sessions.insert_one({
            "user_id": user_id,
            "title": title,
            "summary": "",
            "created_at": datetime.utcnow()
        })

        session_id = str(r.inserted_id)

    # ---------- LOAD SUMMARY ----------
    summary = await get_summary(session_id)

    # ---------- CACHE ----------
    cache_key = f"{user_id}_{query}"
    cached = get_cache(cache_key)

    if cached:
        return {"session_id": session_id, "response": cached}

    # ---------- MAIN LLM ----------
    raw_response = await retry_async(generate_llm_response, summary, query)
    response_json = clean_response(raw_response)

    set_cache(cache_key, response_json)

    # ---------- SAVE MESSAGE ----------
    await db.messages.insert_one({
        "user_id": user_id,
        "session_id": ObjectId(session_id),
        "question": query,
        "response": response_json,
        "created_at": datetime.utcnow()
    })

    # ---------- UPDATE SUMMARY ----------
    answer_text = response_to_text(response_json)

    try:
        new_summary = await retry_async(generate_summary, summary, query, answer_text)

        await db.sessions.update_one(
            {"_id": ObjectId(session_id)},
            {"$set": {"summary": new_summary}}
        )
    except Exception as e:
        print("SUMMARY ERROR:", e)

    return {
        "session_id": session_id,
        "response": response_json
    }