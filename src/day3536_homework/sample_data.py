"""Deterministic fictional banking data used by unit tests and demos."""

from .models import Customer, Product

CUSTOMERS = (
    Customer("C001", "张明", risk_score=2, available_amount=5_000, community_id=1),
    Customer("C002", "李芳", risk_score=1, available_amount=100_000, community_id=1),
    Customer("C003", "王磊", risk_score=3, available_amount=20_000, community_id=2),
    Customer("C004", "陈静", risk_score=2, available_amount=500, community_id=2),
)

PRODUCTS = (
    Product("P001", "稳健理财", "理财", "低风险，收益稳定，适合稳健配置", 1, 1_000, 0.035),
    Product("P002", "成长基金", "基金", "中等风险，兼顾成长和长期收益", 2, 100, 0.060),
    Product("P003", "进取股票", "股票", "高风险高收益，适合进取投资者", 3, 1_000, 0.120),
    Product("P004", "私募尊享", "私募", "高门槛专业投资产品", 3, 100_000, 0.150),
    Product("P005", "灵活存款", "存款", "低风险，可灵活支取，重视流动性", 1, 50, 0.020),
)

PURCHASES: dict[str, tuple[str, ...]] = {
    "C001": ("P001", "P002"),
    "C002": ("P001", "P005"),
    "C003": ("P002", "P003"),
    "C004": ("P005",),
}
