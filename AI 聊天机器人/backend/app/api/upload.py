import os, uuid, json
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException

from ..services.document_processor import process_document, SUPPORTED_EXTS
from ..services.rag_engine import RAGEngine

router = APIRouter(prefix="/api/upload", tags=["upload"])


def get_engine():
    storage_dir = Path(os.environ.get("STORAGE_DIR", "backend/storage"))
    return RAGEngine(storage_dir)


@router.post("")
async def upload_file(file: UploadFile = File(...)):
    ext = Path(file.filename).suffix.lower()
    if ext not in SUPPORTED_EXTS:
        raise HTTPException(
            status_code=400,
            detail=f"不支持的文件格式: {ext}。支持的格式: {', '.join(SUPPORTED_EXTS)}"
        )

    storage_dir = Path(os.environ.get("STORAGE_DIR", "backend/storage"))
    upload_dir = storage_dir / "uploads"
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / f"{uuid.uuid4().hex}{ext}"
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)

    try:
        doc_id, chunks = process_document(str(file_path))
        engine = get_engine()
        engine.add_documents(doc_id, file.filename, chunks)
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"文档处理失败: {str(e)}")

    return {
        "id": doc_id,
        "filename": file.filename,
        "size": len(content),
        "chunk_count": len(chunks),
        "message": f"文档 '{file.filename}' 已成功上传并处理，拆分为 {len(chunks)} 个知识片段",
    }
