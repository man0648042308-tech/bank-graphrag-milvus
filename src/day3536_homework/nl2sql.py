"""Safe NL2SQL pipeline with a deterministic teaching generator."""

from collections.abc import Callable

from .models import QueryResult
from .query_safety import validate_readonly_sql

SQL_EXAMPLES = {
    "查询风险偏好为稳健的用户有多少人": (
        "SELECT COUNT(*) AS user_count FROM users WHERE risk_tolerance = '稳健'"
    ),
    "统计每个城市用户的总购买金额": (
        "SELECT u.city, SUM(t.amount) AS total_amount FROM users u "
        "JOIN transactions t ON t.user_id = u.user_id GROUP BY u.city ORDER BY total_amount DESC"
    ),
    "找出购买过产品P001的用户列表": (
        "SELECT DISTINCT u.user_id, u.name FROM users u JOIN transactions t "
        "ON t.user_id = u.user_id WHERE t.product_id = 'P001' ORDER BY u.user_id"
    ),
    "统计每个风险等级产品的平均年化收益率": (
        "SELECT risk_level, AVG(expected_return) AS avg_return FROM products "
        "GROUP BY risk_level ORDER BY risk_level"
    ),
}


class RuleBasedSQLGenerator:
    """Reproducible baseline; replaceable by an LLM adapter without changing safety."""

    def generate(self, natural_language: str) -> str:
        try:
            return SQL_EXAMPLES[natural_language]
        except KeyError as error:
            raise ValueError("当前基线没有该问题的示例，请接入模型生成器") from error


class NL2SQLService:
    def __init__(
        self,
        generator: RuleBasedSQLGenerator,
        executor: Callable[[str], list[dict[str, object]]],
    ) -> None:
        self.generator = generator
        self.executor = executor
        self.allowed_tables = {"users", "products", "transactions"}

    def query(self, natural_language: str) -> QueryResult:
        generated = self.generator.generate(natural_language)
        safe_query = validate_readonly_sql(generated, allowed_tables=self.allowed_tables)
        rows = tuple(self.executor(safe_query))
        return QueryResult(natural_language, safe_query, rows)
