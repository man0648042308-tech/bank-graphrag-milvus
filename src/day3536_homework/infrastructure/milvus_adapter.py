"""Milvus 2.6 dense + BM25 hybrid search adapter.

All destructive collection operations are protected by the ``day3536_`` prefix.
"""

from pymilvus import (
    AnnSearchRequest,
    DataType,
    Function,
    FunctionType,
    MilvusClient,
    RRFRanker,
)

from ..business_rules import milvus_filter
from ..embeddings import build_product_vector, build_query_vector
from ..models import Customer, Product, RetrievalHit

SAFE_PREFIX = "day3536_"
DEFAULT_COLLECTION = "day3536_bank_products_hybrid"


class MilvusHybridAdapter:
    def __init__(
        self,
        uri: str,
        token: str | None = None,
        collection_name: str = DEFAULT_COLLECTION,
    ) -> None:
        if not collection_name.startswith(SAFE_PREFIX):
            raise ValueError(f"Collection必须以{SAFE_PREFIX}开头")
        kwargs = {"uri": uri}
        if token:
            kwargs["token"] = token
        self.client = MilvusClient(**kwargs)
        self.collection_name = collection_name

    def recreate(self) -> None:
        if self.client.has_collection(self.collection_name):
            self.client.drop_collection(self.collection_name)

        schema = MilvusClient.create_schema(auto_id=False, enable_dynamic_field=False)
        schema.add_field("product_id", DataType.VARCHAR, is_primary=True, max_length=32)
        schema.add_field("name", DataType.VARCHAR, max_length=100)
        schema.add_field(
            "description",
            DataType.VARCHAR,
            max_length=1000,
            enable_analyzer=True,
            analyzer_params={"type": "standard"},
        )
        schema.add_field("dense_vector", DataType.FLOAT_VECTOR, dim=4)
        schema.add_field("sparse_vector", DataType.SPARSE_FLOAT_VECTOR)
        schema.add_field("risk_score", DataType.INT64)
        schema.add_field("min_investment", DataType.DOUBLE)
        schema.add_field("active", DataType.BOOL)
        schema.add_function(
            Function(
                name="description_bm25",
                function_type=FunctionType.BM25,
                input_field_names=["description"],
                output_field_names=["sparse_vector"],
            )
        )

        indexes = MilvusClient.prepare_index_params()
        indexes.add_index("dense_vector", index_type="AUTOINDEX", metric_type="COSINE")
        indexes.add_index(
            "sparse_vector",
            index_type="SPARSE_INVERTED_INDEX",
            metric_type="BM25",
            params={"inverted_index_algo": "DAAT_MAXSCORE"},
        )
        self.client.create_collection(
            collection_name=self.collection_name,
            schema=schema,
            index_params=indexes,
        )

    def insert_products(self, products: tuple[Product, ...]) -> int:
        rows = [
            {
                "product_id": product.product_id,
                "name": product.name,
                "description": product.description,
                "dense_vector": build_product_vector(product.description),
                "risk_score": product.risk_score,
                "min_investment": product.min_investment,
                "active": product.active,
            }
            for product in products
        ]
        result = self.client.insert(self.collection_name, rows)
        # Milvus 默认可能采用最终一致性；显式 flush 让紧随其后的教学验收可重复。
        self.client.flush(self.collection_name)
        return int(result["insert_count"])

    def hybrid_search(self, customer: Customer, query: str, limit: int = 5) -> list[RetrievalHit]:
        filter_expression = milvus_filter(customer)
        dense = AnnSearchRequest(
            data=[build_query_vector(query)],
            anns_field="dense_vector",
            param={"metric_type": "COSINE", "params": {}},
            limit=max(limit, 10),
            expr=filter_expression,
        )
        sparse = AnnSearchRequest(
            data=[query],
            anns_field="sparse_vector",
            param={"metric_type": "BM25", "params": {}},
            limit=max(limit, 10),
            expr=filter_expression,
        )
        results = self.client.hybrid_search(
            collection_name=self.collection_name,
            reqs=[dense, sparse],
            ranker=RRFRanker(60),
            limit=limit,
            output_fields=["product_id", "name"],
        )
        return [
            RetrievalHit(
                product_id=str(hit["entity"]["product_id"]),
                name=str(hit["entity"]["name"]),
                score=float(hit["distance"]),
                sources={"milvus_dense", "milvus_bm25"},
            )
            for hit in results[0]
        ]

    def close(self) -> None:
        self.client.close()

    def __enter__(self) -> "MilvusHybridAdapter":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
