#!/usr/bin/env python3
"""
Create MongoDB Atlas Vector Search and Text Search indexes for hybrid retrieval.

This script uses the Atlas Admin API to create/update:
- Vector Search index on `openai_embedding` (1536 dims, cosine)
- Text Search index on `title`, `brand`, `openai_embedding_text` (BM25)
- (Optional) B-tree indexes via PyMongo for metadata fields

Environment variables (load from .env if present):
- ATLAS_GROUP_ID
- ATLAS_CLUSTER_NAME
- ATLAS_PUBLIC_KEY
- ATLAS_PRIVATE_KEY
- DB_NAME (default: ecom_data)
- COLLECTION_NAME (default: products)
- MONGODB_URI (optional, for B-tree indexes)

Usage:
  python scripts/create_indexes.py --create-btree
"""

from __future__ import annotations
import os
import sys
import json
import time
import argparse
from typing import Any, Dict, Optional

import requests
from requests.auth import HTTPDigestAuth
from dotenv import load_dotenv

try:
    from pymongo import MongoClient
    HAVE_PYMONGO = True
except Exception:
    HAVE_PYMONGO = False


VECTOR_INDEX_NAME = "openai_embedding_vector_index"
TEXT_INDEX_NAME = "hybrid_text_index"

ATLAS_BASE = "https://cloud.mongodb.com/api/atlas/v2"


def get_env() -> Dict[str, str]:
    """Load and validate required environment variables."""
    load_dotenv()
    env = {
        "group_id": os.environ.get("ATLAS_GROUP_ID", "").strip(),
        "cluster_name": os.environ.get("ATLAS_CLUSTER_NAME", "").strip(),
        "public_key": os.environ.get("ATLAS_PUBLIC_KEY", "").strip(),
        "private_key": os.environ.get("ATLAS_PRIVATE_KEY", "").strip(),
        "db": os.environ.get("DB_NAME", "ecom_data").strip(),
        "coll": os.environ.get("COLLECTION_NAME", "products").strip(),
        "mongodb_uri": os.environ.get("MONGODB_URI", "").strip(),
    }
    missing = [k for k, v in env.items() if k in {"group_id","cluster_name","public_key","private_key"} and not v]
    if missing:
        raise SystemExit(f"Missing required env vars: {', '.join(missing)}")
    return env


def atlas_request(method: str, url: str, auth: HTTPDigestAuth, payload: Optional[Dict[str, Any]] = None):
    headers = {"Content-Type": "application/json"}
    resp = requests.request(method, url, auth=auth, headers=headers, json=payload)
    if resp.status_code >= 400:
        raise RuntimeError(f"Atlas API error {resp.status_code}: {resp.text}")
    return resp.json() if resp.text else {}


def list_search_indexes(env: Dict[str, str], auth: HTTPDigestAuth):
    url = f"{ATLAS_BASE}/groups/{env['group_id']}/clusters/{env['cluster_name']}/fts/indexes/{env['db']}/{env['coll']}"
    try:
        return atlas_request("GET", url, auth)
    except RuntimeError as e:
        # If none exist, API might return 404
        if "404" in str(e):
            return []
        raise


def create_or_update_vector_index(env: Dict[str, str], auth: HTTPDigestAuth, num_dimensions: int = 1536):
    """Create or update the Vector Search index."""
    existing = list_search_indexes(env, auth)
    has_vector = any(idx.get("name") == VECTOR_INDEX_NAME for idx in existing)

    definition = {
        "name": VECTOR_INDEX_NAME,
        "type": "vectorSearch",
        "definition": {
            "fields": [
                {
                    "type": "vector",
                    "path": "openai_embedding",
                    "numDimensions": num_dimensions,
                    "similarity": "cosine"
                }
            ]
        }
    }

    base = f"{ATLAS_BASE}/groups/{env['group_id']}/clusters/{env['cluster_name']}/fts/indexes/{env['db']}/{env['coll']}"

    if not has_vector:
        print(f"Creating Vector Search index '{VECTOR_INDEX_NAME}'...")
        atlas_request("POST", base, auth, payload=definition)
    else:
        print(f"Updating Vector Search index '{VECTOR_INDEX_NAME}'...")
        url = f"{base}/{VECTOR_INDEX_NAME}"
        # PATCH is supported for search indexes updates
        atlas_request("PATCH", url, auth, payload=definition)

    print("Vector index ready (propagation may take up to a minute).")


def create_or_update_text_index(env: Dict[str, str], auth: HTTPDigestAuth):
    """Create or update the Text Search (BM25) index."""
    existing = list_search_indexes(env, auth)
    has_text = any(idx.get("name") == TEXT_INDEX_NAME for idx in existing)

    definition = {
        "name": TEXT_INDEX_NAME,
        "type": "search",
        "definition": {
            "mappings": {
                "dynamic": False,
                "fields": {
                    "title": {"type": "string"},
                    "brand": {"type": "string"},
                    "openai_embedding_text": {"type": "string"}
                }
            }
        }
    }

    base = f"{ATLAS_BASE}/groups/{env['group_id']}/clusters/{env['cluster_name']}/fts/indexes/{env['db']}/{env['coll']}"

    if not has_text:
        print(f"Creating Text Search index '{TEXT_INDEX_NAME}'...")
        atlas_request("POST", base, auth, payload=definition)
    else:
        print(f"Updating Text Search index '{TEXT_INDEX_NAME}'...")
        url = f"{base}/{TEXT_INDEX_NAME}"
        atlas_request("PATCH", url, auth, payload=definition)

    print("Text index ready (propagation may take up to a minute).")


def create_btree_indexes(env: Dict[str, str]):
    """Create supportive B-tree indexes using PyMongo (optional)."""
    if not HAVE_PYMONGO:
        print("PyMongo not installed. Skipping B-tree index creation.")
        return

    if not env["mongodb_uri"]:
        print("MONGODB_URI not provided. Skipping B-tree index creation.")
        return

    client = MongoClient(env["mongodb_uri"])
    coll = client[env["db"]][env["coll"]]

    print("Creating B-tree indexes...")
    coll.create_index([("embedding_model", 1), ("embedding_updated_at", -1)], name="model_updatedAt_idx")
    coll.create_index([("openai_embedding_text", 1)], name="embedding_text_idx")
    print("B-tree indexes created.")


def main():
    parser = argparse.ArgumentParser(description="Create Atlas Vector & Text Search indexes")
    parser.add_argument("--no-vector", action="store_true", help="Skip creating vector index")
    parser.add_argument("--no-text", action="store_true", help="Skip creating text index")
    parser.add_argument("--create-btree", action="store_true", help="Also create B-tree indexes via PyMongo")
    parser.add_argument("--dims", type=int, default=1536, help="Vector dimensions (default 1536)")
    args = parser.parse_args()

    env = get_env()
    auth = HTTPDigestAuth(env["public_key"], env["private_key"])

    if not args.no_vector:
        create_or_update_vector_index(env, auth, num_dimensions=args.dims)
    if not args.no_text:
        create_or_update_text_index(env, auth)
    if args.create_btree:
        create_btree_indexes(env)

    print("Done. Note: index build/updates propagate asynchronously in Atlas.")


if __name__ == "__main__":
    main()
