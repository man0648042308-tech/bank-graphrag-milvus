"""Non-negotiable financial suitability filters."""

from collections.abc import Iterable

from .models import Customer, Product


def is_eligible(customer: Customer, product: Product) -> bool:
    return (
        product.active
        and product.risk_score <= customer.risk_score
        and product.min_investment <= customer.available_amount
    )


def eligible_products(customer: Customer, products: Iterable[Product]) -> list[Product]:
    return [product for product in products if is_eligible(customer, product)]


def milvus_filter(customer: Customer) -> str:
    return (
        f"active == true and risk_score <= {customer.risk_score} "
        f"and min_investment <= {float(customer.available_amount)}"
    )
