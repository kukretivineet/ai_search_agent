"""
Search Service - Application Layer
Orchestrates search operations using domain services and repositories
"""

import logging
from typing import Dict, List, Any, Optional
import time

from app.repositories.product_repository import ProductRepository
from app.domain.search.services import SearchDomainService
from app.services.simple_embedding_service import SimpleEmbeddingService
from app.services.reranker_service import RerankerService

logger = logging.getLogger(__name__)


class SearchService:
    """
    Application service for coordinating search operations
    Follows DDD patterns - orchestrates domain services and repositories
    """
    
    def __init__(
        self,
        product_repository: ProductRepository,
        domain_service: SearchDomainService,
        embedding_service: SimpleEmbeddingService,
        reranker_service: RerankerService
    ):
        """Initialize search service with injected dependencies.
        
        Args:
            product_repository: Product repository for data access
            domain_service: Domain service for business logic
            embedding_service: Service for generating embeddings
            reranker_service: Service for reranking results
        """
        self.product_repository = product_repository
        self.search_domain_service = domain_service
        self.embedding_service = embedding_service
        self.reranker_service = reranker_service
        
        # Analytics
        self.search_analytics = {
            'total_searches': 0,
            'avg_response_time': 0.0,
            'search_types': {'text': 0, 'vector': 0, 'hybrid': 0}
        }
    
    async def initialize(self) -> None:
        """Initialize all services and repositories"""
        logger.info("SearchService initialized with injected dependencies")
    
    async def search(
        self, 
        query: str, 
        mode: str = "hybrid",
        limit: int = 20,
        use_reranking: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Main search interface
        
        Args:
            query: Search query string
            mode: Search mode ('text', 'vector', 'hybrid')
            limit: Number of results to return
            use_reranking: Whether to apply reranking
        
        Returns:
            List of search results
        """
        start_time = time.time()
        
        try:
            if not query or not query.strip():
                return []
            
            # Parse search intent using domain service
            search_intent = self.search_domain_service.parse_search_intent(query)
            logger.info(f"Parsed search intent: {search_intent}")
            
            # Execute search based on mode
            if mode == "text":
                results = await self._execute_text_search(query, limit)
            elif mode == "vector":
                results = await self._execute_vector_search(query, limit)
            elif mode == "hybrid":
                results = await self._execute_hybrid_search(query, limit)
            else:
                raise ValueError(f"Unsupported search mode: {mode}")
            
            # Apply reranking if requested and we have results
            if use_reranking and results and len(results) > 1:
                results = await self._apply_reranking(query, results)
            
            # Update analytics
            execution_time = time.time() - start_time
            self._update_analytics(mode, execution_time)
            
            logger.info(f"Search completed: {len(results)} results in {execution_time:.3f}s")
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise
    
    async def _execute_text_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Execute text-based search"""
        try:
            # Parse search intent first
            search_intent = self.search_domain_service.parse_search_intent(query)
            
            # Build optimized text query using domain logic
            text_query_dict = self.search_domain_service.build_text_query(search_intent)
            
            # Extract the actual query string
            actual_query = text_query_dict.get("query", query)
            
            # Execute text search via repository
            results = await self.product_repository.search_products_text(actual_query, limit)
            
            logger.info(f"Text search found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Text search failed: {e}")
            return []
    
    async def _execute_vector_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Execute vector-based search"""
        try:
            # Generate query embedding
            query_embedding = await self.embedding_service.generate_embedding(query)
            
            # Execute vector search via repository
            results = await self.product_repository.search_products_vector(query_embedding, limit)
            
            logger.info(f"Vector search found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []
    
    async def _execute_hybrid_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Execute hybrid search combining text and vector"""
        try:
            # Generate query embedding
            query_embedding = await self.embedding_service.generate_embedding(query)
            
            # Parse search intent first
            search_intent = self.search_domain_service.parse_search_intent(query)
            
            # Build optimized text query
            text_query_dict = self.search_domain_service.build_text_query(search_intent)
            
            # Extract the actual query string
            actual_query = text_query_dict.get("query", query)
            
            # Execute hybrid search via repository
            results = await self.product_repository.search_products_hybrid(actual_query, query_embedding, limit)
            
            logger.info(f"Hybrid search found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Hybrid search failed: {e}")
            return []
    
    async def _apply_reranking(self, query: str, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Apply Cohere reranking to results"""
        try:
            if not results:
                return results
            
            # Apply reranking
            reranked_results = await self.reranker_service.rerank(query, results)
            
            # Handle case where reranking returns None
            if reranked_results is None:
                logger.warning("Reranking returned None, using original results")
                return results
            
            logger.info(f"Reranking applied to {len(results)} results")
            return reranked_results
            
        except Exception as e:
            logger.error(f"Reranking failed: {e}")
            # Return original results if reranking fails
            return results
    
    def _update_analytics(self, mode: str, execution_time: float):
        """Update search analytics"""
        self.search_analytics['total_searches'] += 1
        
        # Update average response time
        total = self.search_analytics['total_searches']
        current_avg = self.search_analytics['avg_response_time']
        self.search_analytics['avg_response_time'] = (
            (current_avg * (total - 1) + execution_time) / total
        )
        
        # Update mode counts
        if mode in self.search_analytics['search_types']:
            self.search_analytics['search_types'][mode] += 1
    
    async def get_stats(self) -> Dict[str, Any]:
        """Get search service statistics"""
        try:
            # Get repository stats
            repo_stats = await self.product_repository.health_check()
            
            # Combine with search analytics
            return {
                "repository_stats": repo_stats,
                "search_analytics": self.search_analytics,
                "service_status": "healthy"
            }
            
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {
                "service_status": "unhealthy",
                "error": str(e),
                "search_analytics": self.search_analytics
            }
