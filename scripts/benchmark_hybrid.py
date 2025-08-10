#!/usr/bin/env python3
"""
Benchmark hybrid retrieval strategies (vector, BM25, hybrid fusion) on Atlas.

- Assumes indexes created by scripts/create_indexes.py
- Uses OpenAI embeddings to vectorize the query
- Evaluates latency and result quality (simple heuristics + optional gold labels)

Environment:
- OPENAI_API_KEY
- MONGODB_URI (direct connection string)
- DB_NAME (default: ecom_data)
- COLLECTION_NAME (default: products)

Usage:
  python scripts/benchmark_hybrid.py --query "iphone 13 128gb" --k 10 --runs 5

If you have a labeled gold set, provide a JSONL with fields:
  {"query": "...", "relevant_ids": ["...", "..."], "k": 10}
Then run:
  python scripts/benchmark_hybrid.py --gold gold.jsonl --runs 3
"""

from __future__ import annotations
import os
import json
import time
import argparse
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv
from pymongo import MongoClient
from openai import OpenAI

load_dotenv()

VECTOR_INDEX_NAME = "openai_embedding_vector_index"
TEXT_INDEX_NAME = "hybrid_text_index"


def embed_query(client: OpenAI, text: str, model: str = "text-embedding-3-small") -> List[float]:
    resp = client.embeddings.create(model=model, input=text, encoding_format="float")
    return resp.data[0].embedding


def run_vector_search(coll, qvec: List[float], k: int) -> Tuple[List[Dict[str, Any]], float]:
    start = time.perf_counter()
    pipeline = [
        {
            "$vectorSearch": {
                "index": VECTOR_INDEX_NAME,
                "path": "openai_embedding",
                "queryVector": qvec,
                "numCandidates": max(200, k * 10),
                "limit": k,
            }
        },
        {"$project": {"score": {"$meta": "vectorSearchScore"}, "openai_embedding": 0}},
    ]
    docs = list(coll.aggregate(pipeline))
    latency = (time.perf_counter() - start) * 1000
    return docs, latency


def run_bm25_search(coll, text: str, k: int) -> Tuple[List[Dict[str, Any]], float]:
    start = time.perf_counter()
    pipeline = [
        {
            "$search": {
                "index": TEXT_INDEX_NAME,
                "compound": {
                    "should": [
                        {"text": {"query": text, "path": "title", "score": {"boost": {"value": 3}}}},
                        {"text": {"query": text, "path": "brand", "score": {"boost": {"value": 2}}}},
                        {"text": {"query": text, "path": "openai_embedding_text"}},
                    ]
                },
            }
        },
        {"$limit": k},
        {"$project": {"score": {"$meta": "searchScore"}}},
    ]
    docs = list(coll.aggregate(pipeline))
    latency = (time.perf_counter() - start) * 1000
    return docs, latency


def normalize_scores(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    if not items:
        return items
    scores = [x.get("score", 0.0) for x in items]
    mx = max(scores) or 1.0
    for x in items:
        x["score_norm"] = x.get("score", 0.0) / mx
    return items


def fuse_results(vector_items: List[Dict[str, Any]], text_items: List[Dict[str, Any]], k: int, w_vector: float = 0.6, w_text: float = 0.4) -> List[Dict[str, Any]]:
    vmap = {str(x.get("_id")): x for x in normalize_scores(vector_items)}
    tmap = {str(x.get("_id")): x for x in normalize_scores(text_items)}
    all_ids = set(vmap) | set(tmap)
    fused = []
    for _id in all_ids:
        v = vmap.get(_id, {})
        t = tmap.get(_id, {})
        score = w_vector * v.get("score_norm", 0.0) + w_text * t.get("score_norm", 0.0)
        doc = v or t
        fused.append({**doc, "_id": _id, "score_fused": score})
    fused.sort(key=lambda x: x["score_fused"], reverse=True)
    return fused[:k]


def simple_quality_heuristic(query: str, docs: List[Dict[str, Any]]) -> float:
    """Very simple heuristic: count occurrences of query terms in fields."""
    qterms = [t for t in query.lower().split() if len(t) > 2]
    score = 0
    for d in docs:
        text = " ".join([str(d.get("title", "")), str(d.get("brand", "")), str(d.get("openai_embedding_text", ""))]).lower()
        score += sum(text.count(t) for t in qterms)
    return float(score)


def evaluate_query(coll, client: OpenAI, query: str, k: int) -> Dict[str, Any]:
    qvec = embed_query(client, query)

    v_docs, v_ms = run_vector_search(coll, qvec, k)
    t_docs, t_ms = run_bm25_search(coll, query, k)

    fused = fuse_results(v_docs, t_docs, k)

    return {
        "query": query,
        "latency_ms": {
            "vector": round(v_ms, 2),
            "bm25": round(t_ms, 2),
            "fused": round(max(v_ms, t_ms), 2),
        },
        "quality": {
            "vector": simple_quality_heuristic(query, v_docs),
            "bm25": simple_quality_heuristic(query, t_docs),
            "fused": simple_quality_heuristic(query, fused),
        },
        "results": {
            "vector": [str(d.get("_id")) for d in v_docs],
            "bm25": [str(d.get("_id")) for d in t_docs],
            "fused": [str(d.get("_id")) for d in fused],
        },
    }


def main():
    parser = argparse.ArgumentParser(description="Benchmark hybrid retrieval on Atlas")
    parser.add_argument("--query", type=str, help="Ad-hoc query to run")
    parser.add_argument("--gold", type=str, help="Path to gold JSONL file")
    parser.add_argument("--k", type=int, default=10, help="Top-K results")
    parser.add_argument("--runs", type=int, default=3, help="Repeat runs for averaging")
    parser.add_argument("--model", type=str, default="text-embedding-3-small", help="Embedding model")
    args = parser.parse_args()

    uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017/")
    db = os.environ.get("DB_NAME", "ecom_data")
    coll_name = os.environ.get("COLLECTION_NAME", "products")

    client = MongoClient(uri)
    coll = client[db][coll_name]

    oai = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

    if args.gold:
        # Evaluate on a labeled gold set
        totals = {"vector": [], "bm25": [], "fused": []}
        with open(args.gold, "r", encoding="utf-8") as f:
            for line in f:
                row = json.loads(line)
                q = row["query"]
                k = row.get("k", args.k)
                rel = set(str(x) for x in row.get("relevant_ids", []))

                agg = {"vector": [], "bm25": [], "fused": []}
                for _ in range(args.runs):
                    out = evaluate_query(coll, oai, q, k)
                    for m in ["vector", "bm25", "fused"]:
                        agg[m].append(out["quality"][m])

                for m in agg:
                    avg_q = sum(agg[m]) / len(agg[m]) if agg[m] else 0
                    totals[m].append(avg_q)
                print(json.dumps({"query": q, "avg_quality": {m: sum(totals[m])/len(totals[m]) for m in totals}}, ensure_ascii=False))
        print("Final averages:")
        print(json.dumps({m: sum(totals[m])/len(totals[m]) if totals[m] else 0 for m in totals}, indent=2))
    elif args.query:
        # Ad-hoc evaluation
        lat_agg = {"vector": [], "bm25": [], "fused": []}
        qual_agg = {"vector": [], "bm25": [], "fused": []}
        for _ in range(args.runs):
            out = evaluate_query(coll, oai, args.query, args.k)
            for m in ["vector", "bm25", "fused"]:
                lat_agg[m].append(out["latency_ms"][m])
                qual_agg[m].append(out["quality"][m])
        print(json.dumps({
            "query": args.query,
            "avg_latency_ms": {m: round(sum(lat_agg[m])/len(lat_agg[m]), 2) for m in lat_agg},
            "avg_quality": {m: round(sum(qual_agg[m])/len(qual_agg[m]), 3) for m in qual_agg},
        }, indent=2))
    else:
        print("Provide --query or --gold")


if __name__ == "__main__":
    main()
