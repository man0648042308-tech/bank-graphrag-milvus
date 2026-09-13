from day3536_homework.fusion import reciprocal_rank_fusion
from day3536_homework.models import RetrievalHit


def test_rrf_merges_sources_and_rewards_overlap() -> None:
    graph = [RetrievalHit("P001", "稳健理财", 1.0), RetrievalHit("P002", "成长基金", 0.8)]
    vector = [RetrievalHit("P002", "成长基金", 0.9), RetrievalHit("P003", "进取股票", 0.7)]
    result = reciprocal_rank_fusion((("graph", graph), ("vector", vector)))
    assert result[0].product_id == "P002"
    assert result[0].sources == {"graph", "vector"}


def test_rrf_rejects_non_positive_k() -> None:
    try:
        reciprocal_rank_fusion((), k=0)
    except ValueError as error:
        assert "大于0" in str(error)
    else:
        raise AssertionError("k=0必须失败")
