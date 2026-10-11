"""Small deterministic helpers reused by tool implementations."""

from __future__ import annotations

import hashlib
import re
from collections.abc import Iterable, Mapping
from typing import Any


def require_text(payload: Mapping[str, Any], key: str, *, max_length: int = 20_000) -> str:
    value = str(payload.get(key, "")).strip()
    if not value:
        raise ValueError(f"{key} is required")
    if len(value) > max_length:
        raise ValueError(f"{key} exceeds {max_length} characters")
    return value


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, float(value)))


def stable_ref(prefix: str, *parts: Any) -> str:
    material = "|".join(str(part) for part in parts)
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()[:20]
    return f"{prefix}_{digest}"


def tokenize(text: str) -> set[str]:
    ascii_words = re.findall(r"[a-zA-Z0-9_]+", text.lower())
    chinese = [char for char in text if "\u4e00" <= char <= "\u9fff"]
    return set(ascii_words + chinese)


def keyword_score(text: str, keywords: Iterable[str]) -> float:
    keys = tuple(keywords)
    normalized = text.lower()
    hits = sum(1 for keyword in keys if keyword.lower() in normalized)
    return clamp(hits / max(len(keys), 1))


def overlap_score(left: str, right: str) -> float:
    a, b = tokenize(left), tokenize(right)
    return round(len(a & b) / max(len(a | b), 1), 4)


def list_of_mappings(payload: Mapping[str, Any], key: str) -> list[Mapping[str, Any]]:
    value = payload.get(key, [])
    if not isinstance(value, list) or any(not isinstance(item, Mapping) for item in value):
        raise ValueError(f"{key} must be a list of objects")
    return value

