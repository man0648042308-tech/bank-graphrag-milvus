import pytest

from day3536_homework.evaluation import precision_at_k
from day3536_homework.models import RetrievalHit


def test_precision_at_k_uses_only_the_first_k_results() -> None:
    hits = [
        RetrievalHit("P001", "稳健理财", 1.0),
        RetrievalHit("P003", "进取股票", 0.9),
        RetrievalHit("P005", "灵活存款", 0.8),
    ]
    assert precision_at_k(hits, frozenset({"P001", "P005"}), k=2) == 0.5


def test_precision_at_k_rejects_invalid_k() -> None:
    with pytest.raises(ValueError, match="k必须大于0"):
        precision_at_k([], frozenset(), k=0)
