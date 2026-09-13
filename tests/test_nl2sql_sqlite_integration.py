import sqlite3

from day3536_homework.nl2sql import NL2SQLService, RuleBasedSQLGenerator


def build_database() -> sqlite3.Connection:
    connection = sqlite3.connect(":memory:")
    connection.row_factory = sqlite3.Row
    connection.executescript(
        """
        CREATE TABLE users (
          user_id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          city TEXT NOT NULL,
          risk_tolerance TEXT NOT NULL
        );
        CREATE TABLE products (
          product_id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          risk_level INTEGER NOT NULL,
          expected_return REAL NOT NULL
        );
        CREATE TABLE transactions (
          transaction_id TEXT PRIMARY KEY,
          user_id TEXT NOT NULL,
          product_id TEXT NOT NULL,
          amount REAL NOT NULL,
          transaction_date TEXT NOT NULL
        );
        INSERT INTO users VALUES
          ('C001','张明','深圳','稳健'),
          ('C002','李芳','广州','保守'),
          ('C003','王磊','深圳','进取'),
          ('C004','陈静','上海','稳健');
        INSERT INTO products VALUES
          ('P001','稳健理财',1,0.035),
          ('P002','成长基金',2,0.060),
          ('P003','进取股票',3,0.120),
          ('P005','灵活存款',1,0.020);
        INSERT INTO transactions VALUES
          ('BT001','C001','P001',1000.00,'2026-08-01'),
          ('BT002','C001','P002',500.00,'2026-08-02'),
          ('BT003','C002','P001',2000.00,'2026-08-03'),
          ('BT004','C003','P003',3000.00,'2026-08-04');
        """
    )
    return connection


def test_all_four_nl2sql_examples_execute_on_a_real_sql_engine() -> None:
    connection = build_database()

    def execute(sql: str) -> list[dict[str, object]]:
        return [dict(row) for row in connection.execute(sql).fetchall()]

    service = NL2SQLService(RuleBasedSQLGenerator(), execute)
    questions = (
        "查询风险偏好为稳健的用户有多少人",
        "统计每个城市用户的总购买金额",
        "找出购买过产品P001的用户列表",
        "统计每个风险等级产品的平均年化收益率",
    )
    results = [service.query(question) for question in questions]
    assert results[0].rows == ({"user_count": 2},)
    assert results[1].rows[0] == {"city": "深圳", "total_amount": 4500.0}
    assert [row["user_id"] for row in results[2].rows] == ["C001", "C002"]
    assert len(results[3].rows) == 3
    connection.close()
