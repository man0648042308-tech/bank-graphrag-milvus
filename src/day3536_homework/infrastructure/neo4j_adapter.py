"""Minimal Neo4j adapter with explicit read and write methods."""

from collections.abc import Mapping
from typing import Any

import neo4j
from neo4j import GraphDatabase


class Neo4jAdapter:
    def __init__(self, uri: str, username: str | None = None, password: str | None = None) -> None:
        auth = None if username is None else (username, password or "")
        self.driver = GraphDatabase.driver(uri, auth=auth)

    def verify(self) -> None:
        self.driver.verify_connectivity()

    def read(self, query: str, parameters: Mapping[str, Any] | None = None) -> list[dict[str, Any]]:
        records, _, _ = self.driver.execute_query(
            query,
            parameters_=dict(parameters or {}),
            routing_=neo4j.RoutingControl.READ,
        )
        return [record.data() for record in records]

    def write(
        self, query: str, parameters: Mapping[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        records, _, _ = self.driver.execute_query(
            query,
            parameters_=dict(parameters or {}),
            routing_=neo4j.RoutingControl.WRITE,
        )
        return [record.data() for record in records]

    def close(self) -> None:
        self.driver.close()

    def __enter__(self) -> "Neo4jAdapter":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
