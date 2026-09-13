"""Safe NL2Cypher pipeline with parameterized deterministic examples."""

from collections.abc import Callable, Mapping

from .models import QueryResult
from .query_safety import validate_readonly_cypher

CYPHER_EXAMPLES = {
    "查询客户C001购买的所有产品": (
        "MATCH (c:Customer {customer_id: $customer_id})-[:PURCHASED]->(p:Product) "
        "RETURN p.product_id AS product_id, p.name AS name ORDER BY product_id"
    ),
    "找出与C001有社交关系的其他客户": (
        "MATCH (c:Customer {customer_id: $customer_id})-[:FOLLOWS]-(other:Customer) "
        "RETURN DISTINCT other.customer_id AS customer_id, other.name AS name ORDER BY customer_id"
    ),
    "查找与P001相似的产品": (
        "MATCH (p:Product {product_id: $product_id})-[:SIMILAR]-(other:Product) "
        "RETURN other.product_id AS product_id, other.name AS name ORDER BY product_id"
    ),
    "统计每个客户购买产品的数量": (
        "MATCH (c:Customer) OPTIONAL MATCH (c)-[:PURCHASED]->(p:Product) "
        "RETURN c.customer_id AS customer_id, count(p) AS product_count ORDER BY customer_id"
    ),
}

CYPHER_PARAMETERS: dict[str, dict[str, object]] = {
    "查询客户C001购买的所有产品": {"customer_id": "C001"},
    "找出与C001有社交关系的其他客户": {"customer_id": "C001"},
    "查找与P001相似的产品": {"product_id": "P001"},
    "统计每个客户购买产品的数量": {},
}


class RuleBasedCypherGenerator:
    def generate(self, natural_language: str) -> str:
        try:
            return CYPHER_EXAMPLES[natural_language]
        except KeyError as error:
            raise ValueError("当前基线没有该问题的示例，请接入模型生成器") from error


class NL2CypherService:
    def __init__(
        self,
        generator: RuleBasedCypherGenerator,
        executor: Callable[[str, Mapping[str, object]], list[dict[str, object]]],
    ) -> None:
        self.generator = generator
        self.executor = executor
        self.allowed_labels = {"Customer", "Product", "Account", "Transaction", "Merchant"}

    def query(self, natural_language: str) -> QueryResult:
        generated = self.generator.generate(natural_language)
        safe_query = validate_readonly_cypher(generated, allowed_labels=self.allowed_labels)
        parameters = CYPHER_PARAMETERS[natural_language]
        rows = tuple(self.executor(safe_query, parameters))
        return QueryResult(natural_language, safe_query, rows)
