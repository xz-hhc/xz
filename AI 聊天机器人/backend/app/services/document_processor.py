import os
import re
import uuid
from pathlib import Path
from typing import List

try:
    import jieba
    HAS_JIEBA = True
except ImportError:
    HAS_JIEBA = False


SUPPORTED_EXTS = {".txt", ".md", ".csv", ".pdf", ".docx", ".json"}


def extract_text(file_path: str) -> str:
    ext = Path(file_path).suffix.lower()
    if ext == ".txt":
        return _read_txt(file_path)
    elif ext == ".md":
        return _read_txt(file_path)
    elif ext == ".csv":
        return _read_csv(file_path)
    elif ext == ".pdf":
        return _read_pdf(file_path)
    elif ext == ".docx":
        return _read_docx(file_path)
    elif ext == ".json":
        return _read_json(file_path)
    else:
        raise ValueError(f"不支持的文件格式: {ext}")


def _read_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def _read_csv(file_path: str) -> str:
    import csv
    texts = []
    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.reader(f)
        for row in reader:
            texts.append(" | ".join(cell.strip() for cell in row if cell.strip()))
    return "\n".join(texts)


def _read_pdf(file_path: str) -> str:
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            return "\n".join(page.extract_text() or "" for page in pdf.pages)
    except ImportError:
        try:
            from pypdf import PdfReader
            reader = PdfReader(file_path)
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except ImportError:
            raise ImportError("需要安装 pdfplumber 或 pypdf 来读取PDF文件")


def _read_docx(file_path: str) -> str:
    try:
        from docx import Document
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    except ImportError:
        raise ImportError("需要安装 python-docx 来读取DOCX文件")


def _read_json(file_path: str) -> str:
    import json
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, str):
        return data
    if isinstance(data, dict):
        return json.dumps(data, ensure_ascii=False, indent=2)
    if isinstance(data, list):
        return "\n".join(
            json.dumps(item, ensure_ascii=False) if not isinstance(item, str) else item
            for item in data
        )
    return str(data)


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """将文本切分为重叠的块"""
    if not text.strip():
        return []

    chunks = []
    # 先按段落分割
    paragraphs = re.split(r"\n\s*\n", text.strip())
    current_chunk = ""

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        # 如果段落本身超过chunk_size，进一步切分
        if len(para) > chunk_size:
            if current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = ""
            # 按句号切分长段落
            sentences = re.split(r"(?<=[。！？.!?])", para)
            temp = ""
            for sent in sentences:
                if len(temp) + len(sent) > chunk_size and temp:
                    chunks.append(temp.strip())
                    temp = sent
                else:
                    temp += sent
            if temp:
                chunks.append(temp.strip())
            continue

        # 正常段落
        if len(current_chunk) + len(para) > chunk_size and current_chunk:
            chunks.append(current_chunk.strip())
            # 保留重叠部分
            current_chunk = current_chunk[-overlap:] + "\n" + para if overlap > 0 else para
        else:
            if current_chunk:
                current_chunk += "\n" + para
            else:
                current_chunk = para

    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return [c for c in chunks if len(c) > 10]


def segment_chinese(text: str) -> str:
    """中文分词，用于改进检索效果"""
    if HAS_JIEBA:
        return " ".join(jieba.cut(text))
    return text


def process_document(file_path: str, chunk_size: int = 500) -> tuple[str, list[dict]]:
    """处理文档：提取文本并切分，返回(原始文本, 块列表)"""
    doc_id = str(uuid.uuid4())
    raw_text = extract_text(file_path)

    if not raw_text.strip():
        raise ValueError("未能从文件中提取到文本内容")

    chunks = chunk_text(raw_text, chunk_size=chunk_size)

    chunk_data = []
    for i, chunk_text_content in enumerate(chunks):
        chunk_data.append({
            "doc_id": doc_id,
            "chunk_index": i,
            "text": chunk_text_content,
            "segmented": segment_chinese(chunk_text_content),
        })

    return doc_id, chunk_data
