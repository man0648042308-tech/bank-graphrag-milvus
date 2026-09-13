"""第 1 关：跟做硬规则。把三个 TODO 逐个替换成正确条件。"""


def is_eligible(customer: dict[str, object], product: dict[str, object]) -> bool:
    product_is_active = False  # TODO 1：从产品字典读取 active
    risk_is_safe = False  # TODO 2：产品风险不高于客户风险
    amount_is_enough = False  # TODO 3：可用金额不低于起购金额
    return product_is_active and risk_is_safe and amount_is_enough


customer = {"risk_score": 2, "available_amount": 5000.0}
product = {"risk_score": 1, "min_investment": 1000.0, "active": True}
print(is_eligible(customer, product))
