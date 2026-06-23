import os
from fastapi import APIRouter, HTTPException
from pathlib import Path

from ..services.rag_engine import RAGEngine
from ..models.schemas import KnowledgeListResponse, DeleteResponse, KnowledgeItem

router = APIRouter(prefix="/api/knowledge", tags=["knowledge"])


def get_engine():
    storage_dir = Path(os.environ.get("STORAGE_DIR", "backend/storage"))
    return RAGEngine(storage_dir)


@router.get("/list", response_model=KnowledgeListResponse)
async def list_knowledge():
    engine = get_engine()
    docs = engine.get_knowledge_list()
    items = []
    storage_dir = Path(os.environ.get("STORAGE_DIR", "backend/storage"))
    vs = RAGEngine(storage_dir).vector_store

    for d in docs:
        doc_chunks = [c for c in vs.chunks if c.get("doc_id") == d["id"]]
        items.append(KnowledgeItem(
            id=d["id"],
            filename=d.get("filename", "unknown"),
            size=sum(len(c.get("text", "")) for c in doc_chunks),
            chunk_count=len(doc_chunks),
            upload_time=doc_chunks[0].get("upload_time", "") if doc_chunks else "",
        ))

    return KnowledgeListResponse(documents=items, total=len(items))


@router.delete("/{doc_id}", response_model=DeleteResponse)
async def delete_document(doc_id: str):
    engine = get_engine()
    success = engine.delete_document(doc_id)
    if not success:
        raise HTTPException(status_code=404, detail="文档未找到")
    return DeleteResponse(message="文档已成功从知识库中删除")


@router.get("/stats")
async def get_stats():
    engine = get_engine()
    return engine.get_stats()
