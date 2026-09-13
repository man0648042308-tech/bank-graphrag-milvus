from day3536_homework.graphrag import GraphRAGRecommender
from day3536_homework.in_memory import InMemoryGraphRetriever, InMemoryVectorRetriever
from day3536_homework.sample_data import CUSTOMERS, PRODUCTS, PURCHASES


def build_recommender() -> GraphRAGRecommender:
    return GraphRAGRecommender(
        InMemoryGraphRetriever(CUSTOMERS, PRODUCTS, PURCHASES),
        InMemoryVectorRetriever(PRODUCTS),
        PRODUCTS,
    )


def test_graphrag_returns_explainable_and_safe_results() -> None:
    results = build_recommender().recommend(CUSTOMERS[0], "低风险稳健并且灵活")
    assert results
    assert all(result.explanation for result in results)
    assert all(result.product_id not in {"P003", "P004"} for result in results)


def test_low_amount_customer_never_gets_expensive_products() -> None:
    results = build_recommender().recommend(CUSTOMERS[3], "高收益产品")
    assert {result.product_id for result in results} <= {"P002", "P005"}
