"""
Search API endpoints - REST API layer
"""

import logging
import time
import math
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any

from app.api.v1.schemas.search import SearchRequest, SearchResponse, ProductResult
from app.api.v1.deps import get_search_service, get_product_repository
from app.services.search_service import SearchService
from app.repositories.product_repository import ProductRepository


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=SearchResponse)
async def search_products(
    request: SearchRequest,
    search_service: SearchService = Depends(get_search_service)
) -> SearchResponse:
    """Search products using text, vector, or hybrid search.
    
    Args:
        request: Search request parameters
        search_service: Injected search service
        
    Returns:
        Search response with results and metadata
    """
    start_time = time.time()
    
    try:
        # Execute search
        results = await search_service.search(
            query=request.query,
            mode=request.mode,
            limit=request.limit,
            use_reranking=request.use_reranking
        )
        
        # Calculate pagination
        total = len(results)
        page_size = request.limit
        total_pages = math.ceil(total / page_size) if total > 0 else 1
        
        # Apply pagination
        start_idx = (request.page - 1) * page_size
        end_idx = start_idx + page_size
        paginated_results = results[start_idx:end_idx]
        
        # Convert to response format
        product_results = [
            ProductResult(**product) for product in paginated_results
        ]
        
        execution_time = time.time() - start_time
        
        return SearchResponse(
            results=product_results,
            total=total,
            returned=len(product_results),
            query=request.query,
            mode=request.mode,
            execution_time=execution_time,
            reranked=request.use_reranking and len(results) > 0,
            page=request.page,
            total_pages=total_pages,
            has_next=request.page < total_pages,
            has_prev=request.page > 1
        )
        
    except Exception as e:
        logger.error(f"Search failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Search operation failed: {str(e)}"
        )


@router.get("/stats")
async def get_search_stats(
    product_repo: ProductRepository = Depends(get_product_repository)
) -> Dict[str, Any]:
    """Get search system statistics.
    
    Args:
        product_repo: Injected product repository
        
    Returns:
        Statistics about the search system
    """
    try:
        total_products = await product_repo.get_product_count()
        health_info = await product_repo.health_check()
        
        return {
            "total_products": total_products,
            "database_status": health_info["status"],
            "available_indexes": health_info.get("indexes", []),
            "search_modes": ["text", "vector", "hybrid"],
            "features": {
                "text_search": True,
                "vector_search": True,
                "hybrid_search": True,
                "reranking": True
            }
        }
        
    except Exception as e:
        logger.error(f"Stats retrieval failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve stats: {str(e)}"
        )


@router.get("/health")
async def health_check(
    search_service: SearchService = Depends(get_search_service)
) -> Dict[str, Any]:
    """Health check endpoint for the search system.
    
    Args:
        search_service: Injected search service
        
    Returns:
        Health status of all search components
    """
    try:
        # Perform health checks on all components
        repo_health = await search_service.product_repository.health_check()
        
        # Test a simple search to ensure everything is working
        test_results = await search_service.search("test", mode="text", limit=1)
        
        return {
            "status": "healthy",
            "components": {
                "database": repo_health["status"],
                "search_service": "healthy" if search_service else "unhealthy",
                "embedding_service": "healthy",  # TODO: Add proper health check
                "reranker_service": "healthy"    # TODO: Add proper health check
            },
            "capabilities": {
                "text_search": True,
                "vector_search": True,
                "hybrid_search": True,
                "reranking": True
            },
            "test_search_functional": len(test_results) >= 0  # Even 0 results means it's working
        }
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {
            "status": "unhealthy",
            "error": str(e),
            "components": {
                "database": "unknown",
                "search_service": "unhealthy"
            }
        }

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
import logging

from api.v1.schemas.search import SearchRequest, SearchResponse
from services.search_service import SearchService
from core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()

# Dependency to get search service
async def get_search_service() -> SearchService:
    """Get search service instance"""
    # This would typically be injected via dependency container
    # For now, create a simple instance
    search_service = SearchService()
    if not hasattr(search_service, '_initialized'):
        await search_service.initialize()
        search_service._initialized = True
    return search_service


@router.post("/search", response_model=SearchResponse, summary="Search Products")
async def search_products(
    request: SearchRequest,
    search_service: SearchService = Depends(get_search_service)
) -> SearchResponse:
    """
    Search products using text, vector, or hybrid search modes.
    
    - **query**: Search query string (required)
    - **mode**: Search mode - 'text', 'vector', or 'hybrid' (default: 'hybrid')
    - **limit**: Number of results to return (default: 20, max: 100)
    - **page**: Page number for pagination (default: 1)
    - **use_reranking**: Whether to apply Cohere reranking (default: true)
    """
    try:
        # Validate request
        if not request.query or not request.query.strip():
            raise HTTPException(status_code=400, detail="Query cannot be empty")
        
        if request.limit > 100:
            raise HTTPException(status_code=400, detail="Limit cannot exceed 100")
        
        if request.page < 1:
            raise HTTPException(status_code=400, detail="Page must be >= 1")
        
        # Execute search
        result = await search_service.search(
            query=request.query.strip(),
            mode=request.mode,
            limit=request.limit,
            page=request.page,
            use_reranking=request.use_reranking
        )
        
        # Handle search errors
        if 'error' in result:
            logger.error(f"Search error for query '{request.query}': {result['error']}")
            raise HTTPException(status_code=500, detail=f"Search failed: {result['error']}")
        
        # Convert to response model
        response = SearchResponse(
            results=result['results'],
            total=result['total'],
            returned=len(result['results']),
            query=result['query'],
            mode=result['mode'],
            execution_time=result['execution_time'],
            reranked=result.get('reranked', False),
            page=result.get('page', request.page),
            total_pages=result.get('total_pages', 1),
            has_next=result.get('has_next', False),
            has_prev=result.get('has_prev', False)
        )
        
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in search endpoint: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/search/stats", summary="Get Search Statistics")
async def get_search_stats(
    search_service: SearchService = Depends(get_search_service)
) -> dict:
    """Get search analytics and database statistics."""
    try:
        # Get search analytics
        analytics = search_service.get_analytics()
        
        # Get database stats
        db_stats = await search_service.get_database_stats()
        
        return {
            "search_analytics": analytics,
            "database_stats": db_stats,
            "service_info": {
                "version": "2.0.0",
                "features": {
                    "text_search": True,
                    "vector_search": bool(settings.OPENAI_API_KEY),
                    "hybrid_search": bool(settings.OPENAI_API_KEY),
                    "reranking": bool(settings.COHERE_API_KEY)
                }
            }
        }
        
    except Exception as e:
        logger.error(f"Error getting search stats: {e}")
        raise HTTPException(status_code=500, detail="Failed to get search statistics")


@router.get("/search/health", summary="Search Service Health Check")
async def search_health_check() -> dict:
    """Health check for search service and dependencies."""
    health_status = {
        "status": "healthy",
        "service": "search-api",
        "version": "2.0.0",
        "dependencies": {
            "mongodb": "unknown",
            "openai": bool(settings.OPENAI_API_KEY),
            "cohere": bool(settings.COHERE_API_KEY)
        }
    }
    
    try:
        # Test search service
        search_service = await get_search_service()
        
        # Test database connection by getting stats
        db_stats = await search_service.get_database_stats()
        
        if 'error' in db_stats:
            health_status["dependencies"]["mongodb"] = "error"
            health_status["status"] = "degraded"
        else:
            health_status["dependencies"]["mongodb"] = "healthy"
            health_status["database_info"] = {
                "total_documents": db_stats.get("total_documents", 0),
                "embedding_coverage": db_stats.get("embedding_coverage", "0%")
            }
        
        return health_status
        
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        health_status["status"] = "unhealthy"
        health_status["error"] = str(e)
        return health_status
