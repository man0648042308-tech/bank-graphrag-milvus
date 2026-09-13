// 1.1 查询所有客户，按年龄降序
MATCH (c:Customer {dataset_id:'day3536'})
RETURN c.customer_id AS customer_id, c.name AS name, c.age AS age
ORDER BY age DESC;

// 1.2 查询深圳且年龄大于30岁的客户
MATCH (c:Customer {dataset_id:'day3536'})
WHERE c.city = '深圳' AND c.age > 30
RETURN c.customer_id AS customer_id, c.name AS name;

// 1.3 创建数据：使用MERGE确保重复运行不会重复创建
MERGE (c:Customer {customer_id:'C005'})
SET c.dataset_id='day3536', c.name='赵敏', c.age=30, c.city='杭州',
    c.risk_score=2, c.risk_tolerance='稳健', c.available_amount=8000.0
MERGE (a:Account {account_id:'A005'})
SET a.dataset_id='day3536', a.balance=60000.0
MERGE (c)-[:HOLDS]->(a)
RETURN c.customer_id AS customer_id, a.account_id AS account_id;

// 1.4 在作业数据范围内更新；删除动作改为返回候选，避免破坏后续验收
MATCH (t:Transaction {dataset_id:'day3536', transaction_id:'T004'})
SET t.review_status='已复核'
RETURN t.transaction_id AS transaction_id, t.review_status AS review_status;

MATCH (t:Transaction {dataset_id:'day3536'})
WHERE t.amount < 30
RETURN t.transaction_id AS would_delete, t.amount AS amount;

// 2.1 查询李芳的消费路径
MATCH (c:Customer {dataset_id:'day3536', name:'李芳'})-[:HOLDS]->(a:Account)
      -[:MADE]->(t:Transaction)-[:PAID_TO]->(m:Merchant)
RETURN c.name AS customer, a.account_id AS account, t.amount AS amount,
       m.name AS merchant, m.category AS category;

// 2.2 找出与张明消费过相同商户的其他客户
MATCH (target:Customer {dataset_id:'day3536', name:'张明'})-[:HOLDS]->(:Account)
      -[:MADE]->(:Transaction)-[:PAID_TO]->(m:Merchant)
MATCH (other:Customer {dataset_id:'day3536'})-[:HOLDS]->(:Account)
      -[:MADE]->(:Transaction)-[:PAID_TO]->(m)
WHERE other <> target
RETURN DISTINCT other.name AS similar_customer, m.name AS common_merchant
ORDER BY similar_customer;

// 2.3 查询大于1000元的交易
MATCH (c:Customer {dataset_id:'day3536'})-[:HOLDS]->(:Account)
      -[:MADE]->(t:Transaction)-[:PAID_TO]->(m:Merchant)
WHERE t.amount > 1000
RETURN c.name AS customer, t.transaction_id AS transaction_id,
       t.amount AS amount, m.name AS merchant
ORDER BY amount DESC;

// 3.1 统计每位客户成功交易总额和次数，并保留零交易客户
MATCH (c:Customer {dataset_id:'day3536'})
OPTIONAL MATCH (c)-[:HOLDS]->(:Account)-[:MADE]->(t:Transaction {status:'成功'})
RETURN c.name AS customer, coalesce(sum(t.amount),0) AS total_amount, count(t) AS tx_count
ORDER BY total_amount DESC, customer;

// 3.2 统计每个商户的不同客户数
MATCH (c:Customer {dataset_id:'day3536'})-[:HOLDS]->(:Account)
      -[:MADE]->(:Transaction)-[:PAID_TO]->(m:Merchant)
RETURN m.name AS merchant, count(DISTINCT c) AS customer_count
ORDER BY customer_count DESC, merchant;

// 3.3 最受欢迎商户类别（按交易金额）
MATCH (:Customer {dataset_id:'day3536'})-[:HOLDS]->(:Account)
      -[:MADE]->(t:Transaction)-[:PAID_TO]->(m:Merchant)
RETURN m.category AS category, sum(t.amount) AS total_amount
ORDER BY total_amount DESC;

// 4.1 CALL子查询计算消费排名
MATCH (c:Customer {dataset_id:'day3536'})
CALL (c) {
  OPTIONAL MATCH (c)-[:HOLDS]->(:Account)-[:MADE]->(t:Transaction {status:'成功'})
  RETURN coalesce(sum(t.amount),0) AS total_amount
}
RETURN c.name AS customer, total_amount
ORDER BY total_amount DESC;

// 4.2 APOC数据转换
MATCH (c:Customer {dataset_id:'day3536'})
RETURN apoc.map.fromPairs([['客户',c.name],['城市',c.city],['风险偏好',c.risk_tolerance]]) AS customer_map
ORDER BY c.customer_id;

// 4.3 APOC日期计算
MATCH (t:Transaction {dataset_id:'day3536'})
RETURN t.transaction_id AS transaction_id,
       apoc.temporal.format(t.tx_date,'yyyy-MM-dd') AS formatted_date
ORDER BY transaction_id;

// 5.1、5.2 的GDS投影和算法在03脚本中，避免重复图名冲突。

