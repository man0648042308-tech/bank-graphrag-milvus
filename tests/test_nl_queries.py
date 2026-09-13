from collections.abc import Mapping

from day3536_homework.nl2cypher import NL2CypherService, RuleBasedCypherGenerator
from day3536_homework.nl2sql import NL2SQLService, RuleBasedSQLGenerator


def test_nl2sql_separates_generation_validation_and_execution() -> None:
    captured: list[str] = []

    def execute(sql: str) -> list[dict[str, object]]:
        captured.append(sql)
        return [{"user_count": 2}]

    service = NL2SQLService(RuleBasedSQLGenerator(), execute)
    result = service.query("查询风险偏好为稳健的用户有多少人")
    assert result.rows == ({"user_count": 2},)
    assert captured[0].endswith("LIMIT 100")


def test_nl2cypher_separates_generation_validation_and_execution() -> None:
    captured: list[str] = []
    captured_parameters: list[Mapping[str, object]] = []

    def execute(cypher: str, parameters: Mapping[str, object]) -> list[dict[str, object]]:
        captured.append(cypher)
        captured_parameters.append(parameters)
        return [{"product_id": "P001", "name": "稳健理财"}]

    service = NL2CypherService(RuleBasedCypherGenerator(), execute)
    result = service.query("查询客户C001购买的所有产品")
    assert result.rows[0]["product_id"] == "P001"
    assert captured[0].endswith("LIMIT 100")
    assert captured_parameters[0] == {"customer_id": "C001"}
