// 仅清理本作业数据；禁止改成 MATCH (n) DETACH DELETE n
MATCH (n {dataset_id: 'day3536'}) DETACH DELETE n;

CREATE CONSTRAINT day3536_customer_id IF NOT EXISTS
FOR (n:Customer) REQUIRE n.customer_id IS UNIQUE;
CREATE CONSTRAINT day3536_product_id IF NOT EXISTS
FOR (n:Product) REQUIRE n.product_id IS UNIQUE;
CREATE CONSTRAINT day3536_account_id IF NOT EXISTS
FOR (n:Account) REQUIRE n.account_id IS UNIQUE;
CREATE CONSTRAINT day3536_transaction_id IF NOT EXISTS
FOR (n:Transaction) REQUIRE n.transaction_id IS UNIQUE;
CREATE CONSTRAINT day3536_merchant_id IF NOT EXISTS
FOR (n:Merchant) REQUIRE n.merchant_id IS UNIQUE;

CREATE
  (c1:Customer {dataset_id:'day3536', customer_id:'C001', name:'张明', age:35, city:'深圳', risk_score:2, risk_tolerance:'稳健', available_amount:5000.0}),
  (c2:Customer {dataset_id:'day3536', customer_id:'C002', name:'李芳', age:42, city:'广州', risk_score:1, risk_tolerance:'保守', available_amount:100000.0}),
  (c3:Customer {dataset_id:'day3536', customer_id:'C003', name:'王磊', age:28, city:'深圳', risk_score:3, risk_tolerance:'进取', available_amount:20000.0}),
  (c4:Customer {dataset_id:'day3536', customer_id:'C004', name:'陈静', age:31, city:'上海', risk_score:2, risk_tolerance:'稳健', available_amount:500.0}),

  (a1:Account {dataset_id:'day3536', account_id:'A001', balance:50000.0}),
  (a2:Account {dataset_id:'day3536', account_id:'A002', balance:30000.0}),
  (a3:Account {dataset_id:'day3536', account_id:'A003', balance:80000.0}),
  (a4:Account {dataset_id:'day3536', account_id:'A004', balance:20000.0}),

  (m1:Merchant {dataset_id:'day3536', merchant_id:'M001', name:'星巴克咖啡', category:'餐饮'}),
  (m2:Merchant {dataset_id:'day3536', merchant_id:'M002', name:'数码商城', category:'数码'}),
  (m3:Merchant {dataset_id:'day3536', merchant_id:'M003', name:'社区超市', category:'商超'}),
  (m4:Merchant {dataset_id:'day3536', merchant_id:'M004', name:'城市票务', category:'票务'}),

  (t1:Transaction {dataset_id:'day3536', transaction_id:'T001', amount:88.5, status:'成功', tx_date:date('2026-08-01')}),
  (t2:Transaction {dataset_id:'day3536', transaction_id:'T002', amount:350.2, status:'成功', tx_date:date('2026-08-02')}),
  (t3:Transaction {dataset_id:'day3536', transaction_id:'T003', amount:150.75, status:'成功', tx_date:date('2026-08-03')}),
  (t4:Transaction {dataset_id:'day3536', transaction_id:'T004', amount:2500.0, status:'成功', tx_date:date('2026-08-04')}),
  (t5:Transaction {dataset_id:'day3536', transaction_id:'T005', amount:6899.0, status:'成功', tx_date:date('2026-08-05')}),
  (t6:Transaction {dataset_id:'day3536', transaction_id:'T006', amount:25.0, status:'成功', tx_date:date('2026-08-06')}),

  (p1:Product {dataset_id:'day3536', product_id:'P001', name:'稳健理财', category:'理财', description:'低风险，收益稳定，适合稳健配置', risk_score:1, risk_level:'低', min_investment:1000.0, expected_return:0.035, active:true, embedding:[0.84,0.17,0.42,0.25]}),
  (p2:Product {dataset_id:'day3536', product_id:'P002', name:'成长基金', category:'基金', description:'中等风险，兼顾成长和长期收益', risk_score:2, risk_level:'中', min_investment:100.0, expected_return:0.06, active:true, embedding:[0.35,0.70,0.35,0.52]}),
  (p3:Product {dataset_id:'day3536', product_id:'P003', name:'进取股票', category:'股票', description:'高风险高收益，适合进取投资者', risk_score:3, risk_level:'高', min_investment:1000.0, expected_return:0.12, active:true, embedding:[0.18,0.71,0.35,0.58]}),
  (p4:Product {dataset_id:'day3536', product_id:'P004', name:'私募尊享', category:'私募', description:'高门槛专业投资产品', risk_score:3, risk_level:'高', min_investment:100000.0, expected_return:0.15, active:true, embedding:[0.12,0.65,0.20,0.72]}),
  (p5:Product {dataset_id:'day3536', product_id:'P005', name:'灵活存款', category:'存款', description:'低风险，可灵活支取，重视流动性', risk_score:1, risk_level:'低', min_investment:50.0, expected_return:0.02, active:true, embedding:[0.70,0.20,0.67,0.14]}),

  (c1)-[:HOLDS]->(a1), (c1)-[:HOLDS]->(a2), (c2)-[:HOLDS]->(a3), (c3)-[:HOLDS]->(a4),
  (a1)-[:MADE]->(t1), (a1)-[:MADE]->(t2), (a2)-[:MADE]->(t3),
  (a3)-[:MADE]->(t4), (a4)-[:MADE]->(t5), (a1)-[:MADE]->(t6),
  (t1)-[:PAID_TO]->(m1), (t2)-[:PAID_TO]->(m3), (t3)-[:PAID_TO]->(m4),
  (t4)-[:PAID_TO]->(m1), (t5)-[:PAID_TO]->(m2), (t6)-[:PAID_TO]->(m1),

  (c1)-[:PURCHASED {amount:1000.0}]->(p1), (c1)-[:PURCHASED {amount:500.0}]->(p2),
  (c2)-[:PURCHASED {amount:2000.0}]->(p1), (c2)-[:PURCHASED {amount:3000.0}]->(p5),
  (c3)-[:PURCHASED {amount:1500.0}]->(p2), (c3)-[:PURCHASED {amount:2000.0}]->(p3),
  (c4)-[:PURCHASED {amount:100.0}]->(p5),

  (c1)-[:FOLLOWS {strength:5.0}]->(c2), (c2)-[:FOLLOWS {strength:4.0}]->(c1),
  (c3)-[:FOLLOWS {strength:5.0}]->(c4), (c4)-[:FOLLOWS {strength:4.0}]->(c3),
  (c2)-[:FOLLOWS {strength:0.2}]->(c3),

  (p1)-[:SIMILAR {distance:1.0}]->(p5), (p1)-[:SIMILAR {distance:2.0}]->(p2),
  (p2)-[:SIMILAR {distance:1.0}]->(p3), (p3)-[:SIMILAR {distance:3.0}]->(p4),
  (p1)-[:CO_PURCHASED]->(p2), (p2)-[:CO_PURCHASED]->(p3),
  (p5)-[:CO_PURCHASED]->(p1), (p2)-[:CO_PURCHASED]->(p1);

CREATE
  (s1:Station {dataset_id:'day3536', name:'A站'}),
  (s2:Station {dataset_id:'day3536', name:'B站'}),
  (s3:Station {dataset_id:'day3536', name:'C站'}),
  (s4:Station {dataset_id:'day3536', name:'D站'}),
  (s1)-[:CONNECTION {distance:1.0}]->(s2),
  (s2)-[:CONNECTION {distance:2.0}]->(s4),
  (s1)-[:CONNECTION {distance:5.0}]->(s3),
  (s3)-[:CONNECTION {distance:1.0}]->(s4);

RETURN 'DAY3536_DATA_READY' AS status;

