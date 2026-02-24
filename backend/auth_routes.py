from fastapi import APIRouter, HTTPException
from backend.db import db
from backend.auth import hash_password, verify_password, create_token

router = APIRouter(prefix="/auth")

@router.post("/register")
async def register(data: dict):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        raise HTTPException(400, "Missing fields")

    existing = await db.users.find_one({"email": email})
    if existing:
        raise HTTPException(400, "User exists")

    r = await db.users.insert_one({
        "email": email,
        "password": hash_password(password)
    })

    token = create_token(r.inserted_id)
    return {"token": token}


@router.post("/login")
async def login(data: dict):
    email = data.get("email")
    password = data.get("password")

    user = await db.users.find_one({"email": email})
    if not user:
        raise HTTPException(401, "Invalid")

    if not verify_password(password, user["password"]):
        raise HTTPException(401, "Invalid")

    token = create_token(user["_id"])
    return {"token": token}