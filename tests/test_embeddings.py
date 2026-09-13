import pytest

from day3536_homework.embeddings import build_query_vector, cosine_similarity, normalize


def test_embedding_is_normalized() -> None:
    vector = build_query_vector("低风险稳健产品")
    assert sum(value * value for value in vector) == pytest.approx(1.0)
    assert vector[0] > vector[1]


def test_liquidity_changes_third_dimension() -> None:
    normal = build_query_vector("普通产品")
    liquid = build_query_vector("资金需要灵活使用")
    assert liquid[2] > normal[2]


def test_invalid_vectors_are_rejected() -> None:
    with pytest.raises(ValueError, match="维度"):
        cosine_similarity([1.0], [1.0, 2.0])
    with pytest.raises(ValueError, match="长度"):
        normalize([0.0, 0.0])
