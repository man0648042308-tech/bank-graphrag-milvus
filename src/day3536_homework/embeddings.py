"""Deterministic four-dimensional teaching embeddings.

The dimensions represent safety, growth, liquidity, and return preference.  A real
project can replace this module with BGE, while the homework remains reproducible.
"""

import math


def normalize(vector: list[float]) -> list[float]:
    length = math.sqrt(sum(value * value for value in vector))
    if length == 0:
        raise ValueError("向量长度不能为0")
    return [value / length for value in vector]


def build_query_vector(text: str) -> list[float]:
    vector = [0.5, 0.5, 0.5, 0.5]
    if any(word in text for word in ("低风险", "稳健", "保本", "安全")):
        vector[0], vector[1] = 1.0, 0.2
    if any(word in text for word in ("高收益", "成长", "进取")):
        vector[1], vector[3] = 1.0, 0.9
    if any(word in text for word in ("灵活", "随时", "流动")):
        vector[2] = 1.0
    return normalize(vector)


def build_product_vector(description: str) -> list[float]:
    return build_query_vector(description)


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError("两个向量维度必须一致")
    return sum(a * b for a, b in zip(left, right, strict=True))


