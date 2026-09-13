"""Explicit live Neo4j/GDS check; excluded from normal pytest collection."""

from day3536_homework.infrastructure.neo4j_adapter import Neo4jAdapter
from day3536_homework.nl2cypher import NL2CypherService, RuleBasedCypherGenerator


def main() -> None:
    with Neo4jAdapter("bolt://127.0.0.1:7688") as neo4j:
        neo4j.verify()
        versions = neo4j.read(
            "RETURN apoc.version() AS apoc_version, gds.version() AS gds_version"
        )[0]
        counts = neo4j.read("MATCH (n {dataset_id:'day3536'}) RETURN count(n) AS node_count")[0]
        dijkstra = neo4j.read(
            "MATCH (s:Station {dataset_id:'day3536',name:'A站'}), "
            "(t:Station {dataset_id:'day3536',name:'D站'}) "
            "CALL gds.shortestPath.dijkstra.stream('day3536_train', "
            "{sourceNode:s,targetNodes:t,relationshipWeightProperty:'distance'}) "
            "YIELD totalCost,nodeIds "
            "RETURN totalCost, "
            "[id IN nodeIds | gds.util.asNode(id).name] AS path"
        )[0]

        service = NL2CypherService(RuleBasedCypherGenerator(), neo4j.read)
        nl_result = service.query("查询客户C001购买的所有产品")

    assert versions["gds_version"].startswith("2.13.")
    assert counts["node_count"] == 29
    assert dijkstra == {"totalCost": 3.0, "path": ["A站", "B站", "D站"]}
    assert [row["product_id"] for row in nl_result.rows] == ["P001", "P002"]
    print("NEO4J_INTEGRATION_PASS")
    print(versions)
    print(counts)
    print(dijkstra)
    print(nl_result.rows)


if __name__ == "__main__":
    main()
