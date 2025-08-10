#!/usr/bin/env python3
"""
Test the migration on a small sample of documents first.
"""

import asyncio
import os
import sys
from typing import Any, Dict

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import UpdateOne

# Add project root to path so we can import our domain services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.embeddings.services import build_embedding_text

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "ecom_search")
COLL_NAME = os.getenv("COLLECTION_NAME", "products")

async def test_sample_migration():
    """Test migration on just a few documents."""
    assert MONGODB_URI, "MONGODB_URI missing from environment"
    
    client = AsyncIOMotorClient(MONGODB_URI)
    coll = client[DB_NAME][COLL_NAME]
    
    print("Testing migration on 5 sample documents...")
    
    # Get 5 sample documents
    sample_docs = await coll.find({}).limit(5).to_list(5)
    
    for doc in sample_docs:
        current_text = doc.get("openai_embedding_text")
        new_text = build_embedding_text(doc)
        
        print(f"\nDocument ID: {doc['_id']}")
        print(f"Title: {doc.get('title', 'No title')[:50]}...")
        print(f"Current embedding text: {current_text[:100] if current_text else 'None'}...")
        print(f"New embedding text: {new_text[:100]}...")
        print(f"Needs update: {new_text != current_text}")
        
        if new_text and new_text != current_text:
            # Update just this one document
            result = await coll.update_one(
                {"_id": doc["_id"]},
                {"$set": {"openai_embedding_text": new_text}}
            )
            print(f"Updated: {result.modified_count} document")
    
    client.close()
    print("\nSample test completed!")

if __name__ == "__main__":
    asyncio.run(test_sample_migration())
