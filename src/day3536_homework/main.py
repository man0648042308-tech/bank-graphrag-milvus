"""Offline golden-path demo."""

import json

from .in_memory import InMemoryGraphRetriever, InMemoryVectorRetriever
from .sample_data import CUSTOMERS, PRODUCTS, PURCHASES
from .workflow import GraphRAGWorkflow


def main() -> None:
    graph = InMemoryGraphRetriever(CUSTOMERS, PRODUCTS, PURCHASES)
    vector = InMemoryVectorRetriever(PRODUCTS)
    recommender = GraphRAGWorkflow(graph, vector, PRODUCTS)
    results = recommender.recommend(CUSTOMERS[0], "稳健、低风险并且可以灵活使用")
    print(
        json.dumps(
            [
                {
                    "product_id": hit.product_id,
                    "name": hit.name,
                    "score": round(hit.score, 6),
                    "sources": sorted(hit.sources),
                    "explanation": hit.explanation,
                }
                for hit in results
            ],
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
