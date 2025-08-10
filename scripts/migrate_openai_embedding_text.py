#!/usr/bin/env python3
"""
Idempotent migration script to update openai_embedding_text field.
Only updates documents where the generated text has changed.
"""

import asyncio
import os
import sys
from typing import Any, Dict

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

# Add project root to path so we can import our domain services
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.embeddings.services import build_embedding_text

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("DB_NAME", "ecom_search")
COLL_NAME = os.getenv("COLLECTION_NAME", "products")

async def process_batch(coll, query: Dict[str, Any], batch_size: int = 500):
    """
    Compute and upsert openai_embedding_text when it changed.
    
    Args:
        coll: MongoDB collection
        query: Query filter for documents to process
        batch_size: Number of documents to process in each batch
    """
    projection = {
        "openai_embedding_text": 1, 
        "title": 1, 
        "brand": 1, 
        "category": 1, 
        "sub_category": 1, 
        "description": 1, 
        "product_details": 1, 
        "selling_price_numeric": 1, 
        "price_inr": 1, 
        "actual_price_numeric": 1
    }
    
    cursor = coll.find(query, projection=projection).batch_size(batch_size)
    ops = []
    processed_count = 0
    updated_count = 0
    
    async for doc in cursor:
        processed_count += 1
        
        try:
            new_text = build_embedding_text(doc)
            current_text = doc.get("openai_embedding_text")
            
            if new_text and new_text != current_text:
                from pymongo import UpdateOne
                ops.append(UpdateOne(
                    {"_id": doc["_id"]},
                    {"$set": {"openai_embedding_text": new_text}},
                    upsert=False
                ))
                updated_count += 1
            
            # Process batch when it's full
            if len(ops) >= batch_size:
                if ops:
                    await coll.bulk_write(ops, ordered=False)
                    print(f"Processed {processed_count} docs, updated {updated_count} so far...")
                ops.clear()
                
        except Exception as e:
            print(f"Error processing document {doc.get('_id')}: {e}")
            continue
    
    # Process remaining operations
    if ops:
        await coll.bulk_write(ops, ordered=False)
    
    print(f"Migration complete: processed {processed_count} docs, updated {updated_count} docs")
    return {"processed": processed_count, "updated": updated_count}

async def main():
    """Main migration function."""
    assert MONGODB_URI, "MONGODB_URI missing from environment"
    
    print(f"Starting migration to update openai_embedding_text...")
    print(f"Database: {DB_NAME}")
    print(f"Collection: {COLL_NAME}")
    
    client = AsyncIOMotorClient(MONGODB_URI)
    coll = client[DB_NAME][COLL_NAME]
    
    # Check collection exists and get count
    total_docs = await coll.count_documents({})
    print(f"Total documents in collection: {total_docs:,}")
    
    if total_docs == 0:
        print("No documents found. Exiting.")
        client.close()
        return
    
    # Process all documents
    result = await process_batch(coll, {})
    
    client.close()
    
    print("\nMigration Summary:")
    print(f"- Documents processed: {result['processed']:,}")
    print(f"- Documents updated: {result['updated']:,}")
    print(f"- Documents unchanged: {result['processed'] - result['updated']:,}")
    
    return result

if __name__ == "__main__":
    asyncio.run(main())
