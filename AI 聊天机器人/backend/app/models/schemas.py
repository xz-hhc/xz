from __future__ import annotations
from pydantic import BaseModel, Field
from typing import List, Optional


class UploadResponse(BaseModel):
    id: str
    filename: str
    size: int
    chunk_count: int
    message: str


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    top_k: int = Field(5, ge=1, le=20)


class ChatResponse(BaseModel):
    reply: str
    conversation_id: str
    sources: list[dict] = []


class KnowledgeItem(BaseModel):
    id: str
    filename: str
    size: int
    chunk_count: int
    upload_time: str


class KnowledgeListResponse(BaseModel):
    documents: list[KnowledgeItem]
    total: int


class DeleteResponse(BaseModel):
    message: str


class ChatHistoryItem(BaseModel):
    role: str
    content: str
    timestamp: str


class ChatHistoryResponse(BaseModel):
    conversation_id: str
    messages: list[ChatHistoryItem]
