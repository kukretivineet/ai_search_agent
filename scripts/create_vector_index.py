#!/usr/bin/env python3
"""
Create or update MongoDB Atlas Vector Search index (and optional text index).

Env required:
  ATLAS_GROUP_ID=        # Atlas Project ID
  ATLAS_CLUSTER_NAME=    # Atlas Cluster Name
  ATLAS_PUBLIC_KEY=      # Atlas API Public Key
  ATLAS_PRIVATE_KEY=     # Atlas API Private Key
  DB_NAME=ecom_search    # database name (defaults to ecom_data)
  COLLECTION_NAME=products
Optional:
  CREATE_TEXT_INDEX=true # also create a minimal BM25 text index
"""
from __future__ import annotations

import os
import sys
import json
import time
from typing import Dict, Any, List
import requests
from requests.auth import HTTPDigestAuth

VECTOR_INDEX_NAME = "openai_embedding_vector_index"
TEXT_INDEX_NAME = "hybrid_text_index"
ATLAS_BASE = "https://cloud.mongodb.com/api/atlas/v2"


def get_env() -> Dict[str, str]:
    env = {
        "group_id": os.getenv("ATLAS_GROUP_ID", "").strip(),
        "cluster_name": os.getenv("ATLAS_CLUSTER_NAME", "").strip(),
        "public_key": os.getenv("ATLAS_PUBLIC_KEY", "").strip(),
        "private_key": os.getenv("ATLAS_PRIVATE_KEY", "").strip(),
        "db": os.getenv("DB_NAME", "ecom_data").strip(),
        "coll": os.getenv("COLLECTION_NAME", "products").strip(),
        "create_text": os.getenv("CREATE_TEXT_INDEX", "false").strip().lower() in ("1", "true", "yes"),
    }
    missing = [k for k, v in env.items() if k in ("group_id", "cluster_name", "public_key", "private_key") and not v]
    if missing:
        print(f"Missing required env: {', '.join(missing)}", file=sys.stderr)
        sys.exit(1)
    return env


def atlas_request(method: str, url: str, auth: HTTPDigestAuth, payload: Dict[str, Any] | None = None) -> Any:
    headers = {"Content-Type": "application/json"}
    data = json.dumps(payload) if payload is not None else None
    r = requests.request(method, url, headers=headers, data=data, auth=auth, timeout=60)
    if r.status_code >= 400:
        raise RuntimeError(f"Atlas API error {r.status_code}: {r.text}")
    if r.text:
        try:
            return r.json()
        except Exception:
            return r.text
    return None


def list_search_indexes(env: Dict[str, str], auth: HTTPDigestAuth) -> List[Dict[str, Any]]:
    url = f"{ATLAS_BASE}/groups/{env['group_id']}/clusters/{env['cluster_name']}/fts/indexes/{env['db']}/{env['coll']}"
    res = atlas_request("GET", url, auth)
    return res if isinstance(res, list) else []


def ensure_vector_index(env: Dict[str, str], auth: HTTPDigestAuth) -> None:
    existing = list_search_indexes(env, auth)
    has_vector = any(ix.get("name") == VECTOR_INDEX_NAME and ix.get("type") == "vectorSearch" for ix in existing)

    definition = {
        "name": VECTOR_INDEX_NAME,
        "type": "vectorSearch",
        "definition": {
            "fields": [
                {
                    "type": "vector",
                    "path": "openai_embedding",
                    "numDimensions": 1536,
                    "similarity": "cosine"
                }
            ]
        }
    }

    base = f"{ATLAS_BASE}/groups/{env['group_id']}/clusters/{env['cluster_name']}/fts/indexes/{env['db']}/{env['coll']}"
    if not has_vector:
        print(f"Creating Vector Search index '{VECTOR_INDEX_NAME}' on {env['db']}.{env['coll']} ...")
        atlas_request("POST", base, auth, payload=definition)
    else:
        print(f"Updating Vector Search index '{VECTOR_INDEX_NAME}' ...")
        url = f"{base}/{VECTOR_INDEX_NAME}"
        atlas_request("PATCH", url, auth, payload=definition)
    print("Submitted. Propagation may take ~1–2 minutes.")


def ensure_text_index(env: Dict[str, str], auth: HTTPDigestAuth) -> None:
    existing = list_search_indexes(env, auth)
    has_text = any(ix.get("name") == TEXT_INDEX_NAME and ix.get("type") == "search" for ix in existing)

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
        print(f"Creating Text Search index '{TEXT_INDEX_NAME}' ...")
        atlas_request("POST", base, auth, payload=definition)
    else:
        print(f"Updating Text Search index '{TEXT_INDEX_NAME}' ...")
        url = f"{base}/{TEXT_INDEX_NAME}"
        atlas_request("PATCH", url, auth, payload=definition)
    print("Submitted. Propagation may take ~1–2 minutes.")


def main() -> None:
    env = get_env()
    auth = HTTPDigestAuth(env["public_key"], env["private_key"])

    ensure_vector_index(env, auth)
    if env["create_text"]:
        ensure_text_index(env, auth)

    # Optional small wait to help avoid immediate query failures after creation
    time.sleep(2)
    print("Done. Validate with an aggregate using $vectorSearch.")


if __name__ == "__main__":
    main()