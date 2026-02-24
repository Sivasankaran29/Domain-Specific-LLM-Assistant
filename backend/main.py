from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.chat import router as chat_router
from backend.auth_routes import router as auth_router
from backend.history import router as history_router
from backend.sessions import router as sessions_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(history_router)
app.include_router(sessions_router)