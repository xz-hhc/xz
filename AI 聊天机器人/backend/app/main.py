import os
import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.api import upload, chat, knowledge

app = FastAPI(
    title="AI 聊天机器人 API",
    description="一个支持用户上传资料进行训练的AI聊天机器人后端服务",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(knowledge.router)


@app.get("/api/health")
async def health():
    return {"status": "ok", "message": "AI 聊天机器人服务运行中"}


# Mount web UI static files
web_ui_path = Path(__file__).parent.parent.parent / "web-ui"
if web_ui_path.exists():
    app.mount("/", StaticFiles(directory=str(web_ui_path), html=True), name="web-ui")
