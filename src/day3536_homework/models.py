"""Small, explicit data models shared by the homework modules."""

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Customer:
    customer_id: str
    name: str
    risk_score: int
    available_amount: float
    community_id: int | None = None


@dataclass(frozen=True, slots=True)
class Product:
    product_id: str
    name: str
    category: str
    description: str
    risk_score: int
    min_investment: float
    expected_return: float
    active: bool = True


@dataclass(slots=True)
class RetrievalHit:
    product_id: str
    name: str
    score: float
    sources: set[str] = field(default_factory=set)
    explanation: str = ""


@dataclass(frozen=True, slots=True)
class QueryResult:
    natural_language: str
    generated_query: str
    rows: tuple[dict[str, object], ...]

