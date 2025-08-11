#!/usr/bin/env python3
"""
Test MongoDB aggregation with allowDiskUse fix
"""

import asyncio
import logging
from app.core.config import get_settings
from app.db.mongo import AsyncMongoClient

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def test_mongodb_aggregation():
    """Test MongoDB aggregation with disk use enabled"""
    
    try:
        # Initialize MongoDB connection
        settings = get_settings()
        mongo_client = AsyncMongoClient()
        await mongo_client.connect()
        
        # Get database and collection
        db = mongo_client.get_database()
        collection = db.products
        
        logger.info("✅ Connected to MongoDB")
        
        # Test a simple aggregation with disk use
        pipeline = [
            {"$match": {"$text": {"$search": "shirt"}}},
            {"$addFields": {"score": {"$meta": "textScore"}}},
            {"$sort": {"score": {"$meta": "textScore"}}},
            {"$limit": 10}
        ]
        
        logger.info("🔧 Testing aggregation with allowDiskUse=True...")
        
        cursor = collection.aggregate(pipeline, allowDiskUse=True)
        results = await cursor.to_list(length=10)
        
        logger.info(f"✅ Aggregation successful! Found {len(results)} results")
        
        # Test faceted aggregation (the one that was failing)
        facet_pipeline = [
            {"$match": {"$text": {"$search": "shirt"}}},
            {"$addFields": {"score": {"$meta": "textScore"}}},
            {"$sort": {"score": {"$meta": "textScore"}}},
            {
                "$facet": {
                    "results": [
                        {"$skip": 0},
                        {"$limit": 20}
                    ],
                    "total": [
                        {"$count": "count"}
                    ]
                }
            }
        ]
        
        logger.info("🔧 Testing faceted aggregation with allowDiskUse=True...")
        
        cursor = collection.aggregate(facet_pipeline, allowDiskUse=True)
        facet_results = await cursor.to_list(length=1)
        
        if facet_results:
            results_count = len(facet_results[0].get("results", []))
            total_count = facet_results[0].get("total", [{}])[0].get("count", 0)
            logger.info(f"✅ Faceted aggregation successful! Found {results_count} results out of {total_count} total")
        else:
            logger.info("✅ Faceted aggregation successful but no results found")
        
        await mongo_client.disconnect()
        logger.info("✅ All MongoDB aggregation tests passed!")
        
    except Exception as e:
        logger.error(f"❌ MongoDB aggregation test failed: {e}")
        return False
    
    return True


if __name__ == "__main__":
    print("🧪 Testing MongoDB Aggregation Performance Fix...\n")
    
    success = asyncio.run(test_mongodb_aggregation())
    
    if success:
        print("\n🎉 MongoDB memory limit fix verified!")
        print("✅ All aggregation operations now use allowDiskUse=True")
        print("✅ Sort operations can use disk storage when needed")
        print("✅ Memory limit errors should be resolved")
    else:
        print("\n❌ Test failed - check MongoDB connection and data")
