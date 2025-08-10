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

    async def search_products_text(self, query: str, limit: int = 20, *, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search products using text search with optional strict filters.
        
        Args:
            query: Search query string
            limit: Maximum number of results
            filters: Optional MongoDB filter document to enforce category/price/color
            
        Returns:
            List of matching products with text scores
        """
        try:
            # Merge $text with provided filters inside a single $match
            if filters:
                # If filters already an $and/$or expression, compose with $text using $and
                match_expr: Dict[str, Any] = {"$and": [{"$text": {"$search": query}}, filters]}
            else:
                match_expr = {"$text": {"$search": query}}
            
            pipeline = [
                {"$match": match_expr},
                {"$addFields": {"score": {"$meta": "textScore"}}},
                {"$sort": {"score": {"$meta": "textScore"}}},
                {"$limit": int(limit)}
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

    async def search_products_vector(self, vector: List[float], limit: int = 20, *, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search products using vector similarity with optional strict filters.
        
        Args:
            vector: Query embedding vector
            limit: Maximum number of results
            filters: Optional MongoDB filter document to enforce category/price/color
            
        Returns:
            List of matching products with vector scores
        """
        try:
            # Oversample candidates, then post filter and limit
            num_candidates = max(limit * 60, 200)
            prelimit = max(limit * 5, 50)
            pipeline = [
                {
                    "$vectorSearch": {
                        "index": "vector_index",
                        "path": "openai_embedding",
                        "queryVector": vector,
                        "numCandidates": int(num_candidates),
                        "limit": int(prelimit)
                    }
                },
                {"$addFields": {"vector_score": {"$meta": "vectorSearchScore"}}},
            ]
            
            if filters:
                pipeline.append({"$match": filters})
            
            pipeline.extend([
                {"$sort": {"vector_score": -1}},
                {"$limit": int(limit)}
            ])
            
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

    async def search_products_hybrid(self, query: str, vector: List[float], limit: int = 20, *, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Search products using hybrid text + vector search with optional strict filters.
        
        Args:
            query: Search query string
            vector: Query embedding vector
            limit: Maximum number of results
            filters: Optional MongoDB filter document to enforce category/price/color
            
        Returns:
            List of matching products with combined scores
        """
        try:
            # Run both searches with filters applied
            text_results = await self.search_products_text(query, limit=limit, filters=filters)
            vector_results = await self.search_products_vector(vector, limit=limit, filters=filters)
            
            # Combine and deduplicate results
            combined_results: Dict[str, Dict[str, Any]] = {}
            
            # Add text results
            for product in text_results:
                pid = product["_id"]
                combined_results[pid] = product
                combined_results[pid]["text_score"] = product.get("search_score", 0.0)
                combined_results[pid]["search_type"] = "hybrid"
            
            # Add vector results
            for product in vector_results:
                pid = product["_id"]
                if pid in combined_results:
                    combined_results[pid]["vector_score"] = product.get("vector_score", 0.0)
                    text_score = combined_results[pid].get("text_score", 0.0)
                    vector_score = product.get("vector_score", 0.0)
                    combined_results[pid]["search_score"] = (text_score * 0.4 + vector_score * 0.6)
                else:
                    combined_results[pid] = product
                    combined_results[pid]["vector_score"] = product.get("vector_score", 0.0)
                    combined_results[pid]["text_score"] = 0.0
                    combined_results[pid]["search_score"] = product.get("vector_score", 0.0)
                    combined_results[pid]["search_type"] = "hybrid"
            
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
