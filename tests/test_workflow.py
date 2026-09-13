from day3536_homework.in_memory import InMemoryGraphRetriever, InMemoryVectorRetriever
from day3536_homework.sample_data import CUSTOMERS, PRODUCTS, PURCHASES
from day3536_homework.workflow import GraphRAGWorkflow


def build_workflow() -> GraphRAGWorkflow:
    return GraphRAGWorkflow(
        InMemoryGraphRetriever(CUSTOMERS, PRODUCTS, PURCHASES),
        InMemoryVectorRetriever(PRODUCTS),
        PRODUCTS,
    )


def test_langgraph_workflow_has_all_required_nodes() -> None:
    workflow = build_workflow()
    node_names = set(workflow.graph.get_graph().nodes)
    assert {
        "graph_retrieve",
        "community_retrieve",
        "vector_retrieve",
        "rrf_fuse",
        "business_filter",
    }.issubset(node_names)


def test_langgraph_workflow_returns_only_suitable_products() -> None:
    workflow = build_workflow()
    results = workflow.recommend(CUSTOMERS[0], "稳健、低风险并且灵活")
    ids = [hit.product_id for hit in results]
    assert ids == ["P005", "P001", "P002"]
    assert "P003" not in ids
    assert "P004" not in ids
