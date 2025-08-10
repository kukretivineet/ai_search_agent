#!/usr/bin/env python3
"""
Create local MongoDB indexes for hybrid retrieval (Community/Enterprise server).

This script creates:
- Text index (MongoDB $text) on: title, brand, openai_embedding_text
- B-tree indexes for metadata: (embedding_model, embedding_updated_at), openai_embedding_text
- Optional helper indexes for common filters (category, sub_category, out_of_stock)

Note:
- Vector Search ($vectorSearch) and Atlas Search ($search) are Atlas-only features.
  On local MongoDB, use $text for BM25-like search and an external vector index (e.g., FAISS) for vectors.

Env (.env):
- MONGODB_URI (default: mongodb://localhost:27017/)
- DB_NAME (default: ecom_data)
- COLLECTION_NAME (default: products)

Usage:
  python scripts/create_local_indexes.py
"""

from __future__ import annotations
import os
from typing import Any

from dotenv import load_dotenv
from pymongo import MongoClient


def main() -> None:
    load_dotenv()
    uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
    db_name = os.environ.get("DB_NAME", "ecom_data")
    coll_name = os.environ.get("COLLECTION_NAME", "products")

    client = MongoClient(uri)
    coll = client[db_name][coll_name]

    print(f"Connecting to {uri} -> {db_name}.{coll_name}")

    # 1) Text index (weights boost title > brand > embedding_text)
    print("Creating TEXT index (MongoDB $text)...")
    coll.create_index(
        [("title", "text"), ("brand", "text"), ("openai_embedding_text", "text")],
        name="text_idx",
        default_language="english",
        weights={"title": 5, "brand": 3, "openai_embedding_text": 2},
        background=True,
    )

    # 2) B-tree indexes for metadata and filters
    print("Creating B-tree indexes (metadata/filters)...")
    coll.create_index([("embedding_model", 1), ("embedding_updated_at", -1)], name="model_updatedAt_idx", background=True)
    coll.create_index([("openai_embedding_text", 1)], name="embedding_text_idx", background=True)

    # Optional helpful indexes for faceting/filters
    coll.create_index([("category", 1), ("sub_category", 1)], name="category_sub_idx", background=True)
    coll.create_index([("out_of_stock", 1)], name="stock_idx", background=True)
    coll.create_index([("selling_price_numeric", 1)], name="price_idx", background=True)

    print("Done. You can now use $text for keyword search locally.")
    print("For vector search locally, use an external index (e.g., FAISS) and fuse results in app code.")


if __name__ == "__main__":
    main()
