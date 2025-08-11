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
        # Execute paginated search
        search_data = await search_service.search_paginated(
            query=request.query,
            mode=request.mode,
            page=request.page,
            page_size=request.limit,
            use_reranking=request.use_reranking
        )
        
        results = search_data.get("results", [])
        total = search_data.get("total", 0)
        
        # Calculate pagination metadata using domain service
        from app.domain.search.services import SearchDomainService
        domain_service = SearchDomainService()
        
        pagination_info = domain_service.calculate_pagination(
            page=request.page,
            page_size=request.limit,
            total=total
        )
        
        # Convert to response format
        product_results = [
            ProductResult(**product) for product in results
        ]
        
        execution_time = time.time() - start_time
        
        return SearchResponse(
            results=product_results,
            total=total,
            returned=pagination_info["returned"],
            query=request.query,
            mode=request.mode,
            execution_time=execution_time,
            reranked=request.use_reranking and len(results) > 0,
            page=pagination_info["page"],
            total_pages=pagination_info["total_pages"],
            has_next=pagination_info["has_next"],
            has_prev=pagination_info["has_prev"]
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
