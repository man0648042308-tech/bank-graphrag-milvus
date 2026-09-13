"""Deterministic retrievers used for tests, learning and offline demonstrations."""

from .embeddings import build_product_vector, build_query_vector, cosine_similarity
from .models import Customer, Product, RetrievalHit


class InMemoryVectorRetriever:
    def __init__(self, products: tuple[Product, ...]) -> None:
        self.products = products

    def retrieve(self, query: str, limit: int = 5) -> list[RetrievalHit]:
        query_vector = build_query_vector(query)
        hits = [
            RetrievalHit(
                product.product_id,
                product.name,
                cosine_similarity(query_vector, build_product_vector(product.description)),
                {"vector"},
            )
            for product in self.products
        ]
        return sorted(hits, key=lambda hit: (-hit.score, hit.product_id))[:limit]


class InMemoryGraphRetriever:
    def __init__(
        self,
        customers: tuple[Customer, ...],
        products: tuple[Product, ...],
        purchases: dict[str, tuple[str, ...]],
    ) -> None:
        self.customers = {customer.customer_id: customer for customer in customers}
        self.products = {product.product_id: product for product in products}
        self.purchases = purchases

    def retrieve(self, customer_id: str, limit: int = 5) -> list[RetrievalHit]:
        customer = self.customers[customer_id]
        own = set(self.purchases.get(customer_id, ()))
        votes: dict[str, int] = {}
        witnesses: dict[str, str] = {}
        for other_id, bought in self.purchases.items():
            if other_id == customer_id or not own.intersection(bought):
                continue
            common = sorted(own.intersection(bought))[0]
            for product_id in set(bought) - own:
                votes[product_id] = votes.get(product_id, 0) + 1
                witnesses[product_id] = (
                    f"客户{customer.name}与客户{self.customers[other_id].name}都购买过"
                    f"{self.products[common].name}；后者还购买了{self.products[product_id].name}"
                )
        hits = [
            RetrievalHit(
                product_id,
                self.products[product_id].name,
                float(vote),
                {"graph"},
                witnesses[product_id],
            )
            for product_id, vote in votes.items()
        ]
        return sorted(hits, key=lambda hit: (-hit.score, hit.product_id))[:limit]

    def community_retrieve(self, customer_id: str, limit: int = 5) -> list[RetrievalHit]:
        target = self.customers[customer_id]
        own = set(self.purchases.get(customer_id, ()))
        votes: dict[str, int] = {}
        for other in self.customers.values():
            if other.customer_id == customer_id or other.community_id != target.community_id:
                continue
            for product_id in set(self.purchases.get(other.customer_id, ())) - own:
                votes[product_id] = votes.get(product_id, 0) + 1
        return [
            RetrievalHit(
                product_id,
                self.products[product_id].name,
                float(vote),
                {"community"},
                f"同社区客户购买热度为{vote}",
            )
            for product_id, vote in sorted(votes.items(), key=lambda item: (-item[1], item[0]))[
                :limit
            ]
        ]
