"""Small deterministic retrieval evaluation set."""

from dataclasses import dataclass

from .models import RetrievalHit


@dataclass(frozen=True, slots=True)
class EvalCase:
    query: str
    relevant_ids: frozenset[str]


EVAL_CASES = (
    EvalCase("低风险稳健理财", frozenset({"P001", "P005"})),
    EvalCase("高收益成长产品", frozenset({"P002", "P003"})),
    EvalCase("灵活使用资金", frozenset({"P005"})),
)


def precision_at_k(hits: list[RetrievalHit], relevant: frozenset[str], k: int = 3) -> float:
    if k <= 0:
        raise ValueError("k必须大于0")
    selected = hits[:k]
    if not selected:
        return 0.0
    correct = sum(hit.product_id in relevant for hit in selected)
    return correct / len(selected)
