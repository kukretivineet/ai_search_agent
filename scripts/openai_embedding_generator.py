#!/usr/bin/env python3
"""
OpenAI Embedding Generator for MongoDB Atlas Vector Search
Uses text-embedding-3-small for high-quality embeddings
Replaces existing embedding data with OpenAI embeddings
"""

import os
import sys
import time
import logging
from typing import List, Dict, Any, Optional
from pymongo import MongoClient
from dotenv import load_dotenv
import openai
from openai import OpenAI
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OpenAIEmbeddingGenerator:
    """Generate embeddings using OpenAI's text-embedding-3-small model"""
    
    def __init__(self):
        """Initialize the OpenAI embedding client"""
        self.model_name = "text-embedding-3-small"
        self.embedding_dimension = 1536  # text-embedding-3-small produces 1536-dim embeddings
        
        logger.info(f"🚀 Initializing OpenAI Embedding Generator...")
        logger.info(f"Model: {self.model_name}")
        logger.info(f"Expected embedding dimension: {self.embedding_dimension}")
        
        # Initialize OpenAI client
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = OpenAI(api_key=api_key)
        
        logger.info(f"✅ OpenAI Embedding Generator initialized successfully")

    def create_embedding_text(self, document: Dict[str, Any]) -> str:
        """Create a comprehensive text representation of the document for embedding"""
        components = []
        
        # Title (most important)
        if document.get('title'):
            components.append(f"Product: {document['title']}")
        
        # Brand
        if document.get('brand'):
            components.append(f"Brand: {document['brand']}")
        
        # Category information
        if document.get('category'):
            components.append(f"Category: {document['category']}")
        
        if document.get('sub_category'):
            components.append(f"Type: {document['sub_category']}")
        
        # Description
        if document.get('description'):
            # Clean up description - remove extra quotes and truncate if too long
            desc = document['description'].strip('"\'').strip()
            if len(desc) > 300:  # Limit description length
                desc = desc[:300] + "..."
            components.append(f"Description: {desc}")
        
        # Price information (for context)
        if document.get('selling_price'):
            components.append(f"Price: ₹{document['selling_price']}")
        
        # Join all components
        embedding_text = " | ".join(components)
        
        return embedding_text

    def generate_embedding(self, text: str, max_retries: int = 3) -> Optional[List[float]]:
        """Generate embedding for a single text using OpenAI API"""
        if not text or not text.strip():
            logger.warning("Empty text provided for embedding")
            return None
        
        # Clean and prepare text
        text = text.strip()
        
        for attempt in range(max_retries):
            try:
                logger.debug(f"Generating embedding for text: {text[:100]}...")
                
                # Call OpenAI embedding API
                response = self.client.embeddings.create(
                    model=self.model_name,
                    input=text
                )
                
                # Extract embedding from response
                embedding = response.data[0].embedding
                
                # Validate embedding dimension
                if len(embedding) != self.embedding_dimension:
                    logger.warning(f"Unexpected embedding dimension: {len(embedding)} (expected {self.embedding_dimension})")
                    return None
                
                logger.debug(f"✅ Generated OpenAI embedding: {len(embedding)} dimensions")
                return embedding
                
            except Exception as e:
                logger.error(f"Embedding attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                if attempt < max_retries - 1:
                    # Exponential backoff
                    wait_time = 2 ** attempt
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed to generate embedding after {max_retries} attempts")
                    return None
        
        return None

    def generate_batch_embeddings(self, texts: List[str], max_retries: int = 3) -> List[Optional[List[float]]]:
        """Generate embeddings for multiple texts in a batch (more efficient)"""
        if not texts:
            return []
        
        # Filter out empty texts
        valid_texts = [text.strip() for text in texts if text and text.strip()]
        if not valid_texts:
            return [None] * len(texts)
        
        for attempt in range(max_retries):
            try:
                logger.debug(f"Generating batch embeddings for {len(valid_texts)} texts...")
                
                # Call OpenAI embedding API with batch
                response = self.client.embeddings.create(
                    model=self.model_name,
                    input=valid_texts
                )
                
                # Extract embeddings from response
                embeddings = []
                for data in response.data:
                    embedding = data.embedding
                    
                    # Validate embedding dimension
                    if len(embedding) != self.embedding_dimension:
                        logger.warning(f"Unexpected embedding dimension: {len(embedding)} (expected {self.embedding_dimension})")
                        embeddings.append(None)
                    else:
                        embeddings.append(embedding)
                
                logger.debug(f"✅ Generated {len(embeddings)} OpenAI embeddings")
                return embeddings
                
            except Exception as e:
                logger.error(f"Batch embedding attempt {attempt + 1}/{max_retries} failed: {str(e)}")
                if attempt < max_retries - 1:
                    # Exponential backoff
                    wait_time = 2 ** attempt
                    logger.info(f"Waiting {wait_time} seconds before retry...")
                    time.sleep(wait_time)
                else:
                    logger.error(f"Failed to generate batch embeddings after {max_retries} attempts")
                    return [None] * len(texts)
        
        return [None] * len(texts)


class MongoDBVectorManager:
    """Manage vector embeddings in MongoDB"""
    
    def __init__(self, connection_string: str = None):
        """Initialize MongoDB connection"""
        # Get connection details from environment
        if not connection_string:
            connection_string = os.environ.get("MONGODB_URI") or os.environ.get("MONGODB_ATLAS_URI")
        
        if not connection_string:
            raise ValueError("MongoDB connection string is required")
        
        self.client = MongoClient(connection_string)
        
        # Get database and collection names from environment
        db_name = os.environ.get("DB_NAME", "econ_data")
        collection_name = os.environ.get("COLLECTION_NAME", "products")
        
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]
        
        logger.info(f"✅ Connected to MongoDB: {db_name}.{collection_name}")
        
        # Show database stats
        total_docs = self.collection.count_documents({})
        existing_openai_embeddings = self.collection.count_documents({"openai_embedding": {"$exists": True}})
        existing_embeddings = self.collection.count_documents({"embedding": {"$exists": True}})
        
        logger.info(f"📊 Database stats:")
        logger.info(f"   Total products: {total_docs:,}")
        logger.info(f"   Products with OpenAI embeddings: {existing_openai_embeddings:,}")
        logger.info(f"   Products with old embeddings: {existing_embeddings:,}")
        logger.info(f"   Products needing OpenAI embeddings: {total_docs - existing_openai_embeddings:,}")

    def get_documents_for_embedding(self, batch_size: int = 50, skip: int = 0) -> List[Dict[str, Any]]:
        """Get documents that need OpenAI embeddings"""
        
        # Find documents without OpenAI embeddings
        cursor = self.collection.find(
            {"openai_embedding": {"$exists": False}},
            {
                "_id": 1,
                "title": 1,
                "brand": 1,
                "category": 1,
                "sub_category": 1,
                "description": 1,
                "selling_price": 1
            }
        ).skip(skip).limit(batch_size)
        
        documents = list(cursor)
        logger.info(f"📦 Found {len(documents)} documents needing OpenAI embeddings")
        
        return documents

    def update_document_embeddings(self, document_id: str, embedding: List[float], embedding_text: str) -> bool:
        """Update a document with its OpenAI embedding"""
        try:
            result = self.collection.update_one(
                {"_id": document_id},
                {
                    "$set": {
                        "openai_embedding": embedding,
                        "openai_embedding_text": embedding_text,
                        "openai_embedding_updated_at": time.time()
                    }
                }
            )
            
            if result.modified_count > 0:
                logger.debug(f"✅ Updated document {document_id} with OpenAI embedding")
                return True
            else:
                logger.warning(f"⚠️  Document {document_id} was not updated")
                return False
                
        except Exception as e:
            logger.error(f"❌ Failed to update document {document_id}: {e}")
            return False

    def update_batch_embeddings(self, updates: List[Dict]) -> int:
        """Update multiple documents with their OpenAI embeddings in batch"""
        if not updates:
            return 0
        
        try:
            from pymongo import UpdateOne
            
            operations = []
            for update in updates:
                operations.append(
                    UpdateOne(
                        {"_id": update["document_id"]},
                        {
                            "$set": {
                                "openai_embedding": update["embedding"],
                                "openai_embedding_text": update["embedding_text"],
                                "openai_embedding_updated_at": time.time()
                            }
                        }
                    )
                )
            
            result = self.collection.bulk_write(operations)
            modified_count = result.modified_count
            
            logger.info(f"✅ Batch updated {modified_count} documents with OpenAI embeddings")
            return modified_count
            
        except Exception as e:
            logger.error(f"❌ Batch update failed: {e}")
            # Try individual updates as fallback
            success_count = 0
            for update in updates:
                try:
                    result = self.collection.update_one(
                        {"_id": update["document_id"]},
                        {
                            "$set": {
                                "openai_embedding": update["embedding"],
                                "openai_embedding_text": update["embedding_text"],
                                "openai_embedding_updated_at": time.time()
                            }
                        }
                    )
                    if result.modified_count > 0:
                        success_count += 1
                except Exception as individual_error:
                    logger.error(f"❌ Individual update failed for {update['document_id']}: {individual_error}")
            
            if success_count > 0:
                logger.info(f"✅ Fallback individual updates: {success_count} documents updated")
            
            return success_count

    def get_embedding_stats(self) -> Dict[str, Any]:
        """Get embedding statistics"""
        try:
            total_docs = self.collection.count_documents({})
            openai_embeddings = self.collection.count_documents({"openai_embedding": {"$exists": True}})
            old_embeddings = self.collection.count_documents({"embedding": {"$exists": True}})
            
            # Get sample embedding to check dimension
            sample_doc = self.collection.find_one({"openai_embedding": {"$exists": True}})
            embedding_dim = len(sample_doc.get("openai_embedding", [])) if sample_doc else 0
            
            return {
                "total_products": total_docs,
                "products_with_openai_embeddings": openai_embeddings,
                "products_with_old_embeddings": old_embeddings,
                "openai_embedding_coverage": f"{openai_embeddings/total_docs*100:.1f}%" if total_docs > 0 else "0%",
                "openai_embedding_dimension": embedding_dim,
                "products_needing_embeddings": max(total_docs - openai_embeddings, 0)
            }
            
        except Exception as e:
            logger.error(f"❌ Failed to get embedding stats: {e}")
            return {}

    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")


def main():
    """Main function to generate OpenAI embeddings for all products"""
    print("🚀 OpenAI Embedding Generator for Product Database")
    print("=" * 60)
    
    try:
        # Initialize components
        embedding_generator = OpenAIEmbeddingGenerator()
        vector_manager = MongoDBVectorManager()
        
        # Get initial stats
        stats = vector_manager.get_embedding_stats()
        print(f"\n📊 Initial Statistics:")
        for key, value in stats.items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
        
        if stats.get("products_needing_embeddings", 0) == 0:
            print("\n✅ All products already have OpenAI embeddings!")
            return
        
        print(f"\n🎯 Will process {stats['products_needing_embeddings']} products")
        
        # Confirm before proceeding
        response = input("\nProceed with generating OpenAI embeddings? (y/N): ").strip().lower()
        if response != 'y':
            print("Operation cancelled.")
            return
        
                # Processing parameters
        batch_size = 50  # Process 50 documents at a time (bulk processing)
        skip = 0
        total_processed = 0
        total_failed = 0
        
        print(f"\n🔄 Starting embedding generation (batch size: {batch_size})...")
        start_time = time.time()
        
        while True:
            # Get batch of documents
            documents = vector_manager.get_documents_for_embedding(batch_size, skip)
            
            if not documents:
                print(f"\n✅ No more documents to process")
                break
            
            print(f"\n📦 Processing batch {skip//batch_size + 1}: {len(documents)} documents")
            
            # Create embedding texts
            embedding_texts = []
            for doc in documents:
                embedding_text = embedding_generator.create_embedding_text(doc)
                embedding_texts.append(embedding_text)
            
            # Generate embeddings in batch
            embeddings = embedding_generator.generate_batch_embeddings(embedding_texts)
            
            # Prepare batch updates
            batch_updates = []
            for i, (doc, embedding, embedding_text) in enumerate(zip(documents, embeddings, embedding_texts)):
                if embedding is not None:
                    batch_updates.append({
                        "document_id": doc["_id"],
                        "embedding": embedding,
                        "embedding_text": embedding_text
                    })
                    print(f"   ✅ Generated embedding for: {doc.get('title', 'Unknown')[:50]}...")
                else:
                    print(f"   ❌ Failed to generate embedding for: {doc.get('title', 'Unknown')[:50]}...")
                    total_failed += 1
            
            # Update database with batch
            if batch_updates:
                updated_count = vector_manager.update_batch_embeddings(batch_updates)
                total_processed += updated_count
                print(f"   📝 Updated {updated_count} documents in database")
            
            skip += batch_size
            
            # Show progress
            elapsed_time = time.time() - start_time
            print(f"   ⏱️  Progress: {total_processed} processed, {total_failed} failed, {elapsed_time:.1f}s elapsed")
            
            # Small delay to respect API rate limits
            time.sleep(1)
        
        # Final statistics
        print(f"\n🎉 Processing completed!")
        print(f"   Total processed: {total_processed}")
        print(f"   Total failed: {total_failed}")
        print(f"   Total time: {time.time() - start_time:.1f}s")
        
        # Get final stats
        final_stats = vector_manager.get_embedding_stats()
        print(f"\n📊 Final Statistics:")
        for key, value in final_stats.items():
            print(f"   {key.replace('_', ' ').title()}: {value}")
        
    except KeyboardInterrupt:
        print(f"\n⚠️  Process interrupted by user")
    except Exception as e:
        logger.error(f"❌ Main process failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up
        try:
            vector_manager.close()
        except:
            pass

if __name__ == "__main__":
    main()
