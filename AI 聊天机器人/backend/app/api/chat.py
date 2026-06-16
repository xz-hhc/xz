import os
import uuid
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ..services.rag_engine import RAGEngine
from ..models.schemas import ChatRequest, ChatResponse
from pathlib import Path

router = APIRouter(prefix="/api/chat", tags=["chat"])


def get_engine():
    storage_dir = Path(os.environ.get("STORAGE_DIR", "backend/storage"))
    return RAGEngine(storage_dir)


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="消息不能为空")

    engine = get_engine()
    conv_id = req.conversation_id

    if not conv_id:
        conv_id = engine.conversation_store.create_conversation()

    try:
        result = engine.query(req.message, conv_id, top_k=req.top_k)
        return ChatResponse(
            reply=result["reply"],
            conversation_id=conv_id,
            sources=result["sources"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成回复失败: {str(e)}")


@router.get("/history/{conversation_id}")
async def get_history(conversation_id: str):
    engine = get_engine()
    messages = engine.conversation_store.get_history(conversation_id)
    return {"conversation_id": conversation_id, "messages": messages}
