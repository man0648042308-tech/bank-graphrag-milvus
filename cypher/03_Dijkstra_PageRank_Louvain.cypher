// 清理旧内存投影；false表示不存在时不报错
CALL gds.graph.drop('day3536_train', false) YIELD graphName;
CALL gds.graph.drop('day3536_products', false) YIELD graphName;
CALL gds.graph.drop('day3536_social', false) YIELD graphName;
CALL gds.graph.drop('day3536_bipartite', false) YIELD graphName;

// Dijkstra：投影带distance权重的车站图
MATCH (source:Station {dataset_id:'day3536'})-[r:CONNECTION]->(target:Station {dataset_id:'day3536'})
RETURN gds.graph.project(
  'day3536_train', source, target,
  {relationshipProperties: r {.distance}}
) AS projection;

MATCH (source:Station {dataset_id:'day3536', name:'A站'}),
      (target:Station {dataset_id:'day3536', name:'D站'})
CALL gds.shortestPath.dijkstra.stream('day3536_train', {
  sourceNode: source,
  targetNodes: target,
  relationshipWeightProperty: 'distance'
})
YIELD totalCost, nodeIds
RETURN totalCost,
       [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS path;

// PageRank：产品共同购买有向图
MATCH (source:Product {dataset_id:'day3536'})-[r:CO_PURCHASED]->(target:Product {dataset_id:'day3536'})
RETURN gds.graph.project('day3536_products', source, target) AS projection;

CALL gds.pageRank.stream('day3536_products')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).product_id AS product_id,
       gds.util.asNode(nodeId).name AS product, score
ORDER BY score DESC, product_id;

// Louvain：客户关注关系按无向图投影
CALL gds.graph.project(
  'day3536_social',
  'Customer',
  {FOLLOWS: {orientation:'UNDIRECTED', properties:'strength'}}
) YIELD graphName, nodeCount, relationshipCount;

CALL gds.louvain.stream('day3536_social', {relationshipWeightProperty:'strength'})
YIELD nodeId, communityId
RETURN gds.util.asNode(nodeId).customer_id AS customer_id,
       gds.util.asNode(nodeId).name AS customer,
       communityId
ORDER BY communityId, customer_id;

// 节点相似度：客户-产品购买二部图
CALL gds.graph.project(
  'day3536_bipartite',
  ['Customer','Product'],
  {PURCHASED: {orientation:'UNDIRECTED'}}
) YIELD graphName, nodeCount, relationshipCount;

CALL gds.nodeSimilarity.stream('day3536_bipartite', {topK:5, similarityCutoff:0.0})
YIELD node1, node2, similarity
WITH gds.util.asNode(node1) AS left, gds.util.asNode(node2) AS right, similarity
WHERE left:Customer AND right:Customer
RETURN left.customer_id AS customer_1, right.customer_id AS customer_2, similarity
ORDER BY similarity DESC, customer_1, customer_2;

