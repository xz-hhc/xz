import os
import random
from pathlib import Path
from typing import List, Optional

from .embeddings import EmbeddingService
from .vector_store import VectorStore
from .conversation_store import ConversationStore


class RAGEngine:
    def __init__(self, storage_dir: Path):
        storage_dir = Path(storage_dir)
        self.storage_dir = storage_dir
        self.vector_store = VectorStore(storage_dir / "vector_store")
        self.conversation_store = ConversationStore(storage_dir / "conversations")
        self.embeddings = EmbeddingService(storage_dir / "embeddings" / "model.pkl")
        self.embeddings.load()

    def add_documents(self, doc_id: str, filename: str, chunks: List[dict]):
        for c in chunks:
            c["filename"] = filename
            c["upload_time"] = ""
        texts = [c.get("text", c.get("content", "")) for c in chunks]
        vectors = self.embeddings.encode(texts)
        self.vector_store.add_documents(chunks, vectors)
        self.embeddings.save()

    def query(self, question: str, conversation_id: str, top_k: int = 5) -> dict:
        stats = self.vector_store.get_stats()
        if stats["total_chunks"] == 0:
            return self._no_knowledge_response(question, conversation_id)

        try:
            query_vec = self.embeddings.encode_query(question)
        except ValueError:
            return self._no_knowledge_response(question, conversation_id)

        results = self.vector_store.search(query_vec, top_k=top_k)

        context_parts = []
        for i, r in enumerate(results):
            fname = r.get("filename", "unknown")
            text = r.get("text", "")
            context_parts.append("[来源 " + str(i+1) + ": " + fname + "]\n" + text)
        context = "\n\n".join(context_parts)

        sources = []
        for r in results:
            sources.append({
                "filename": r.get("filename", "unknown"),
                "content": r.get("text", "")[:300],
                "similarity": round(float(r.get("similarity", 0)), 4),
            })

        history = self.conversation_store.get_history(conversation_id)
        history_lines = []
        for m in history:
            role_label = "用户" if m.get("role") == "user" else "AI助手"
            history_lines.append(role_label + ": " + m.get("content", ""))
        history_text = "\n".join(history_lines[-6:])

        reply = self._generate_reply(question, context, history_text)

        self.conversation_store.add_message(conversation_id, "user", question)
        self.conversation_store.add_message(conversation_id, "assistant", reply)

        return {"reply": reply, "sources": sources}

    def _no_knowledge_response(self, question: str, conversation_id: str) -> dict:
        reply = self._generate_reply(question, "", "")
        self.conversation_store.add_message(conversation_id, "user", question)
        self.conversation_store.add_message(conversation_id, "assistant", reply)
        return {"reply": reply, "sources": []}

    def _generate_reply(self, question: str, context: str, history: str) -> str:
        has_knowledge = bool(context.strip())

        if not has_knowledge:
            return (
                "你好！我是你的AI知识助手。\n\n"
                "你还没有上传知识资料，所以我暂时无法基于你的文档回答具体问题。\n"
                "请先通过「上传文档」功能上传你的资料"
                "（支持 TXT、PDF、DOCX、CSV、MD、JSON 格式），"
                "然后我就可以基于这些资料为你提供智能回答了！\n\n"
                "你也可以直接和我自由对话，我会尽力帮助你。"
            )

        parts = []
        parts.append("基于你提供的知识资料，我对你的问题分析如下：\n")
        parts.append("【检索到的相关知识点】\n")

        seen = set()
        for line in context.split("\n"):
            stripped = line.strip()
            if stripped and stripped not in seen:
                parts.append(stripped + "\n")
                seen.add(stripped)

        parts.append("\n【回答】\n")
        parts.append(
            "根据你上传的资料中的相关信息，针对「" + question + "」：\n\n"
            "以上信息来源于你上传的知识库文档。如果需要更详细的解释，"
            "请上传更多相关资料，我可以帮你做更深入的分析。"
        )

        return "".join(parts)

    def delete_document(self, doc_id: str) -> bool:
        return self.vector_store.remove_document(doc_id) > 0

    def get_knowledge_list(self) -> List[dict]:
        return self.vector_store.get_document_list()

    def get_stats(self) -> dict:
        return self.vector_store.get_stats()
