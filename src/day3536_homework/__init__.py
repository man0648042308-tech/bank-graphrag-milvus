"""Day35/Day36 banking GraphRAG homework package."""

from .business_rules import eligible_products
from .embeddings import build_query_vector

__all__ = ["build_query_vector", "eligible_products"]


