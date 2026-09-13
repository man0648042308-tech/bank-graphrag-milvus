"""Reciprocal Rank Fusion for combining heterogeneous retrieval paths."""

from collections.abc import Iterable

from .models import RetrievalHit


def reciprocal_rank_fusion(
    ranked_lists: Iterable[tuple[str, list[RetrievalHit]]], *, k: int = 60, limit: int = 5
) -> list[RetrievalHit]:
    if k <= 0:
        raise ValueError("k必须大于0")
    merged: dict[str, RetrievalHit] = {}
    for source, hits in ranked_lists:
        for rank, hit in enumerate(hits, start=1):
            current = merged.setdefault(
                hit.product_id,
                RetrievalHit(hit.product_id, hit.name, 0.0, set(), hit.explanation),
            )
            current.score += 1.0 / (k + rank)
            current.sources.add(source)
            if not current.explanation and hit.explanation:
                current.explanation = hit.explanation
    return sorted(merged.values(), key=lambda item: (-item.score, item.product_id))[:limit]
