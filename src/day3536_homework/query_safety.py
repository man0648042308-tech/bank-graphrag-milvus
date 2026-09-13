"""Guards for model-generated SQL and Cypher.

Generation and execution are intentionally separated.  A query must pass these
guards before an adapter may send it to a database.
"""

import re

from sqlglot import exp, parse

SQL_FORBIDDEN = (
    exp.Insert,
    exp.Update,
    exp.Delete,
    exp.Drop,
    exp.Alter,
    exp.Create,
    exp.Command,
    exp.Copy,
    exp.Merge,
)

CYPHER_FORBIDDEN = re.compile(
    r"\b(CREATE|MERGE|DELETE|DETACH|SET|REMOVE|DROP|LOAD\s+CSV|FOREACH|GRANT|DENY|REVOKE|STOP|START)\b",
    re.IGNORECASE,
)


def validate_readonly_sql(sql: str, *, allowed_tables: set[str], max_rows: int = 100) -> str:
    if max_rows <= 0:
        raise ValueError("max_rows必须大于0")
    statements = parse(sql, read="mysql")
    if len(statements) != 1:
        raise ValueError("只允许一条SQL语句")
    statement = statements[0]
    if any(statement.find(kind) is not None for kind in SQL_FORBIDDEN):
        raise ValueError("只允许只读SELECT/WITH查询")
    if statement.find(exp.Select) is None:
        raise ValueError("查询必须包含SELECT")
    tables = {table.name.lower() for table in statement.find_all(exp.Table)}
    unknown = tables - {name.lower() for name in allowed_tables}
    if unknown:
        raise ValueError(f"查询包含未授权表: {sorted(unknown)}")
    cleaned = sql.strip().rstrip(";")
    if statement.args.get("limit") is None:
        cleaned = f"{cleaned} LIMIT {max_rows}"
    return cleaned


def validate_readonly_cypher(cypher: str, *, allowed_labels: set[str], max_rows: int = 100) -> str:
    cleaned = cypher.strip().rstrip(";")
    if not cleaned:
        raise ValueError("Cypher不能为空")
    if ";" in cleaned:
        raise ValueError("只允许一条Cypher语句")
    if CYPHER_FORBIDDEN.search(cleaned):
        raise ValueError("Cypher包含写入或管理命令")
    if re.search(r"\bCALL\b", cleaned, re.IGNORECASE):
        raise ValueError("自然语言查询不允许直接调用过程")
    if not re.search(r"\bMATCH\b", cleaned, re.IGNORECASE):
        raise ValueError("Cypher必须包含MATCH")
    if not re.search(r"\bRETURN\b", cleaned, re.IGNORECASE):
        raise ValueError("Cypher必须包含RETURN")
    labels = set(re.findall(r"\([A-Za-z_]\w*\s*:\s*([A-Za-z_]\w*)", cleaned))
    unknown = labels - allowed_labels
    if unknown:
        raise ValueError(f"Cypher包含未授权标签: {sorted(unknown)}")
    if not re.search(r"\bLIMIT\s+\d+\b", cleaned, re.IGNORECASE):
        cleaned = f"{cleaned} LIMIT {max_rows}"
    return cleaned
