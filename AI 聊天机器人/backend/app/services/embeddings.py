import pickle
import numpy as np
from pathlib import Path
from typing import List, Optional
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TFIDFEmbeddings:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=10000,
            analyzer="char_wb",
            ngram_range=(1, 3),
            sublinear_tf=True,
        )
        self._fitted = False

    def fit(self, texts: List[str]):
        self.vectorizer.fit(texts)
        self._fitted = True

    def transform(self, texts: List[str]) -> np.ndarray:
        if not self._fitted:
            self.fit(texts)
        return self.vectorizer.transform(texts).toarray().astype(np.float32)

    def transform_query(self, query: str) -> np.ndarray:
        if not self._fitted:
            raise ValueError("Vectorizer not fitted yet")
        return self.vectorizer.transform([query]).toarray().astype(np.float32)

    def similarity(self, qv: np.ndarray, dv: np.ndarray) -> np.ndarray:
        return cosine_similarity(qv, dv)[0]

    def save(self, path: Path):
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(self.vectorizer, f)

    @classmethod
    def load(cls, path: Path):
        with open(path, "rb") as f:
            v = pickle.load(f)
        inst = cls()
        inst.vectorizer = v
        inst._fitted = True
        return inst


class EmbeddingService:
    def __init__(self, model_path: Optional[Path] = None):
        self.model = TFIDFEmbeddings()
        self.model_path = model_path
        self._dimension = 0

    def encode(self, texts: List[str]) -> np.ndarray:
        vectors = self.model.transform(texts)
        self._dimension = vectors.shape[1] if len(vectors) > 0 else 0
        return vectors

    def encode_query(self, query: str) -> np.ndarray:
        return self.model.transform_query(query)

    def compute_similarity(self, qv: np.ndarray, dv: np.ndarray) -> np.ndarray:
        return self.model.similarity(qv, dv)

    @property
    def dimension(self) -> int:
        return self._dimension

    def save(self):
        if self.model_path:
            self.model.save(self.model_path)

    def load(self):
        if self.model_path and self.model_path.exists():
            self.model = TFIDFEmbeddings.load(self.model_path)
            self._dimension = 10000
            return True
        return False
