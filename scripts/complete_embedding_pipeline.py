#!/usr/bin/env python3
"""
Complete Embedding Pipeline: Generate embedding text AND OpenAI embeddings

This script:
1. Generates structured embedding text using build_embedding_text()
2. Creates OpenAI embeddings from that text using text-embedding-3-small
3. Stores both openai_embedding_text and openai_embedding in MongoDB
4. Processes in configurable batches for optimal performance
"""

import os
import sys
import argparse
import logging
import time
from typing import Dict, Any, List, Optional
from pymongo import MongoClient, UpdateOne
from pymongo.errors import BulkWriteError
from dotenv import load_dotenv
import openai
from openai import OpenAI

from scripts.embedding_text_generator import build_embedding_text, should_regenerate_embedding

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class CompletEmbeddingPipeline:
    """Complete pipeline for generating embedding text and OpenAI embeddings."""
    
    def __init__(self, connection_string: Optional[str] = None):
        """Initialize the complete embedding pipeline."""
        
        # Initialize OpenAI client
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.openai_client = OpenAI(api_key=api_key)
        self.model_name = "text-embedding-3-small"
        self.embedding_dimension = 1536
        
        # Get MongoDB connection
        if not connection_string:
            connection_string = (
                os.environ.get("MONGODB_URI") or 
                os.environ.get("MONGODB_ATLAS_URI") or 
                "mongodb://localhost:27017/"
            )
        
        self.client = MongoClient(connection_string)
        
        # Get database and collection names
        self.db_name = os.environ.get("DB_NAME", "ecom_data")
        self.collection_name = os.environ.get("COLLECTION_NAME", "products")
        
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]
        
        logger.info(f"Connected to MongoDB: {self.db_name}.{self.collection_name}")
        logger.info(f"OpenAI Model: {self.model_name}")
        
        # Test connections
        try:
            self.client.admin.command('ping')
            logger.info("MongoDB connection successful")
        except Exception as e:
            logger.error(f"MongoDB connection failed: {e}")
            raise
    
    def generate_openai_embedding(self, text: str, max_retries: int = 3) -> Optional[List[float]]:
        """Generate OpenAI embedding with retry logic."""
        
        for attempt in range(max_retries):
            try:
                response = self.openai_client.embeddings.create(
                    model=self.model_name,
                    input=text,
                    encoding_format="float"
                )
                
                embedding = response.data[0].embedding
                
                if len(embedding) != self.embedding_dimension:
                    logger.warning(f"Unexpected embedding dimension: {len(embedding)}, expected {self.embedding_dimension}")
                
                # Validate embedding format
                if not isinstance(embedding, list) or not all(isinstance(x, (int, float)) for x in embedding):
                    logger.error(f"Invalid embedding format: {type(embedding)}")
                    return None
                
                # Ensure all values are finite
                if not all(isinstance(x, (int, float)) and not (x != x) for x in embedding):  # NaN check
                    logger.error("Embedding contains NaN or infinite values")
                    return None
                
                return embedding
                
            except openai.RateLimitError as e:
                wait_time = (2 ** attempt) * 1  # Exponential backoff: 1, 2, 4 seconds
                logger.warning(f"Rate limit hit, waiting {wait_time}s before retry {attempt + 1}/{max_retries}")
                time.sleep(wait_time)
                
            except openai.APIError as e:
                logger.error(f"OpenAI API error: {e}")
                if attempt == max_retries - 1:
                    return None
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Unexpected error generating embedding: {e}")
                if attempt == max_retries - 1:
                    return None
                time.sleep(1)
        
        logger.error(f"Failed to generate embedding after {max_retries} attempts")
        return None
    
    def process_batch_complete(self, documents: List[Dict[str, Any]], dry_run: bool = False) -> Dict[str, int]:
        """Process a batch with complete embedding generation (text + vectors)."""
        
        results = {
            "processed": 0,
            "text_generated": 0,
            "embeddings_generated": 0,
            "updated": 0,
            "skipped": 0,
            "errors": 0
        }
        
        updates = []
        progress_counter = 0
        
        for doc in documents:
            try:
                results["processed"] += 1
                progress_counter += 1
                doc_id = doc["_id"]
                
                # 1. Generate embedding text
                new_embedding_text = build_embedding_text(doc)
                results["text_generated"] += 1
                
                # 2. Check if we need to update
                current_embedding_text = doc.get("openai_embedding_text", "")
                current_embedding = doc.get("openai_embedding", [])
                
                # Skip if embedding text hasn't changed and embedding exists
                if (new_embedding_text == current_embedding_text and 
                    current_embedding and len(current_embedding) == self.embedding_dimension):
                    results["skipped"] += 1
                    logger.debug(f"Skipping {doc_id}: embedding unchanged")
                    
                    # Show progress every 10 records (including skipped)
                    if progress_counter % 10 == 0:
                        logger.info(f"✅ Progress: {progress_counter}/{len(documents)} records processed (skipped: {doc_id})")
                    continue
                
                # 3. Generate OpenAI embedding
                embedding = self.generate_openai_embedding(new_embedding_text)
                
                if embedding:
                    results["embeddings_generated"] += 1
                    
                    if not dry_run:
                        updates.append(UpdateOne(
                            {"_id": doc_id},
                            {
                                "$set": {
                                    "openai_embedding_text": new_embedding_text,
                                    "openai_embedding": embedding,
                                    "embedding_updated_at": time.time(),
                                    "embedding_model": self.model_name
                                }
                            }
                        ))
                    
                    results["updated"] += 1
                    logger.debug(f"Generated embedding for {doc_id}: {len(embedding)} dimensions")
                    
                    # Show success message every 10 records
                    if progress_counter % 10 == 0:
                        logger.info(f"✅ Progress: {progress_counter}/{len(documents)} records processed successfully (latest: {doc_id})")
                else:
                    results["errors"] += 1
                    logger.error(f"Failed to generate embedding for {doc_id}")
                    
                    # Show progress even for errors
                    if progress_counter % 10 == 0:
                        logger.info(f"⚠️  Progress: {progress_counter}/{len(documents)} records processed (error on: {doc_id})")
                    
            except Exception as e:
                results["errors"] += 1
                # Don't include the full document object in error logging to avoid printing embeddings
                doc_id = doc.get('_id', 'unknown')
                error_msg = str(e)
                # Truncate very long error messages that might contain embedding vectors
                if len(error_msg) > 200:
                    error_msg = error_msg[:200] + "... [truncated]"
                logger.error(f"Error processing document {doc_id}: {error_msg}")
                
                # Show progress even for exceptions
                if progress_counter % 10 == 0:
                    logger.info(f"🔴 Progress: {progress_counter}/{len(documents)} records processed (exception on: {doc_id})")
        
        # Execute batch updates
        if updates and not dry_run:
            try:
                result = self.collection.bulk_write(updates, ordered=False)
                logger.info(f"✅ Bulk write completed: {result.modified_count}/{len(updates)} documents updated successfully")
                
                # Show detailed success for smaller batches
                if len(updates) <= 50:
                    logger.info(f"🎯 Successfully stored embeddings for {result.modified_count} documents")
            except BulkWriteError as bwe:
                # Log bulk write errors without including the full embedding vectors
                write_errors = bwe.details.get("writeErrors", [])
                successful_writes = len(updates) - len(write_errors)
                logger.error(f"❌ Bulk write partial failure: {successful_writes}/{len(updates)} successful, {len(write_errors)} errors")
                
                # Log individual errors with safe formatting (no embedding data)
                for i, error in enumerate(write_errors[:5]):  # Limit to first 5 errors
                    error_code = error.get("code", "unknown")
                    error_msg = error.get("errmsg", "unknown error")
                    # Truncate long error messages that might contain embedding data
                    if len(str(error_msg)) > 100:
                        error_msg = str(error_msg)[:100] + "... [truncated]"
                    logger.error(f"Write error {i+1}: Code {error_code} - {error_msg}")
                
                if len(write_errors) > 5:
                    logger.error(f"... and {len(write_errors) - 5} more write errors")
                
                results["errors"] += len(write_errors)
            except Exception as e:
                # Handle any other database errors safely
                error_msg = str(e)
                if len(error_msg) > 200:
                    error_msg = error_msg[:200] + "... [truncated]"
                logger.error(f"❌ Database operation error: {error_msg}")
                results["errors"] += len(updates)
        elif updates and dry_run:
            logger.info(f"🔍 Dry run: Would update {len(updates)} documents")
        
        # Final batch summary
        if progress_counter > 0:
            logger.info(f"📊 Batch completed: {progress_counter} records processed, {results['updated']} updated, {results['skipped']} skipped, {results['errors']} errors")
        
        return results
    
    def get_collection_stats(self) -> Dict[str, int]:
        """Get detailed collection statistics."""
        try:
            total_docs = self.collection.count_documents({})
            
            # Count different states
            with_embedding_text = self.collection.count_documents({
                "openai_embedding_text": {"$exists": True, "$ne": ""}
            })
            
            with_embeddings = self.collection.count_documents({
                "openai_embedding": {"$exists": True, "$ne": []}
            })
            
            complete_records = self.collection.count_documents({
                "openai_embedding_text": {"$exists": True, "$ne": ""},
                "openai_embedding": {"$exists": True, "$ne": []}
            })
            
            return {
                "total_documents": total_docs,
                "with_embedding_text": with_embedding_text,
                "with_embeddings": with_embeddings,
                "complete_records": complete_records,
                "needs_processing": total_docs - complete_records
            }
            
        except Exception as e:
            logger.error(f"Failed to get collection stats: {e}")
            return {}
    
    def run_complete_pipeline(self, batch_size: int = 1000, dry_run: bool = False, 
                            max_documents: Optional[int] = None) -> Dict[str, Any]:
        """Run the complete embedding pipeline."""
        
        logger.info("Starting complete embedding pipeline (text + embeddings)")
        logger.info(f"Batch size: {batch_size}")
        logger.info(f"Dry run: {dry_run}")
        logger.info(f"Max documents: {max_documents or 'unlimited'}")
        
        # Get initial stats
        initial_stats = self.get_collection_stats()
        logger.info(f"Initial stats: {initial_stats}")
        
        if initial_stats.get("total_documents", 0) == 0:
            logger.warning("No documents found in collection")
            return {"error": "No documents found"}
        
        # Initialize counters
        total_results = {
            "processed": 0,
            "text_generated": 0,
            "embeddings_generated": 0,
            "updated": 0,
            "skipped": 0,
            "errors": 0,
            "batches": 0
        }
        
        start_time = time.time()
        skip = 0
        
        # Process in batches
        while True:
            if max_documents and total_results["processed"] >= max_documents:
                logger.info(f"Reached maximum documents limit: {max_documents}")
                break
                
            logger.info(f"Processing batch starting at document {skip}")
            
            try:
                # Calculate batch size for this iteration
                current_batch_size = batch_size
                if max_documents:
                    remaining = max_documents - total_results["processed"]
                    current_batch_size = min(batch_size, remaining)
                
                # Fetch batch - prioritize documents without complete embeddings
                cursor = self.collection.find({
                    "$or": [
                        {"openai_embedding_text": {"$exists": False}},
                        {"openai_embedding": {"$exists": False}},
                        {"openai_embedding": []}
                    ]
                }).skip(skip).limit(current_batch_size)
                
                documents = list(cursor)
                
                if not documents:
                    # Try getting any documents if no incomplete ones found
                    cursor = self.collection.find({}).skip(skip).limit(current_batch_size)
                    documents = list(cursor)
                    
                    if not documents:
                        logger.info("No more documents to process")
                        break
                
                # Process batch
                batch_results = self.process_batch_complete(documents, dry_run)
                
                # Update totals
                for key in batch_results:
                    total_results[key] += batch_results[key]
                
                total_results["batches"] += 1
                
                logger.info(f"Batch {total_results['batches']} completed: "
                           f"processed={batch_results['processed']}, "
                           f"text_generated={batch_results['text_generated']}, "
                           f"embeddings_generated={batch_results['embeddings_generated']}, "
                           f"updated={batch_results['updated']}, "
                           f"skipped={batch_results['skipped']}, "
                           f"errors={batch_results['errors']}")
                
                skip += len(documents)
                
                # Rate limiting - small delay between batches
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error processing batch starting at {skip}: {e}")
                total_results["errors"] += current_batch_size
                skip += current_batch_size
        
        # Calculate final stats
        end_time = time.time()
        duration = end_time - start_time
        final_stats = self.get_collection_stats()
        
        pipeline_results = {
            "pipeline_summary": total_results,
            "duration_seconds": duration,
            "documents_per_second": total_results["processed"] / duration if duration > 0 else 0,
            "embeddings_per_second": total_results["embeddings_generated"] / duration if duration > 0 else 0,
            "initial_stats": initial_stats,
            "final_stats": final_stats,
            "dry_run": dry_run
        }
        
        logger.info("Complete pipeline finished!")
        logger.info(f"Total processed: {total_results['processed']}")
        logger.info(f"Embedding texts generated: {total_results['text_generated']}")
        logger.info(f"OpenAI embeddings generated: {total_results['embeddings_generated']}")
        logger.info(f"Documents updated: {total_results['updated']}")
        logger.info(f"Documents skipped: {total_results['skipped']}")
        logger.info(f"Errors: {total_results['errors']}")
        logger.info(f"Duration: {duration:.2f} seconds")
        logger.info(f"Processing rate: {pipeline_results['documents_per_second']:.2f} docs/sec")
        logger.info(f"Embedding rate: {pipeline_results['embeddings_per_second']:.2f} embeddings/sec")
        
        return pipeline_results
    
    def close(self):
        """Close connections."""
        if self.client:
            self.client.close()
            logger.info("MongoDB connection closed")


def main():
    """Main function to run the complete embedding pipeline."""
    
    parser = argparse.ArgumentParser(description="Complete embedding pipeline: generate text + OpenAI embeddings")
    parser.add_argument("--batch-size", type=int, default=1000, help="Number of documents per batch")
    parser.add_argument("--dry-run", action="store_true", help="Run without making changes")
    parser.add_argument("--max-documents", type=int, help="Maximum number of documents to process")
    parser.add_argument("--connection-string", type=str, help="MongoDB connection string")
    
    args = parser.parse_args()
    
    try:
        # Initialize pipeline
        pipeline = CompletEmbeddingPipeline(args.connection_string)
        
        # Run complete pipeline
        results = pipeline.run_complete_pipeline(
            batch_size=args.batch_size,
            dry_run=args.dry_run,
            max_documents=args.max_documents
        )
        
        # Print summary
        if "error" not in results:
            print("\n" + "="*60)
            print("COMPLETE EMBEDDING PIPELINE SUMMARY")
            print("="*60)
            print(f"Documents processed: {results['pipeline_summary']['processed']:,}")
            print(f"Embedding texts generated: {results['pipeline_summary']['text_generated']:,}")
            print(f"OpenAI embeddings generated: {results['pipeline_summary']['embeddings_generated']:,}")
            print(f"Documents updated: {results['pipeline_summary']['updated']:,}")
            print(f"Documents skipped: {results['pipeline_summary']['skipped']:,}")
            print(f"Errors: {results['pipeline_summary']['errors']:,}")
            print(f"Duration: {results['duration_seconds']:.2f} seconds")
            print(f"Processing rate: {results['documents_per_second']:.2f} docs/sec")
            print(f"Embedding rate: {results['embeddings_per_second']:.2f} embeddings/sec")
            print()
            print("Database State:")
            print(f"  Before: {results['initial_stats']['complete_records']:,} complete records")
            print(f"  After:  {results['final_stats']['complete_records']:,} complete records")
            print(f"  Improvement: +{results['final_stats']['complete_records'] - results['initial_stats']['complete_records']:,}")
        
        pipeline.close()
        
    except KeyboardInterrupt:
        logger.info("Pipeline interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
