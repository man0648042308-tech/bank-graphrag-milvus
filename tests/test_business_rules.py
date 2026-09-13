from day3536_homework.business_rules import eligible_products, milvus_filter
from day3536_homework.sample_data import CUSTOMERS, PRODUCTS


def test_customer_c001_gets_only_suitable_products() -> None:
    assert [item.product_id for item in eligible_products(CUSTOMERS[0], PRODUCTS)] == [
        "P001",
        "P002",
        "P005",
    ]


def test_amount_and_risk_are_both_required() -> None:
    customer = CUSTOMERS[3]
    assert [item.product_id for item in eligible_products(customer, PRODUCTS)] == ["P002", "P005"]


def test_milvus_filter_contains_all_hard_rules() -> None:
    assert milvus_filter(CUSTOMERS[0]) == (
        "active == true and risk_score <= 2 and min_investment <= 5000.0"
    )
