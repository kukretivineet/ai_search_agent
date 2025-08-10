#!/usr/bin/env python3
"""
Monitor the embedding pipeline progress
"""

import os
import time
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_pipeline_progress():
    """Get current pipeline progress."""
    
    # Connect to MongoDB
    connection_string = (
        os.environ.get("MONGODB_URI") or 
        os.environ.get("MONGODB_ATLAS_URI") or 
        "mongodb://localhost:27017/"
    )
    
    client = MongoClient(connection_string)
    db_name = os.environ.get("DB_NAME", "ecom_data")
    collection_name = os.environ.get("COLLECTION_NAME", "products")
    
    collection = client[db_name][collection_name]
    
    # Get stats
    total_docs = collection.count_documents({})
    
    with_embedding_text = collection.count_documents({
        "openai_embedding_text": {"$exists": True, "$ne": ""}
    })
    
    with_embeddings = collection.count_documents({
        "openai_embedding": {"$exists": True, "$ne": []}
    })
    
    complete_records = collection.count_documents({
        "openai_embedding_text": {"$exists": True, "$ne": ""},
        "openai_embedding": {"$exists": True, "$ne": []}
    })
    
    client.close()
    
    return {
        "total_documents": total_docs,
        "with_embedding_text": with_embedding_text,
        "with_embeddings": with_embeddings,
        "complete_records": complete_records,
        "completion_percentage": (complete_records / total_docs) * 100 if total_docs > 0 else 0
    }

def main():
    """Monitor progress continuously."""
    
    print("🔍 MongoDB Embedding Pipeline Monitor")
    print("="*50)
    
    start_time = time.time()
    last_count = 0
    
    try:
        while True:
            stats = get_pipeline_progress()
            current_time = time.time()
            elapsed = current_time - start_time
            
            # Calculate rate
            current_count = stats["complete_records"]
            rate = (current_count - last_count) / 60 if elapsed >= 60 else 0  # per minute
            
            print(f"\n📊 Progress Update ({time.strftime('%H:%M:%S')})")
            print(f"   Total documents: {stats['total_documents']:,}")
            print(f"   Complete records: {stats['complete_records']:,}")
            print(f"   Completion: {stats['completion_percentage']:.2f}%")
            print(f"   With embedding text: {stats['with_embedding_text']:,}")
            print(f"   With embeddings: {stats['with_embeddings']:,}")
            
            if elapsed >= 60:
                print(f"   Processing rate: {rate:.1f} docs/minute")
                eta_minutes = (stats['total_documents'] - current_count) / rate if rate > 0 else 0
                if eta_minutes > 0:
                    print(f"   ETA: {eta_minutes/60:.1f} hours")
            
            last_count = current_count
            
            # Sleep for 1 minute
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\n👋 Monitoring stopped.")

if __name__ == "__main__":
    main()
