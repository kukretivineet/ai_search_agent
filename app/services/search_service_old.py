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
            
            # Initialize reranker service
            if settings.COHERE_API_KEY:
                self.reranker_service = RerankerService()
                await self.reranker_service.initialize()
            
            logger.info("Search service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize search service: {e}")
            raise
    
    async def search(
        self, 
        query: str, 
        mode: str = "hybrid",
        limit: int = 20, 
        page: int = 1,
        use_reranking: bool = True
    ) -> Dict[str, Any]:
        """
        Main search interface
        
        Args:
            query: Search query string
            mode: Search mode ('text', 'vector', 'hybrid')
            limit: Number of results to return
            page: Page number for pagination
            use_reranking: Whether to apply reranking
        
        Returns:
            Search results with metadata
        """
        start_time = time.time()
        
        try:
            if not query or not query.strip():
                return {
                    'results': [],
                    'total': 0,
                    'query': query,
                    'mode': mode,
                    'execution_time': 0.0,
                    'error': 'Empty query'
                }
            
            # Parse search intent
            search_intent = self.search_domain_service.parse_search_intent(query)
            
            # Execute search based on mode
            if mode == "text":
                results = await self._execute_text_search(search_intent, limit, page)
            elif mode == "vector":
                results = await self._execute_vector_search(search_intent, limit, page)
            elif mode == "hybrid":
                results = await self._execute_hybrid_search(search_intent, limit, page)
            else:
                raise ValueError(f"Invalid search mode: {mode}")
            
            # Apply reranking if enabled and available
            if use_reranking and self.reranker_service and results['results']:
                try:
                    reranked_results = await self.reranker_service.rerank(
                        query=query,
                        documents=results['results'],
                        top_n=limit
                    )
                    if reranked_results:
                        results['results'] = reranked_results
                        results['reranked'] = True
                except Exception as e:
                    logger.warning(f"Reranking failed: {e}")
                    results['reranked'] = False
            else:
                results['reranked'] = False
            
            # Calculate execution time
            execution_time = time.time() - start_time
            results['execution_time'] = execution_time
            
            # Update analytics
            self._update_analytics(mode, execution_time, len(results['results']))
            
            logger.info(f"Search completed: '{query}' -> {len(results['results'])} results in {execution_time:.3f}s")
            
            return results
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            return {
                'results': [],
                'total': 0,
                'query': query,
                'mode': mode,
                'execution_time': time.time() - start_time,
                'error': str(e)
            }
    
    async def _execute_text_search(
        self, 
        search_intent: Dict[str, Any], 
        limit: int, 
        page: int
    ) -> Dict[str, Any]:
        """Execute text-based search with pagination"""
        
        # Build MongoDB query from intent
        mongo_query = self.search_domain_service.build_text_query(search_intent)
        
        # Get total count for pagination
        total_count = await self.product_repository.count_documents(mongo_query)
        
        # Calculate skip for pagination
        skip = (page - 1) * limit
        
        # Execute search
        results = await self.product_repository.find_products(
            query=mongo_query,
            limit=limit,
            skip=skip
        )
        
        return {
            'results': results,
            'total': total_count,
            'query': search_intent['original_query'],
            'mode': 'text',
            'page': page,
            'total_pages': (total_count + limit - 1) // limit,
            'has_next': page * limit < total_count,
            'has_prev': page > 1
        }
    
    async def _execute_vector_search(
        self, 
        search_intent: Dict[str, Any], 
        limit: int, 
        page: int
    ) -> Dict[str, Any]:
        """Execute vector-based semantic search"""
        
        if not self.embedding_service:
            raise ValueError("Vector search not available - OpenAI API key missing")
        
        # Get query embedding
        query_embedding = await self.embedding_service.get_embedding(
            search_intent['original_query']
        )
        
        # Execute vector search
        results = await self.product_repository.vector_search(
            embedding=query_embedding,
            limit=limit
        )
        
        return {
            'results': results,
            'total': len(results),
            'query': search_intent['original_query'],
            'mode': 'vector',
            'page': page,
            'total_pages': 1,
            'has_next': False,
            'has_prev': False
        }
    
    async def _execute_hybrid_search(
        self, 
        search_intent: Dict[str, Any], 
        limit: int, 
        page: int,
        vector_weight: float = 0.6
    ) -> Dict[str, Any]:
        """Execute hybrid search combining text and vector search"""
        
        # Get vector results
        vector_results = []
        if self.embedding_service:
            try:
                query_embedding = await self.embedding_service.get_embedding(
                    search_intent['original_query']
                )
                vector_results = await self.product_repository.vector_search(
                    embedding=query_embedding,
                    limit=limit
                )
            except Exception as e:
                logger.warning(f"Vector search failed in hybrid mode: {e}")
        
        # Get text results
        mongo_query = self.search_domain_service.build_text_query(search_intent)
        text_results = await self.product_repository.find_products(
            query=mongo_query,
            limit=limit,
            skip=0  # No pagination for hybrid search
        )
        
        # Combine and deduplicate results
        combined_results = []
        seen_ids = set()
        
        # Add vector results with weighted scores
        for i, result in enumerate(vector_results):
            result_id = str(result.get('_id'))
            if result_id not in seen_ids:
                result['search_score'] = result.get('vector_score', 0) * vector_weight
                result['search_type'] = 'vector'
                combined_results.append(result)
                seen_ids.add(result_id)
        
        # Add text results with weighted scores
        text_weight = 1.0 - vector_weight
        for i, result in enumerate(text_results):
            result_id = str(result.get('_id'))
            if result_id not in seen_ids:
                # Simple relevance scoring for text results
                result['search_score'] = (1.0 - (i / max(len(text_results), 1))) * text_weight
                result['search_type'] = 'text'
                combined_results.append(result)
                seen_ids.add(result_id)
        
        # Sort by combined score and limit
        combined_results.sort(key=lambda x: x.get('search_score', 0), reverse=True)
        final_results = combined_results[:limit]
        
        return {
            'results': final_results,
            'total': len(combined_results),
            'query': search_intent['original_query'],
            'mode': 'hybrid',
            'page': page,
            'total_pages': 1,
            'has_next': False,
            'has_prev': False
        }
    
    def _update_analytics(self, mode: str, execution_time: float, result_count: int):
        """Update search analytics"""
        self.search_analytics['total_searches'] += 1
        self.search_analytics['search_types'][mode] += 1
        
        # Update average response time
        current_avg = self.search_analytics['avg_response_time']
        total_searches = self.search_analytics['total_searches']
        self.search_analytics['avg_response_time'] = (
            (current_avg * (total_searches - 1) + execution_time) / total_searches
        )
    
    async def get_database_stats(self) -> Dict[str, Any]:
        """Get database statistics"""
        if not self.product_repository:
            return {'error': 'Repository not initialized'}
        
        return await self.product_repository.get_stats()
    
    def get_analytics(self) -> Dict[str, Any]:
        """Get search analytics"""
        return self.search_analytics.copy()
    
    async def close(self):
        """Close all services"""
        try:
            if self.embedding_service:
                await self.embedding_service.close()
            if self.reranker_service:
                await self.reranker_service.close()
            logger.info("Search service closed successfully")
        except Exception as e:
            logger.error(f"Error closing search service: {e}")
