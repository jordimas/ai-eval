"""Shared ASR evaluation helpers."""

import hashlib
import json
import re
import unicodedata
from pathlib import Path


def normalize_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text.lower())
    text = re.sub(r"[^\w\s]", "", text)
    return re.sub(r"\s+", " ", text).strip()


def load_manifest(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    expected = data.pop("sha256", None)
    actual = hashlib.sha256(
        json.dumps(
            data, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode()
    ).hexdigest()
    if not expected or expected != actual:
        raise ValueError(f"manifest hash mismatch: {path}")
    if not data.get("records"):
        raise ValueError(f"manifest contains no records: {path}")
    return {**data, "sha256": expected}
