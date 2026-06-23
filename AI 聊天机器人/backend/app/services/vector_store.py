import json
import numpy as np
from pathlib import Path
from typing import List, Optional, Dict, Any


class VectorStore:
    def __init__(self, persist_dir: Path):
        self.persist_dir = Path(persist_dir)
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.chunks: List[Dict[str, Any]] = []
        self.vectors: Optional[np.ndarray] = None
        self._load()

    def add_documents(self, chunks: List[Dict], vectors: np.ndarray):
        start = len(self.chunks)
        for i, chunk in enumerate(chunks):
            self.chunks.append(chunk)
        if self.vectors is None:
            self.vectors = vectors
        else:
            self.vectors = np.vstack([self.vectors, vectors])
        self._save()

    def search(self, query_vec: np.ndarray, top_k: int = 5) -> List[Dict]:
        if self.vectors is None or len(self.chunks) == 0:
            return []

        from sklearn.metrics.pairwise import cosine_similarity
        scores = cosine_similarity(query_vec, self.vectors)[0]
        top_indices = np.argsort(scores)[::-1][:top_k]

        results = []
        for idx in top_indices:
            if scores[idx] > 0.01:
                entry = dict(self.chunks[idx])
                entry["similarity"] = float(scores[idx])
                results.append(entry)
        return results

    def remove_document(self, doc_id: str):
        remaining_chunks = [c for c in self.chunks if c.get("doc_id") != doc_id]
        removed = len(self.chunks) - len(remaining_chunks)
        if removed == 0:
            return 0
        self.chunks = remaining_chunks
        if len(self.chunks) == 0:
            self.vectors = None
        else:
            raise NotImplementedError("Full re-index required after removal")
        self._clear_persist()
        return removed

    def get_document_list(self) -> List[Dict]:
        seen = {}
        for c in self.chunks:
            did = c.get("doc_id")
            if did and did not in seen:
                seen[did] = {
                    "id": did,
                    "filename": c.get("filename", "unknown"),
                }
        return list(seen.values())

    def get_stats(self) -> dict:
        return {
            "total_chunks": len(self.chunks),
            "total_docs": len(self.get_document_list()),
            "vector_dim": self.vectors.shape[1] if self.vectors is not None else 0,
        }

    def _save(self):
        meta = {
            "chunks": [
                {k: v for k, v in c.items() if k != "segmented"}
                for c in self.chunks
            ],
        }
        with open(self.persist_dir / "meta.json", "w", encoding="utf-8") as f:
            json.dump(meta, f, ensure_ascii=False, indent=2)
        if self.vectors is not None:
            np.save(self.persist_dir / "vectors.npy", self.vectors)

    def _load(self):
        meta_path = self.persist_dir / "meta.json"
        vec_path = self.persist_dir / "vectors.npy"
        if meta_path.exists():
            with open(meta_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.chunks = data.get("chunks", [])
        if vec_path.exists():
            self.vectors = np.load(vec_path)

    def _clear_persist(self):
        meta_path = self.persist_dir / "meta.json"
        vec_path = self.persist_dir / "vectors.npy"
        if meta_path.exists():
            meta_path.unlink()
        if vec_path.exists():
            vec_path.unlink()
