#!/usr/bin/env python3
"""
Simple migration script that updates documents one by one to avoid bulk operation issues.
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

async def migrate_simple():
    """Simple migration that updates documents one by one."""
    assert MONGODB_URI, "MONGODB_URI missing from environment"
    
    print(f"Starting simple migration...")
    print(f"Database: {DB_NAME}")
    print(f"Collection: {COLL_NAME}")
    
    client = AsyncIOMotorClient(MONGODB_URI)
    coll = client[DB_NAME][COLL_NAME]
    
    # Check collection exists and get count
    total_docs = await coll.count_documents({})
    print(f"Total documents in collection: {total_docs:,}")
    
    processed_count = 0
    updated_count = 0
    
    # Process documents in batches
    batch_size = 100
    skip = 0
    
    while skip < total_docs:
        print(f"\nProcessing batch {skip // batch_size + 1}: documents {skip + 1} to {min(skip + batch_size, total_docs)}")
        
        # Get batch of documents
        cursor = coll.find({}).skip(skip).limit(batch_size)
        
        async for doc in cursor:
            processed_count += 1
            
            try:
                current_text = doc.get("openai_embedding_text")
                new_text = build_embedding_text(doc)
                
                if new_text and new_text != current_text:
                    # Update this document
                    await coll.update_one(
                        {"_id": doc["_id"]},
                        {"$set": {"openai_embedding_text": new_text}}
                    )
                    updated_count += 1
                    
                if processed_count % 100 == 0:
                    print(f"  Processed {processed_count} docs, updated {updated_count}")
                    
            except Exception as e:
                print(f"  Error processing document {doc.get('_id')}: {e}")
                continue
        
        skip += batch_size
    
    client.close()
    
    print(f"\nMigration complete:")
    print(f"- Documents processed: {processed_count:,}")
    print(f"- Documents updated: {updated_count:,}")
    print(f"- Documents unchanged: {processed_count - updated_count:,}")
    
    return {"processed": processed_count, "updated": updated_count}

if __name__ == "__main__":
    asyncio.run(migrate_simple())
