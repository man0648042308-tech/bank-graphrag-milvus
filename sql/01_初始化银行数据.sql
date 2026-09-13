CREATE DATABASE IF NOT EXISTS day3536_bank CHARACTER SET utf8mb4;
USE day3536_bank;

CREATE TABLE IF NOT EXISTS users (
  user_id VARCHAR(16) PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  city VARCHAR(50) NOT NULL,
  risk_tolerance VARCHAR(20) NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
  product_id VARCHAR(16) PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  risk_level INT NOT NULL,
  expected_return DECIMAL(8,5) NOT NULL
);

CREATE TABLE IF NOT EXISTS transactions (
  transaction_id VARCHAR(16) PRIMARY KEY,
  user_id VARCHAR(16) NOT NULL,
  product_id VARCHAR(16) NOT NULL,
  amount DECIMAL(14,2) NOT NULL,
  transaction_date DATE NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (product_id) REFERENCES products(product_id)
);

DELETE FROM transactions;
DELETE FROM users;
DELETE FROM products;

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

