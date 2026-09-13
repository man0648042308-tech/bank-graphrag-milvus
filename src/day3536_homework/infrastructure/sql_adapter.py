"""SQLAlchemy adapter that executes already validated read-only queries."""

from sqlalchemy import Engine, create_engine, text


class SQLAdapter:
    def __init__(self, url: str) -> None:
        self.engine: Engine = create_engine(url)

    def read(self, query: str) -> list[dict[str, object]]:
        with self.engine.connect() as connection:
            return [dict(row) for row in connection.execute(text(query)).mappings()]

    def dispose(self) -> None:
        self.engine.dispose()
