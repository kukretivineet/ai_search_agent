#!/usr/bin/env python3
"""
Usage example for MongoDB schema extraction script.

This script demonstrates how to use the schema extractor with different configurations.
"""

import asyncio
import os
from extract_pepagora_schema import MongoSchemaExtractor, SchemaExtractorSettings


async def extract_with_custom_settings():
    """Extract schema with custom settings."""
    
    # Custom settings for different use cases
    settings = SchemaExtractorSettings(
        mongodb_uri="mongodb://localhost:27017/",  # Local MongoDB
        pepagora_db_name="pepagora_dev",
        sample_size=50,  # Smaller sample for faster extraction
        output_file="pepagora_dev_small_sample.md"
    )
    
    extractor = MongoSchemaExtractor(settings)
    await extractor.run()


async def extract_specific_collections():
    """Extract schema for only specific collections (modification needed)."""
    
    # Note: This would require modifying the extractor to accept a collection filter
    # For now, this is just a demonstration of how it could be done
    
    settings = SchemaExtractorSettings(
        mongodb_uri="mongodb://localhost:27017/",
        pepagora_db_name="pepagora_dev",
        sample_size=20,
        output_file="pepagora_dev_specific.md"
    )
    
    # This would need to be implemented in the main extractor class
    # extractor = MongoSchemaExtractor(settings)
    # extractor.set_collection_filter(['users', 'products', 'orders'])
    # await extractor.run()
    
    print("Specific collection extraction not implemented yet.")


async def extract_with_atlas_connection():
    """Extract schema from MongoDB Atlas."""
    
    # Use Atlas connection string from environment
    atlas_uri = os.getenv("MONGODB_ATLAS_URI")
    
    if not atlas_uri:
        print("MONGODB_ATLAS_URI not set in environment variables")
        return
    
    settings = SchemaExtractorSettings(
        mongodb_uri=atlas_uri,
        pepagora_db_name="pepagora_dev",
        sample_size=100,
        output_file="pepagora_dev_atlas.md"
    )
    
    extractor = MongoSchemaExtractor(settings)
    await extractor.run()


async def main():
    """Main function to demonstrate different usage patterns."""
    
    print("MongoDB Schema Extractor Usage Examples")
    print("=" * 50)
    
    # Example 1: Default extraction (already done)
    print("1. Default extraction completed - see pepagora_dev.md")
    
    # Example 2: Custom sample size
    print("2. Running extraction with smaller sample size...")
    try:
        await extract_with_custom_settings()
        print("   ✓ Custom extraction completed")
    except Exception as e:
        print(f"   ✗ Custom extraction failed: {e}")
    
    # Example 3: Atlas connection (if available)
    print("3. Attempting Atlas extraction...")
    try:
        await extract_with_atlas_connection()
        print("   ✓ Atlas extraction completed")
    except Exception as e:
        print(f"   ✗ Atlas extraction failed: {e}")
    
    # Example 4: Specific collections (not implemented)
    print("4. Specific collection extraction...")
    await extract_specific_collections()
    
    print("\nExtraction examples completed!")
    print("Check the generated .md files for results.")


if __name__ == "__main__":
    asyncio.run(main())
