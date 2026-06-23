import json
import uuid
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional


class ConversationStore:
    def __init__(self, persist_dir: Path):
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)

    def create_conversation(self) -> str:
        cid = str(uuid.uuid4())
        data = {"id": cid, "messages": [], "created_at": datetime.now().isoformat()}
        with open(self._path(cid), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
        return cid

    def add_message(self, conversation_id: str, role: str, content: str):
        path = self._path(conversation_id)
        if not path.exists():
            data = {"id": conversation_id, "messages": [], "created_at": datetime.now().isoformat()}
        else:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        data["messages"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
        })
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_history(self, conversation_id: str) -> List[dict]:
        path = self._path(conversation_id)
        if not path.exists():
            return []
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("messages", [])

    def get_all_conversations(self) -> List[dict]:
        conversations = []
        for f in self.persist_dir.glob("*.json"):
            with open(f, "r", encoding="utf-8") as fp:
                data = json.load(fp)
            conversations.append({
                "id": data["id"],
                "created_at": data.get("created_at", ""),
                "message_count": len(data.get("messages", [])),
            })
        return sorted(conversations, key=lambda x: x["created_at"], reverse=True)

    def _path(self, cid: str) -> Path:
        return self.persist_dir / f"{cid}.json"
