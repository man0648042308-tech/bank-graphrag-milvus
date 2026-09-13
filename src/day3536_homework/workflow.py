"""LangGraph implementation of the GraphRAG recommendation workflow."""

from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from .business_rules import is_eligible
from .fusion import reciprocal_rank_fusion
from .in_memory import InMemoryGraphRetriever, InMemoryVectorRetriever
from .models import Customer, Product, RetrievalHit


class RecommendationState(TypedDict, total=False):
    customer: Customer
    query: str
    graph_hits: list[RetrievalHit]
    community_hits: list[RetrievalHit]
    vector_hits: list[RetrievalHit]
    merged_hits: list[RetrievalHit]
    final_hits: list[RetrievalHit]


class GraphRAGWorkflow:
    """A visible node-by-node pipeline that can later swap in real adapters."""

    def __init__(
        self,
        graph_retriever: InMemoryGraphRetriever,
        vector_retriever: InMemoryVectorRetriever,
        products: tuple[Product, ...],
    ) -> None:
        self.graph_retriever = graph_retriever
        self.vector_retriever = vector_retriever
        self.products = {product.product_id: product for product in products}
        self.graph = self._build()

    def _graph_retrieve(self, state: RecommendationState) -> RecommendationState:
        return {"graph_hits": self.graph_retriever.retrieve(state["customer"].customer_id)}

    def _community_retrieve(self, state: RecommendationState) -> RecommendationState:
        return {
            "community_hits": self.graph_retriever.community_retrieve(state["customer"].customer_id)
        }

    def _vector_retrieve(self, state: RecommendationState) -> RecommendationState:
        return {"vector_hits": self.vector_retriever.retrieve(state["query"])}

    @staticmethod
    def _fuse(state: RecommendationState) -> RecommendationState:
        return {
            "merged_hits": reciprocal_rank_fusion(
                (
                    ("graph", state["graph_hits"]),
                    ("community", state["community_hits"]),
                    ("vector", state["vector_hits"]),
                ),
                limit=20,
            )
        }

    def _filter(self, state: RecommendationState) -> RecommendationState:
        customer = state["customer"]
        safe = [
            hit
            for hit in state["merged_hits"]
            if is_eligible(customer, self.products[hit.product_id])
        ]
        for hit in safe:
            if not hit.explanation:
                hit.explanation = "多路召回后通过风险等级、起购金额和产品状态校验"
        return {"final_hits": safe[:3]}

    def _build(self):  # type: ignore[no-untyped-def]
        builder = StateGraph(RecommendationState)
        builder.add_node("graph_retrieve", self._graph_retrieve)
        builder.add_node("community_retrieve", self._community_retrieve)
        builder.add_node("vector_retrieve", self._vector_retrieve)
        builder.add_node("rrf_fuse", self._fuse)
        builder.add_node("business_filter", self._filter)
        builder.add_edge(START, "graph_retrieve")
        builder.add_edge("graph_retrieve", "community_retrieve")
        builder.add_edge("community_retrieve", "vector_retrieve")
        builder.add_edge("vector_retrieve", "rrf_fuse")
        builder.add_edge("rrf_fuse", "business_filter")
        builder.add_edge("business_filter", END)
        return builder.compile(name="day3536_bank_graphrag")

    def recommend(self, customer: Customer, query: str) -> list[RetrievalHit]:
        result = self.graph.invoke({"customer": customer, "query": query})
        return result["final_hits"]
