MATCH (n {dataset_id:'day3536'})
WITH labels(n)[0] AS label, count(*) AS count
RETURN label, count ORDER BY label;

MATCH (source:Station {dataset_id:'day3536', name:'A站'}),
      (target:Station {dataset_id:'day3536', name:'D站'})
CALL gds.shortestPath.dijkstra.stream('day3536_train', {
  sourceNode:source, targetNodes:target, relationshipWeightProperty:'distance'
})
YIELD totalCost, nodeIds
RETURN totalCost = 3.0 AS PASS_DIJKSTRA_COST,
       [nodeId IN nodeIds | gds.util.asNode(nodeId).name] = ['A站','B站','D站'] AS PASS_DIJKSTRA_PATH;

MATCH (c:Customer {dataset_id:'day3536', customer_id:'C001'})
MATCH (p:Product {dataset_id:'day3536'})
WHERE p.active = true
  AND p.risk_score <= c.risk_score
  AND p.min_investment <= c.available_amount
WITH collect(p.product_id) AS ids
RETURN all(expected IN ['P001','P002','P005'] WHERE expected IN ids)
       AND size(ids)=3 AS PASS_BUSINESS_RULES;

CALL gds.louvain.stats('day3536_social', {relationshipWeightProperty:'strength'})
YIELD communityCount, modularity
RETURN communityCount >= 2 AS PASS_LOUVAIN_COMMUNITIES,
       modularity > 0 AS PASS_LOUVAIN_MODULARITY;

