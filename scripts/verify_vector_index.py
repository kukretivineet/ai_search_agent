#!/usr/bin/env python3
"""
Smoke test to verify vector search is working properly.
"""

import asyncio
import os
from typing import List

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from openai import OpenAI

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "ecom_search")
COLL_NAME = os.getenv("COLLECTION_NAME", "products")
INDEX_NAME = os.getenv("VECTOR_INDEX_NAME", "vector_index")
EMBED_FIELD = os.getenv("EMBED_FIELD", "openai_embedding")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")

def _assert_env():
    assert MONGODB_URI, "MONGODB_URI missing"
    assert OPENAI_API_KEY, "OPENAI_API_KEY missing"

async def _embed_query(q: str) -> List[float]:
    client = OpenAI(api_key=OPENAI_API_KEY)
    resp = client.embeddings.create(model=EMBED_MODEL, input=q)
    return resp.data[0].embedding  # 1536-d

async def main():
    _assert_env()
    mongo = AsyncIOMotorClient(MONGODB_URI)
    coll = mongo[DB_NAME][COLL_NAME]

    # Basic shape check on a sample document
    sample = await coll.find_one({EMBED_FIELD: {"$type": "array"}}, {EMBED_FIELD: {"$slice": 3}, "title": 1})
    assert sample, "No document contains an embedding array"
    print(f"Sample doc title: {sample.get('title', '')}")
    print(f"Embedding first 3 values: {sample[EMBED_FIELD][:3]}")

    # Quick cardinality/dimension check
    dims = await coll.aggregate([
        {"$match": {EMBED_FIELD: {"$type": "array"}}},
        {"$project": {"len": {"$size": f"${EMBED_FIELD}"}}},
        {"$group": {"_id": "$len", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
    ]).to_list(5)
    print("Embedding length histogram:", dims)
    assert dims and dims[0]["_id"] == 1536, "Embeddings must be 1536-d"

    # Smoke vector search
    qvec = await _embed_query("men blue cotton track pants")
    pipeline = [
        {"$vectorSearch": {
            "index": INDEX_NAME,
            "path": EMBED_FIELD,
            "queryVector": qvec,
            "numCandidates": 200,
            "limit": 5
        }},
        {"$project": {
            "_id": 0,
            "title": 1,
            "score": {"$meta": "vectorSearchScore"}
        }}
    ]
    results = await coll.aggregate(pipeline).to_list(5)
    print("Top results:")
    for r in results:
        print(f"- {r.get('title')} (score={r.get('score'):.4f})")

    mongo.close()

if __name__ == "__main__":
    asyncio.run(main())
