import os
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from backend.db import db
from bson import ObjectId

SECRET = os.getenv("JWT_SECRET")
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def hash_password(p):
    return pwd.hash(p)

def verify_password(p, h):
    return pwd.verify(p, h)

def create_token(user_id):
    payload = {
        "user_id": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")

async def get_current_user(token=Depends(security)):
    try:
        data = jwt.decode(token.credentials, SECRET, algorithms=["HS256"])
        return ObjectId(data["user_id"])
    except:
        raise HTTPException(401, "Invalid token")