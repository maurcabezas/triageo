"""
Knowledge base retrieval service.

Phase 3 implementation: keyword overlap scoring over local markdown docs.
Each .md file in KB_DIR is loaded once at startup and indexed.

Phase later: replace the keyword scorer with a vector embedding search
once sentence-transformers or a similar library is added.
"""

import re
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Words too common to be useful for matching
_STOP_WORDS = {
    "the", "and", "for", "that", "this", "with", "are", "from", "have",
    "not", "they", "their", "also", "will", "can", "has", "been", "but",
    "more", "when", "all", "any", "may", "its", "such", "than", "into",
    "per", "via", "our", "your", "you", "our", "was", "were", "who",
    "which", "what", "how", "why", "each", "both",
}


class _KBDoc:
    """Internal representation of one KB document."""

    def __init__(self, path: Path) -> None:
        self.id = path.stem
        raw = path.read_text(encoding="utf-8")

        # Extract title from first "# ..." line
        self.title = "Untitled"
        for line in raw.splitlines():
            stripped = line.strip()
            if stripped.startswith("# "):
                self.title = stripped[2:].strip()
                break

        # Excerpt: first 2 non-heading, non-empty lines of prose
        prose_lines = [
            l.strip()
            for l in raw.splitlines()
            if l.strip() and not l.strip().startswith("#")
        ]
        self.excerpt = " ".join(prose_lines[:2])[:300]

        # Full text lowercased for scoring (include KEYWORDS line)
        self.tokens: set[str] = self._tokenize(raw)

    @staticmethod
    def _tokenize(text: str) -> set[str]:
        words = re.findall(r"\b[a-z]{3,}\b", text.lower())
        return {w for w in words if w not in _STOP_WORDS}

    def score(self, query_tokens: set[str]) -> int:
        return len(query_tokens & self.tokens)


class KnowledgeBase:
    """
    Loads and indexes all .md files from kb_dir on construction.
    Call retrieve() with a ticket subject + description to get
    the top-k most relevant KB snippets.
    """

    def __init__(self, kb_dir: str) -> None:
        self._docs: list[_KBDoc] = []
        path = Path(kb_dir)
        if not path.exists():
            logger.warning("KB directory not found: %s — retrieval disabled", kb_dir)
            return
        for f in sorted(path.glob("*.md")):
            if f.name.startswith("."):
                continue
            try:
                self._docs.append(_KBDoc(f))
            except Exception:
                logger.exception("Failed to load KB doc: %s", f)
        logger.info("Knowledge base loaded: %d documents from %s", len(self._docs), kb_dir)

    def retrieve(self, subject: str, description: str, top_k: int = 3) -> list[str]:
        """
        Return up to top_k KB snippets most relevant to the given ticket.
        Each snippet is a short string: "[doc-id] Title: excerpt..."
        Returns an empty list if no docs score above zero.
        """
        if not self._docs:
            return []

        query_tokens = _KBDoc._tokenize(subject + " " + description)
        if not query_tokens:
            return []

        scored = [
            (doc.score(query_tokens), doc)
            for doc in self._docs
            if doc.score(query_tokens) > 0
        ]
        scored.sort(key=lambda x: x[0], reverse=True)

        return [
            f"[{doc.id}] {doc.title}: {doc.excerpt}"
            for _, doc in scored[:top_k]
        ]
