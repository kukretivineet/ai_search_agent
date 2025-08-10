"""
Reranker Service - Application Layer
Handles document reranking using Cohere API
"""

import logging
from typing import List, Dict, Any, Optional
import asyncio

logger = logging.getLogger(__name__)


class RerankerService:
    """Service for reranking search results using Cohere"""
    
    def __init__(self, api_key: str):
        """Initialize reranker service.
        
        Args:
            api_key: Cohere API key
        """
        self.api_key = api_key
        self.cohere_client = None
        self.is_available = False
        
        # Initialize client immediately if we have API key
        if api_key:
            self._initialize_client()
    
    def _initialize_client(self) -> None:
        """Initialize Cohere client"""
        try:
            import cohere
            self.cohere_client = cohere.AsyncClient(api_key=self.api_key)
            self.is_available = True
            
            logger.info("Cohere reranker service initialized successfully")
            
        except ImportError:
            logger.warning("Cohere package not available, reranking disabled")
        except Exception as e:
            logger.error(f"Failed to initialize Cohere client: {e}")
    
    async def initialize(self) -> None:
        """Initialize method for compatibility (already done in constructor)"""
        if not self.is_available and self.api_key:
            self._initialize_client()
    
    async def rerank(
        self, 
        query: str, 
        documents: List[Dict[str, Any]], 
        top_n: Optional[int] = None,
        model: str = "rerank-english-v3.0"
    ) -> Optional[List[Dict[str, Any]]]:
        """
        Rerank documents using Cohere rerank API
        
        Args:
            query: The search query
            documents: List of documents to rerank
            top_n: Number of top results to return
            model: Cohere rerank model to use
            
        Returns:
            Reranked documents or None if reranking fails
        """
        if not self.is_available or not self.cohere_client:
            logger.debug("Cohere reranker not available")
            return None
        
        if not documents:
            return []
        
        try:
            # Prepare documents for reranking
            docs_for_rerank = []
            for doc in documents:
                # Create text representation of document
                doc_text = self._create_document_text(doc)
                docs_for_rerank.append(doc_text)
            
            # Call Cohere rerank API
            response = await self.cohere_client.rerank(
                model=model,
                query=query,
                documents=docs_for_rerank,
                top_n=top_n or len(documents)
            )
            
            # Reorder original documents based on rerank results
            reranked_docs = []
            for result in response.results:
                original_doc = documents[result.index].copy()
                original_doc['relevance_score'] = result.relevance_score
                reranked_docs.append(original_doc)
            
            logger.info(f"Successfully reranked {len(reranked_docs)} documents")
            return reranked_docs
            
        except Exception as e:
            logger.error(f"Reranking failed: {e}")
            return None
    
    def _create_document_text(self, doc: Dict[str, Any]) -> str:
        """Create text representation of document for reranking"""
        parts = []
        
        # Title
        if doc.get('title'):
            parts.append(f"Title: {doc['title']}")
        
        # Brand
        if doc.get('brand'):
            parts.append(f"Brand: {doc['brand']}")
        
        # Category
        if doc.get('category'):
            parts.append(f"Category: {doc['category']}")
        
        # Description
        if doc.get('description'):
            # Truncate long descriptions
            description = doc['description'][:200] + "..." if len(doc['description']) > 200 else doc['description']
            parts.append(f"Description: {description}")
        
        # Price
        if doc.get('selling_price_numeric'):
            parts.append(f"Price: ₹{doc['selling_price_numeric']}")
        
        return " | ".join(parts)
    
    async def close(self):
        """Close reranker service"""
        try:
            if self.cohere_client:
                await self.cohere_client.close()
                logger.info("Cohere client closed")
        except Exception as e:
            logger.error(f"Error closing Cohere client: {e}")
