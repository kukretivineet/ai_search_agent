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
from app.services.intent_service import LLMIntentService, LLMIntent
from app.core.config import Settings

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
        reranker_service: RerankerService,
        intent_service: Optional[LLMIntentService] = None,
        settings: Optional[Settings] = None
    ):
        """Initialize search service with injected dependencies.
        
        Args:
            product_repository: Product repository for data access
            domain_service: Domain service for business logic
            embedding_service: Service for generating embeddings
            reranker_service: Service for reranking results
            intent_service: Optional LLM-based intent service
            settings: Application settings
        """
        self.product_repository = product_repository
        self.search_domain_service = domain_service
        self.embedding_service = embedding_service
        self.reranker_service = reranker_service
        self.intent_service = intent_service
        self.settings = settings
        
        # Analytics
        self.search_analytics = {
            'total_searches': 0,
            'avg_response_time': 0.0,
            'search_types': {'text': 0, 'vector': 0, 'hybrid': 0}
        }
    
    async def initialize(self) -> None:
        """Initialize all services and repositories"""
        logger.info("SearchService initialized with injected dependencies")
    
    async def _parse_search_intent_with_llm_fallback(self, query: str) -> Dict[str, Any]:
        """Parse search intent using LLM with fallback to domain heuristics.
        
        Args:
            query: User's raw search query
            
        Returns:
            Parsed search intent dictionary compatible with domain service format
        """
        # Try LLM intent parsing first if available
        if (self.intent_service and 
            self.settings and 
            self.settings.llm_intent_enabled):
            try:
                llm_intent = await self.intent_service.parse_intent(query)
                if (llm_intent and 
                    llm_intent.confidence >= self.settings.llm_intent_confidence_threshold):
                    
                    # Convert LLM intent to domain service format
                    search_intent = self._convert_llm_intent_to_domain_intent(llm_intent, query)
                    logger.info(f"Using LLM intent (confidence: {llm_intent.confidence:.2f}): {search_intent}")
                    return search_intent
                else:
                    logger.info(f"LLM confidence too low ({llm_intent.confidence if llm_intent else 'None'}), falling back to heuristics")
            except Exception as e:
                logger.warning(f"LLM intent parsing failed, falling back to heuristics: {e}")
        
        # Fallback to domain service heuristics
        search_intent = self.search_domain_service.parse_search_intent(query)
        logger.info(f"Using heuristic intent: {search_intent}")
        return search_intent
    
    def _convert_llm_intent_to_domain_intent(self, llm_intent: LLMIntent, original_query: str) -> Dict[str, Any]:
        """Convert LLM intent format to domain service intent format.
        
        Args:
            llm_intent: Structured intent from LLM
            original_query: Original user query
            
        Returns:
            Intent dictionary compatible with domain service
        """
        # Convert budget to price constraints
        price_constraints = {}
        if llm_intent.budget_min is not None:
            price_constraints['above'] = llm_intent.budget_min
        if llm_intent.budget_max is not None:
            price_constraints['under'] = llm_intent.budget_max
        
        # Build filters from additional LLM data
        filters = {}
        if llm_intent.brands:
            filters['brands'] = llm_intent.brands
        if llm_intent.sizes:
            filters['sizes'] = llm_intent.sizes
        if llm_intent.gifting:
            filters['gifting'] = True
            filters['recipient'] = llm_intent.recipient
        if llm_intent.occasion:
            filters['occasion'] = llm_intent.occasion
        
        return {
            'original_query': original_query,
            'rephrased_query': llm_intent.rephrased_query,
            'normalized_query': llm_intent.rephrased_query.lower(),
            'categories': llm_intent.categories,
            'colors': llm_intent.colors,
            'price_constraints': price_constraints,
            'keywords': llm_intent.keywords,
            'filters': filters,
            'llm_enhanced': True,
            'confidence': llm_intent.confidence
        }
    
    async def search(
        self, 
        query: str, 
        mode: str = "hybrid",
        limit: int = 20,
        use_reranking: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Main search interface (backward compatibility)
        
        Args:
            query: Search query string
            mode: Search mode ('text', 'vector', 'hybrid')
            limit: Number of results to return
            use_reranking: Whether to apply reranking
        
        Returns:
            List of search results
        """
        # Use the paginated version internally for consistency
        result = await self.search_paginated(
            query=query,
            mode=mode,
            page=1,
            page_size=limit,
            use_reranking=use_reranking
        )
        return result.get("results", [])
    
    async def search_paginated(
        self, 
        query: str, 
        mode: str = "hybrid",
        page: int = 1,
        page_size: int = 20,
        use_reranking: bool = True
    ) -> Dict[str, Any]:
        """
        Main paginated search interface
        
        Args:
            query: Search query string
            mode: Search mode ('text', 'vector', 'hybrid')
            page: Page number (1-based)
            page_size: Number of results per page
            use_reranking: Whether to apply reranking
        
        Returns:
            Dictionary with results, total count, and pagination metadata
        """
        start_time = time.time()
        
        try:
            if not query or not query.strip():
                return {"results": [], "total": 0}
            
            # Parse search intent using LLM with fallback to heuristics
            search_intent = await self._parse_search_intent_with_llm_fallback(query)
            logger.info(f"Parsed search intent: {search_intent}")
            
            # Use rephrased query if available from LLM
            effective_query = search_intent.get('rephrased_query', query)
            
            # Execute search based on mode
            if mode == "text":
                search_data = await self._execute_text_search_paginated(effective_query, page, page_size, search_intent)
            elif mode == "vector":
                search_data = await self._execute_vector_search_paginated(effective_query, page, page_size, search_intent)
            elif mode == "hybrid":
                search_data = await self._execute_hybrid_search_paginated(effective_query, page, page_size, search_intent)
            else:
                raise ValueError(f"Unsupported search mode: {mode}")
            
            results = search_data.get("results", [])
            total = search_data.get("total", 0)
            
            # Apply reranking if requested and we have results
            if use_reranking and results and len(results) > 1:
                results = await self._apply_reranking(query, results)
                search_data["results"] = results
            
            # Update analytics
            execution_time = time.time() - start_time
            self._update_analytics(mode, execution_time)
            
            logger.info(f"Search completed: {len(results)}/{total} results in {execution_time:.3f}s (page {page})")
            return search_data
            
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise
    
    async def _execute_text_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Execute text-based search with strict filtering"""
        try:
            # Parse search intent first
            search_intent = self.search_domain_service.parse_search_intent(query)
            
            # Build strict MongoDB filters
            filters = self.search_domain_service.build_mongo_filters(search_intent, strict_color=False)
            
            # Build optimized text query using domain logic
            text_query_dict = self.search_domain_service.build_text_query(search_intent)
            
            # Extract the actual query string
            actual_query = text_query_dict.get("query", query)
            
            # Execute text search via repository with filters
            results = await self.product_repository.search_products_text(
                actual_query, limit, filters=filters if filters else None
            )
            
            logger.info(f"Text search found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Text search failed: {e}")
            return []
    
    async def _execute_text_search_paginated(self, query: str, page: int, page_size: int, search_intent: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute paginated text-based search with strict filtering"""
        try:
            # Use provided search intent or parse it
            if search_intent is None:
                search_intent = self.search_domain_service.parse_search_intent(query)
            
            # Build strict MongoDB filters
            filters = self.search_domain_service.build_mongo_filters(search_intent, strict_color=False)
            
            # Build optimized text query using domain logic
            text_query_dict = self.search_domain_service.build_text_query(search_intent)
            
            # Extract the actual query string
            actual_query = text_query_dict.get("query", query)
            
            # Execute paginated text search via repository with filters
            search_data = await self.product_repository.search_products_text_paginated(
                actual_query, page, page_size, filters=filters if filters else None
            )
            
            results = search_data.get("results", [])
            total = search_data.get("total", 0)
            
            logger.info(f"Text search found {len(results)}/{total} results (page {page})")
            return search_data
            
        except Exception as e:
            logger.error(f"Paginated text search failed: {e}")
            return {"results": [], "total": 0}
    
    async def _execute_vector_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Execute vector-based search with strict filtering"""
        try:
            # Parse search intent first
            search_intent = self.search_domain_service.parse_search_intent(query)
            
            # Build strict MongoDB filters
            filters = self.search_domain_service.build_mongo_filters(search_intent, strict_color=False)
            
            # Generate query embedding
            query_embedding = await self.embedding_service.generate_embedding(query)
            
            # Execute vector search via repository with filters
            results = await self.product_repository.search_products_vector(
                query_embedding, limit, filters=filters if filters else None
            )
            
            logger.info(f"Vector search found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            return []
    
    async def _execute_vector_search_paginated(self, query: str, page: int, page_size: int, search_intent: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute paginated vector-based search with strict filtering"""
        try:
            # Use provided search intent or parse it
            if search_intent is None:
                search_intent = self.search_domain_service.parse_search_intent(query)
            
            # Build strict MongoDB filters
            filters = self.search_domain_service.build_mongo_filters(search_intent, strict_color=False)
            
            # Generate query embedding
            query_embedding = await self.embedding_service.generate_embedding(query)
            
            # Execute paginated vector search via repository with filters
            search_data = await self.product_repository.search_products_vector_paginated(
                query_embedding, page, page_size, filters=filters if filters else None
            )
            
            results = search_data.get("results", [])
            total = search_data.get("total", 0)
            
            logger.info(f"Vector search found {len(results)}/{total} results (page {page})")
            return search_data
            
        except Exception as e:
            logger.error(f"Paginated vector search failed: {e}")
            return {"results": [], "total": 0}
    
    async def _execute_hybrid_search(self, query: str, limit: int) -> List[Dict[str, Any]]:
        """Execute hybrid search combining text and vector with strict filtering"""
        try:
            # Parse search intent first
            search_intent = self.search_domain_service.parse_search_intent(query)
            
            # Build strict MongoDB filters
            filters = self.search_domain_service.build_mongo_filters(search_intent, strict_color=False)
            
            # Generate query embedding
            query_embedding = await self.embedding_service.generate_embedding(query)
            
            # Build optimized text query
            text_query_dict = self.search_domain_service.build_text_query(search_intent)
            
            # Extract the actual query string
            actual_query = text_query_dict.get("query", query)
            
            # Execute hybrid search via repository with filters
            results = await self.product_repository.search_products_hybrid(
                actual_query, query_embedding, limit, filters=filters if filters else None
            )
            
            # Apply additional relevance scoring for color preference
            if search_intent.get('colors') and results:
                for result in results:
                    color_boost = self.search_domain_service.calculate_relevance_score(result, search_intent)
                    # Boost results that match colors
                    if color_boost > 0.5:  # High color relevance
                        result['search_score'] = result.get('search_score', 0.0) * 1.2
            
            # Re-sort by updated scores
            results.sort(key=lambda x: x.get("search_score", 0.0), reverse=True)
            
            logger.info(f"Hybrid search found {len(results)} results")
            return results
            
        except Exception as e:
            logger.error(f"Hybrid search failed: {e}")
            return []
    
    async def _execute_hybrid_search_paginated(self, query: str, page: int, page_size: int, search_intent: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute paginated hybrid search combining text and vector with strict filtering"""
        try:
            # Use provided search intent or parse it
            if search_intent is None:
                search_intent = self.search_domain_service.parse_search_intent(query)
            
            # Build strict MongoDB filters
            filters = self.search_domain_service.build_mongo_filters(search_intent, strict_color=False)
            
            # Generate query embedding
            query_embedding = await self.embedding_service.generate_embedding(query)
            
            # Build optimized text query
            text_query_dict = self.search_domain_service.build_text_query(search_intent)
            
            # Extract the actual query string
            actual_query = text_query_dict.get("query", query)
            
            # Execute paginated hybrid search via repository with filters
            search_data = await self.product_repository.search_products_hybrid_paginated(
                actual_query, query_embedding, page, page_size, filters=filters if filters else None
            )
            
            results = search_data.get("results", [])
            total = search_data.get("total", 0)
            
            # Apply additional relevance scoring for color preference
            if search_intent.get('colors') and results:
                for result in results:
                    color_boost = self.search_domain_service.calculate_relevance_score(result, search_intent)
                    # Boost results that match colors
                    if color_boost > 0.5:  # High color relevance
                        result['search_score'] = result.get('search_score', 0.0) * 1.2
                
                # Re-sort by updated scores
                results.sort(key=lambda x: x.get("search_score", 0.0), reverse=True)
                search_data["results"] = results
            
            logger.info(f"Hybrid search found {len(results)}/{total} results (page {page})")
            return search_data
            
        except Exception as e:
            logger.error(f"Paginated hybrid search failed: {e}")
            return {"results": [], "total": 0}
    
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
