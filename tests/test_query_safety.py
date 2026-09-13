import pytest

from day3536_homework.query_safety import validate_readonly_cypher, validate_readonly_sql

TABLES = {"users", "products", "transactions"}
LABELS = {"Customer", "Product"}


def test_select_gets_limit() -> None:
    result = validate_readonly_sql("SELECT * FROM users", allowed_tables=TABLES)
    assert result.endswith("LIMIT 100")


@pytest.mark.parametrize(
    "query",
    [
        "DELETE FROM users",
        "SELECT * FROM users; DROP TABLE users",
        "SELECT * FROM secrets",
        "UPDATE users SET name='x'",
    ],
)
def test_sql_writes_and_unknown_tables_are_blocked(query: str) -> None:
    with pytest.raises(ValueError):
        validate_readonly_sql(query, allowed_tables=TABLES)


def test_cypher_gets_limit() -> None:
    result = validate_readonly_cypher(
        "MATCH (c:Customer)-[:PURCHASED]->(p:Product) RETURN p.name",
        allowed_labels=LABELS,
    )
    assert result.endswith("LIMIT 100")


@pytest.mark.parametrize(
    "query",
    [
        "MATCH (c:Customer) DETACH DELETE c RETURN c",
        "CALL dbms.components() YIELD name RETURN name",
        "MATCH (x:Secret) RETURN x",
        "CREATE (c:Customer) RETURN c",
    ],
)
def test_unsafe_cypher_is_blocked(query: str) -> None:
    with pytest.raises(ValueError):
        validate_readonly_cypher(query, allowed_labels=LABELS)
