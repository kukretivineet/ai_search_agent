#!/usr/bin/env python3
"""
Repository for product data access and embedding management.
Enhanced with search capabilities for OpenAI embeddings and vector search.
"""

from typing import Dict, Any, List, Optional
from bson import ObjectId
from pymongo import UpdateOne
from pymongo.errors import BulkWriteError
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import get_settings
from app.domain.embeddings.models import ProductEmbedding
import logging

logger = logging.getLogger(__name__)


class ProductRepository:
    """Product repository for MongoDB operations."""

from typing import List, Dict, Any, Optional
import logging
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import TEXT

# Configure logger
logger = logging.getLogger(__name__)


class ProductRepository:
    """Repository for product data operations in MongoDB."""

    def __init__(self, collection: AsyncIOMotorCollection):
        """Initialize repository with MongoDB collection.
        
        Args:
            collection: MongoDB collection instance
        """
        self.collection = collection

    async def get_all_products(self, skip: int = 0, limit: int = 10) -> List[Dict[str, Any]]:
        """Get all products with pagination.
        
        Args:
            skip: Number of documents to skip
            limit: Maximum number of documents to return
            
        Returns:
            List of product documents
        """
        try:
            cursor = self.collection.find().skip(skip).limit(limit)
            products = await cursor.to_list(length=limit)
            
            # Convert ObjectId to string
            for product in products:
                product["_id"] = str(product["_id"])
            
            logger.info(f"Retrieved {len(products)} products")
            return products
            
        except Exception as e:
            logger.error(f"Error retrieving products: {e}")
            return []

    async def search_products_text(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        """Search products using text search.
        
        Args:
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            List of matching products with text scores
        """
        try:
            pipeline = [
                {"$match": {"$text": {"$search": query}}},
                {"$addFields": {"score": {"$meta": "textScore"}}},
                {"$sort": {"score": {"$meta": "textScore"}}},
                {"$limit": limit}
            ]
            
            cursor = self.collection.aggregate(pipeline)
            products = await cursor.to_list(length=limit)
            
            # Convert ObjectId to string and add search metadata
            for product in products:
                product["_id"] = str(product["_id"])
                product["search_score"] = product.get("score", 0.0)
                product["search_type"] = "text"
            
            logger.info(f"Text search found {len(products)} products for query: '{query}'")
            return products
            
        except Exception as e:
            logger.error(f"Error in text search: {e}")
            return []

    async def search_products_vector(self, vector: List[float], limit: int = 20) -> List[Dict[str, Any]]:
        """Search products using vector similarity.
        
        Args:
            vector: Query embedding vector
            limit: Maximum number of results
            
        Returns:
            List of matching products with vector scores
        """
        try:
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "embedding_vector",
                        "queryVector": vector,
                        "numCandidates": limit * 10,
                        "limit": limit
                    }
                },
                {
                    "$addFields": {
                        "vector_score": {"$meta": "vectorSearchScore"}
                    }
                }
            ]
            
            cursor = self.collection.aggregate(pipeline)
            products = await cursor.to_list(length=limit)
            
            # Convert ObjectId to string and add search metadata
            for product in products:
                product["_id"] = str(product["_id"])
                product["search_type"] = "vector"
            
            logger.info(f"Vector search found {len(products)} products")
            return products
            
        except Exception as e:
            logger.error(f"Error in vector search: {e}")
            return []

    async def search_products_hybrid(self, query: str, vector: List[float], limit: int = 20) -> List[Dict[str, Any]]:
        """Search products using hybrid text + vector search.
        
        Args:
            query: Search query string
            vector: Query embedding vector
            limit: Maximum number of results
            
        Returns:
            List of matching products with combined scores
        """
        try:
            # Run both searches in parallel
            text_results = await self.search_products_text(query, limit)
            vector_results = await self.search_products_vector(vector, limit)
            
            # Combine and deduplicate results
            combined_results = {}
            
            # Add text results
            for product in text_results:
                product_id = product["_id"]
                combined_results[product_id] = product
                combined_results[product_id]["text_score"] = product.get("search_score", 0.0)
                combined_results[product_id]["search_type"] = "hybrid"
            
            # Add vector results
            for product in vector_results:
                product_id = product["_id"]
                if product_id in combined_results:
                    # Merge scores for products found in both searches
                    combined_results[product_id]["vector_score"] = product.get("vector_score", 0.0)
                    # Calculate combined score (weighted average)
                    text_score = combined_results[product_id].get("text_score", 0.0)
                    vector_score = product.get("vector_score", 0.0)
                    combined_results[product_id]["search_score"] = (text_score * 0.4 + vector_score * 0.6)
                else:
                    # Add vector-only results
                    combined_results[product_id] = product
                    combined_results[product_id]["vector_score"] = product.get("vector_score", 0.0)
                    combined_results[product_id]["text_score"] = 0.0
                    combined_results[product_id]["search_score"] = product.get("vector_score", 0.0)
                    combined_results[product_id]["search_type"] = "hybrid"
            
            # Sort by combined score and return top results
            results = list(combined_results.values())
            results.sort(key=lambda x: x.get("search_score", 0.0), reverse=True)
            
            logger.info(f"Hybrid search found {len(results)} products for query: '{query}'")
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Error in hybrid search: {e}")
            return []

    async def get_product_count(self) -> int:
        """Get total count of products in collection.
        
        Returns:
            Total number of products
        """
        try:
            count = await self.collection.count_documents({})
            logger.info(f"Total products in collection: {count}")
            return count
            
        except Exception as e:
            logger.error(f"Error getting product count: {e}")
            return 0

    async def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Get a single product by ID.
        
        Args:
            product_id: Product ID string
            
        Returns:
            Product document or None if not found
        """
        try:
            from bson import ObjectId
            
            # Try to convert to ObjectId if it's a valid ObjectId string
            try:
                oid = ObjectId(product_id)
                product = await self.collection.find_one({"_id": oid})
            except:
                # If not a valid ObjectId, search as string
                product = await self.collection.find_one({"_id": product_id})
            
            if product:
                product["_id"] = str(product["_id"])
                logger.info(f"Found product: {product_id}")
            else:
                logger.warning(f"Product not found: {product_id}")
            
            return product
            
        except Exception as e:
            logger.error(f"Error retrieving product {product_id}: {e}")
            return None

    async def create_text_index(self):
        """Create text search index on relevant fields."""
        try:
            # Create compound text index
            await self.collection.create_index([
                ("title", TEXT),
                ("brand", TEXT),
                ("category", TEXT),
                ("sub_category", TEXT),
                ("description", TEXT),
                ("embedding_text", TEXT)
            ], name="text_search_index")
            
            logger.info("Text search index created successfully")
            
        except Exception as e:
            logger.error(f"Error creating text index: {e}")

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check on the repository.
        
        Returns:
            Health status information
        """
        try:
            # Check if collection is accessible
            count = await self.collection.count_documents({}, limit=1)
            
            # Check indexes
            indexes = await self.collection.index_information()
            
            return {
                "status": "healthy",
                "collection_accessible": True,
                "sample_document_count": count,
                "indexes": list(indexes.keys())
            }
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "collection_accessible": False
            }
    
    def __init__(self, database: AsyncIOMotorDatabase):
        """
        Initialize repository with database connection.
        
        Args:
            database: AsyncIOMotorDatabase instance
        """
        Initialize repository with database connection.
        
        Args:
            database: AsyncIOMotorDatabase instance
        """
        self.db = database
        self.collection = database.products
        self.settings = get_settings()
        self.logger = logging.getLogger(__name__)
    
    async def get_products_without_embeddings(
        self, 
        limit: int = 1000, 
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get products that don't have embeddings yet.
        
        Args:
            limit: Maximum number of products to return
            skip: Number of products to skip
            
        Returns:
            List of product documents
        """
        cursor = self.collection.find(
            {"embedding": {"$exists": False}},
            limit=limit,
            skip=skip
        )
        return await cursor.to_list(length=limit)
    
    async def count_products_without_embeddings(self) -> int:
        """Count products without embeddings."""
        return await self.collection.count_documents({"embedding": {"$exists": False}})
    
    async def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a single product by ID.
        
        Args:
            product_id: Product ID (string or ObjectId)
            
        Returns:
            Product document or None
        """
        try:
            if isinstance(product_id, str):
                product_id = ObjectId(product_id)
            
            return await self.collection.find_one({"_id": product_id})
        except Exception as e:
            self.logger.error(f"Error fetching product {product_id}: {e}")
            return None
    
    async def bulk_update_embeddings(self, embeddings: List[ProductEmbedding]) -> int:
        """
        Bulk update products with embeddings.
        
        Args:
            embeddings: List of ProductEmbedding objects
            
        Returns:
            Number of products updated
        """
        if not embeddings:
            return 0
        
        try:
            # Prepare bulk operations
            operations = []
            for embedding in embeddings:
                update_doc = {
                    "$set": {
                        "embedding": embedding.embedding_vector,
                        "embedding_metadata": {
                            "model": embedding.metadata.model,
                            "dimensions": embedding.metadata.dimensions,
                            "generated_at": embedding.metadata.generated_at.isoformat(),
                            "source_text": embedding.metadata.source_text
                        }
                    }
                }
                
                operations.append(
                    UpdateOne(
                        {"_id": ObjectId(embedding.product_id)},
                        update_doc
                    )
                )
            
            # Execute bulk write
            result = await self.collection.bulk_write(operations, ordered=False)
            
            self.logger.debug(f"Bulk update completed: {result.modified_count} modified")
            return result.modified_count
            
        except BulkWriteError as e:
            self.logger.error(f"Bulk write error: {e.details}")
            # Return count of successful operations
            return len(e.details.get("writeErrors", []))
        except Exception as e:
            self.logger.error(f"Error in bulk update: {e}")
            return 0
    
    async def update_product_embedding(self, embedding: ProductEmbedding) -> bool:
        """
        Update a single product with embedding.
        
        Args:
            embedding: ProductEmbedding object
            
        Returns:
            True if updated successfully
        """
        try:
            update_doc = {
                "$set": {
                    "embedding": embedding.embedding_vector,
                    "embedding_metadata": {
                        "model": embedding.metadata.model,
                        "dimensions": embedding.metadata.dimensions,
                        "generated_at": embedding.metadata.generated_at.isoformat(),
                        "source_text": embedding.metadata.source_text
                    }
                }
            }
            
            result = await self.collection.update_one(
                {"_id": ObjectId(embedding.product_id)},
                update_doc
            )
            
            return result.modified_count > 0
            
        except Exception as e:
            self.logger.error(f"Error updating single embedding: {e}")
            return False
    
    async def get_products_with_embeddings(
        self,
        limit: int = 1000,
        skip: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Get products that have embeddings.
        
        Args:
            limit: Maximum number of products to return
            skip: Number of products to skip
            
        Returns:
            List of product documents with embeddings
        """
        cursor = self.collection.find(
            {"embedding": {"$exists": True}},
            limit=limit,
            skip=skip
        )
        return await cursor.to_list(length=limit)
    
    async def count_products_with_embeddings(self) -> int:
        """Count products with embeddings."""
        return await self.collection.count_documents({"embedding": {"$exists": True}})
    
    async def get_embedding_stats(self) -> Dict[str, int]:
        """
        Get embedding statistics.
        
        Returns:
            Dict with embedding counts and totals
        """
        try:
            total_products = await self.collection.count_documents({})
            with_embeddings = await self.count_products_with_embeddings()
            without_embeddings = await self.count_products_without_embeddings()
            
            return {
                "total_products": total_products,
                "with_embeddings": with_embeddings,
                "without_embeddings": without_embeddings,
                "completion_percentage": round((with_embeddings / total_products) * 100, 2) if total_products > 0 else 0
            }
        except Exception as e:
            self.logger.error(f"Error getting embedding stats: {e}")
            return {
                "total_products": 0,
                "with_embeddings": 0,
                "without_embeddings": 0,
                "completion_percentage": 0
            }
    
    async def search_products_by_embedding(
        self,
        query_embedding: List[float],
        limit: int = 10,
        similarity_threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search products using vector similarity.
        
        Args:
            query_embedding: Query embedding vector
            limit: Maximum number of results
            similarity_threshold: Minimum similarity score
            
        Returns:
            List of matching products with similarity scores
        """
        try:
            # Note: This is a placeholder for vector search
            # In production, you'd use Atlas Vector Search or similar
            pipeline = [
                {
                    "$match": {
                        "embedding": {"$exists": True}
                    }
                },
                {
                    "$limit": limit
                }
            ]
            
            cursor = self.collection.aggregate(pipeline)
            return await cursor.to_list(length=limit)
            
        except Exception as e:
            self.logger.error(f"Error in vector search: {e}")
            return []
    
    async def create_embedding_index(self) -> bool:
        """
        Create index for embedding searches.
        Note: For production, use Atlas Vector Search indexes.
        
        Returns:
            True if index created successfully
        """
        try:
            # Create compound index for embedding metadata
            await self.collection.create_index([
                ("embedding_metadata.model", 1),
                ("embedding_metadata.generated_at", -1)
            ])
            
            self.logger.info("Embedding metadata index created")
            return True
            
        except Exception as e:
            self.logger.error(f"Error creating embedding index: {e}")
            return False
    
    async def find_products(
        self, 
        query: Dict[str, Any], 
        limit: int = 20, 
        skip: int = 0,
        projection: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Find products matching the given query for search operations.
        
        Args:
            query: MongoDB query dictionary
            limit: Maximum number of results
            skip: Number of documents to skip
            projection: Fields to include/exclude
            
        Returns:
            List of product documents
        """
        try:
            if projection is None:
                projection = {
                    "_id": 1,
                    "title": 1,
                    "brand": 1,
                    "category": 1,
                    "sub_category": 1,
                    "description": 1,
                    "selling_price_numeric": 1,
                    "price_inr": 1,
                    "images": {"$slice": 1}
                }
            
            cursor = self.collection.find(query, projection).skip(skip).limit(limit)
            results = await cursor.to_list(length=limit)
            
            # Convert ObjectId to string for JSON serialization
            for result in results:
                if '_id' in result:
                    result['_id'] = str(result['_id'])
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error finding products for search: {e}")
            return []
    
    async def count_documents(self, query: Dict[str, Any]) -> int:
        """
        Count documents matching the query for pagination.
        
        Args:
            query: MongoDB query dictionary
            
        Returns:
            Number of matching documents
        """
        try:
            return await self.collection.count_documents(query)
        except Exception as e:
            self.logger.error(f"Error counting documents: {e}")
            return 0
    
    async def get_search_stats(self) -> Dict[str, Any]:
        """
        Get database statistics for search operations.
        
        Returns:
            Dictionary with database stats
        """
        try:
            settings = get_settings()
            total_docs = await self.collection.count_documents({})
            with_openai_embeddings = await self.collection.count_documents({
                "openai_embedding": {"$exists": True}
            })
            
            embedding_coverage = (with_openai_embeddings / total_docs * 100) if total_docs > 0 else 0
            
            return {
                "database": settings.DB_NAME,
                "collection": settings.COLLECTION_NAME,
                "total_documents": total_docs,
                "documents_with_openai_embeddings": with_openai_embeddings,
                "missing_openai_embeddings": max(total_docs - with_openai_embeddings, 0),
                "openai_embedding_coverage": f"{embedding_coverage:.1f}%"
            }
            
        except Exception as e:
            self.logger.error(f"Error getting search stats: {e}")
            return {"error": str(e)}
