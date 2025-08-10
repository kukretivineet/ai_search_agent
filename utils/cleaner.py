import os
import asyncio
from typing import Dict, Any
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

FIELDS_TO_REMOVE: Dict[str, Any] = {
    "embedding": "",
    "openai_embedding": "",
    "openai_embedding_text": "",
    "openai_embedding_updated_at": "",
}

async def main() -> None:
    """Remove specified embedding fields from all documents in products collection."""
    load_dotenv()

    mongo_uri = (
        os.getenv("MONGODB_URI")

        or "mongodb://localhost:27017/"
    )
    db_name = os.getenv("DB_NAME", "econ_data")
    collection_name = os.getenv("COLLECTION_NAME", "products")

    print(f"Connecting to MongoDB: {mongo_uri}")
    print(f"Database: {db_name}, Collection: {collection_name}")

    client = AsyncIOMotorClient(mongo_uri)
    db = client[db_name]
    coll = db[collection_name]

    # First, check total document count
    total_docs = await coll.count_documents({})
    print(f"Total documents in collection: {total_docs}")

    if total_docs == 0:
        print("No documents found in collection!")
        return

    # Count docs that currently have any of the fields
    exists_filter = {
        "$or": [{k: {"$exists": True}} for k in FIELDS_TO_REMOVE.keys()]
    }
    to_fix = await coll.count_documents(exists_filter)

    print(f"Documents with embedding fields before cleanup: {to_fix}")

    # Show sample document structure
    sample_doc = await coll.find_one({})
    if sample_doc:
        print(f"Sample document keys: {list(sample_doc.keys())}")

    if to_fix > 0:
        result = await coll.update_many({}, {"$unset": FIELDS_TO_REMOVE})
        print(f"Cleanup result - Matched: {result.matched_count}, Modified: {result.modified_count}")
    else:
        print("No documents found with the target embedding fields.")

    client.close()

if __name__ == "__main__":
    asyncio.run(main())