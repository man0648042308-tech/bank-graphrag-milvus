USE day3536_bank;
SELECT COUNT(*) AS user_count FROM users WHERE risk_tolerance='稳健';
SELECT u.city, SUM(t.amount) AS total_amount
FROM users u JOIN transactions t ON t.user_id=u.user_id
GROUP BY u.city ORDER BY total_amount DESC;
SELECT DISTINCT u.user_id, u.name
FROM users u JOIN transactions t ON t.user_id=u.user_id
WHERE t.product_id='P001' ORDER BY u.user_id;
SELECT risk_level, AVG(expected_return) AS avg_return
FROM products GROUP BY risk_level ORDER BY risk_level;

