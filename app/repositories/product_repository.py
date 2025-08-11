"""Product repository for MongoDB operations."""

from typing import List, Dict, Any, Optional
import logging
from motor.motor_asyncio import AsyncIOMotorCollection
from pymongo import TEXT

# Configure logger
logger = logging.getLogger(__name__)


class ProductRepository:
    """Repository for product data operations in MongoDB.
    
    All aggregation operations use allowDiskUse=True to prevent memory limit errors
    when sorting large result sets. This allows MongoDB to use disk storage for
    operations that exceed the 32MB memory limit.
    """

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
            
            cursor = self.collection.aggregate(pipeline, allowDiskUse=True)
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

    async def search_products_text_paginated(
        self, 
        query: str, 
        page: int = 1, 
        page_size: int = 20, 
        *, 
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Search products using text search with pagination and total count.
        
        Args:
            query: Search query string
            page: Page number (1-based)
            page_size: Number of results per page
            filters: Optional MongoDB filter document to enforce category/price/color
            
        Returns:
            Dictionary with results, total count, and pagination metadata
        """
        try:
            # Merge $text with provided filters inside a single $match
            if filters:
                match_expr: Dict[str, Any] = {"$and": [{"$text": {"$search": query}}, filters]}
            else:
                match_expr = {"$text": {"$search": query}}
            
            # Calculate skip value for pagination
            skip = (page - 1) * page_size
            
            # For large collections, use a more memory-efficient approach
            # First get total count without sorting
            count_pipeline = [
                {"$match": match_expr},
                {"$count": "total"}
            ]
            
            count_cursor = self.collection.aggregate(count_pipeline, allowDiskUse=True)
            count_result = await count_cursor.to_list(length=1)
            total = count_result[0]["total"] if count_result else 0
            
            # Then get paginated results with sort
            results_pipeline = [
                {"$match": match_expr},
                {"$addFields": {"score": {"$meta": "textScore"}}},
                {"$sort": {"score": {"$meta": "textScore"}}},
                {"$skip": skip},
                {"$limit": page_size}
            ]
            
            results_cursor = self.collection.aggregate(results_pipeline, allowDiskUse=True)
            products = await results_cursor.to_list(length=page_size)
            
            # Convert ObjectId to string and add search metadata
            for product in products:
                product["_id"] = str(product["_id"])
                product["search_score"] = product.get("score", 0.0)
                product["search_type"] = "text"
            
            logger.info(f"Text search found {len(products)}/{total} products for query: '{query}' (page {page})")
            return {"results": products, "total": total}
            
        except Exception as e:
            logger.error(f"Error in paginated text search: {e}")
            return {"results": [], "total": 0}

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
            
            cursor = self.collection.aggregate(pipeline, allowDiskUse=True)
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

    async def search_products_vector_paginated(
        self, 
        vector: List[float], 
        page: int = 1, 
        page_size: int = 20, 
        *, 
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Search products using vector similarity with pagination and total count.
        
        Args:
            vector: Query embedding vector
            page: Page number (1-based)
            page_size: Number of results per page
            filters: Optional MongoDB filter document to enforce category/price/color
            
        Returns:
            Dictionary with results, total count, and pagination metadata
        """
        try:
            # For vector search, we need to oversample and then paginate
            # This is a compromise since we can't easily get exact total counts for vector search
            total_needed = page * page_size
            num_candidates = max(total_needed * 10, 500)
            prelimit = max(total_needed * 3, 100)
            
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
            
            # Use facet to get both results and count
            skip = (page - 1) * page_size
            pipeline.append({
                "$facet": {
                    "results": [
                        {"$sort": {"vector_score": -1}},
                        {"$skip": skip},
                        {"$limit": page_size}
                    ],
                    "total": [
                        {"$count": "count"}
                    ]
                }
            })
            
            cursor = self.collection.aggregate(pipeline, allowDiskUse=True)
            result = await cursor.to_list(length=1)
            
            if not result:
                return {"results": [], "total": 0}
                
            facet_result = result[0]
            products = facet_result.get("results", [])
            total_count = facet_result.get("total", [])
            total = total_count[0]["count"] if total_count else 0
            
            # Convert ObjectId to string and add search metadata
            for product in products:
                product["_id"] = str(product["_id"])
                product["search_type"] = "vector"
            
            logger.info(f"Vector search found {len(products)}/{total} products (page {page})")
            return {"results": products, "total": total}
            
        except Exception as e:
            logger.error(f"Error in paginated vector search: {e}")
            return {"results": [], "total": 0}

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

    async def search_products_hybrid_paginated(
        self, 
        query: str, 
        vector: List[float], 
        page: int = 1, 
        page_size: int = 20, 
        *, 
        filters: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Search products using hybrid text + vector search with pagination.
        
        Args:
            query: Search query string
            vector: Query embedding vector
            page: Page number (1-based)
            page_size: Number of results per page
            filters: Optional MongoDB filter document to enforce category/price/color
            
        Returns:
            Dictionary with results, total count, and pagination metadata
        """
        try:
            # Get larger samples from both searches to ensure good hybrid results
            sample_size = max(page * page_size * 3, 100)
            
            # Run both searches with filters applied
            text_data = await self.search_products_text_paginated(query, page=1, page_size=sample_size, filters=filters)
            vector_data = await self.search_products_vector_paginated(vector, page=1, page_size=sample_size, filters=filters)
            
            text_results = text_data.get("results", [])
            vector_results = vector_data.get("results", [])
            
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
            
            # Sort by combined score
            all_results = list(combined_results.values())
            all_results.sort(key=lambda x: x.get("search_score", 0.0), reverse=True)
            
            # Apply pagination
            total = len(all_results)
            skip = (page - 1) * page_size
            end = skip + page_size
            paginated_results = all_results[skip:end]
            
            logger.info(f"Hybrid search found {len(paginated_results)}/{total} products for query: '{query}' (page {page})")
            return {"results": paginated_results, "total": total}
            
        except Exception as e:
            logger.error(f"Error in paginated hybrid search: {e}")
            return {"results": [], "total": 0}

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
