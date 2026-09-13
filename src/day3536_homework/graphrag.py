"""GraphRAG orchestration with suitability rules before final output."""

from .business_rules import is_eligible
from .fusion import reciprocal_rank_fusion
from .in_memory import InMemoryGraphRetriever, InMemoryVectorRetriever
from .models import Customer, Product, RetrievalHit


class GraphRAGRecommender:
    def __init__(
        self,
        graph: InMemoryGraphRetriever,
        vector: InMemoryVectorRetriever,
        products: tuple[Product, ...],
    ) -> None:
        self.graph = graph
        self.vector = vector
        self.products = {product.product_id: product for product in products}

    def recommend(self, customer: Customer, query: str, limit: int = 3) -> list[RetrievalHit]:
        graph_hits = self.graph.retrieve(customer.customer_id)
        community_hits = self.graph.community_retrieve(customer.customer_id)
        vector_hits = self.vector.retrieve(query)
        merged = reciprocal_rank_fusion(
            (("graph", graph_hits), ("community", community_hits), ("vector", vector_hits)),
            limit=20,
        )
        safe = [hit for hit in merged if is_eligible(customer, self.products[hit.product_id])]
        for hit in safe:
            if not hit.explanation:
                hit.explanation = "语义与用户需求相似，并已通过风险和起购金额规则"
        return safe[:limit]
