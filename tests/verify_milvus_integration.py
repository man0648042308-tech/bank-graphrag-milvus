"""Explicit live Milvus 2.6 dense + BM25 integration check."""

from day3536_homework.infrastructure.milvus_adapter import (
    DEFAULT_COLLECTION,
    MilvusHybridAdapter,
)
from day3536_homework.sample_data import CUSTOMERS, PRODUCTS


def main() -> None:
    with MilvusHybridAdapter("http://127.0.0.1:19531") as milvus:
        milvus.recreate()
        inserted = milvus.insert_products(PRODUCTS)
        hits = milvus.hybrid_search(
            CUSTOMERS[0],
            "稳健、低风险并且可以灵活使用",
            limit=5,
        )
        collections = milvus.client.list_collections()

    ids = [hit.product_id for hit in hits]
    assert inserted == 5
    assert DEFAULT_COLLECTION in collections
    assert "P003" not in ids
    assert "P004" not in ids
    assert {"P001", "P005"}.issubset(ids)
    print("MILVUS_INTEGRATION_PASS")
    print(f"collection={DEFAULT_COLLECTION}")
    print(f"inserted={inserted}")
    print(f"safe_result_ids={ids}")


if __name__ == "__main__":
    main()
