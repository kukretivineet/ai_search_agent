"""
Dependency injection for DDD services and repositories.
"""

import logging
from typing import AsyncGenerator, Optional
from fastapi import Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorCollection

from app.core.config import get_settings, Settings
from app.db.mongo import AsyncMongoClient
from app.repositories.product_repository import ProductRepository
from app.services.simple_embedding_service import SimpleEmbeddingService
from app.services.search_service import SearchService
from app.services.reranker_service import RerankerService
from app.services.intent_service import LLMIntentService
from app.domain.search.services import SearchDomainService


# Configure logger
logger = logging.getLogger(__name__)


async def get_database() -> AsyncIOMotorDatabase:
    """Get database dependency.
    
    Returns:
        AsyncIOMotorDatabase instance
    """
    settings = get_settings()
    mongo_client = AsyncMongoClient()
    try:
        await mongo_client.connect()
        return mongo_client.get_database()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}"
        )


async def get_product_collection(
    database: AsyncIOMotorDatabase = Depends(get_database)
) -> AsyncIOMotorCollection:
    """Get the product collection from MongoDB.
    
    Args:
        database: Database instance
        
    Returns:
        MongoDB collection for products
    """
    return database.products


async def get_product_repository(
    collection: AsyncIOMotorCollection = Depends(get_product_collection)
) -> ProductRepository:
    """Get product repository instance.
    
    Args:
        collection: MongoDB collection
        
    Returns:
        ProductRepository instance
    """
    return ProductRepository(collection)


async def get_embedding_service(
    settings: Settings = Depends(get_settings)
) -> SimpleEmbeddingService:
    """Get embedding service instance.
    
    Args:
        settings: Application settings
        
    Returns:
        EmbeddingService instance
    """
    return SimpleEmbeddingService(
        api_key=settings.openai_api_key,
        model=settings.embedding_model
    )


async def get_reranker_service(
    settings: Settings = Depends(get_settings)
) -> RerankerService:
    """Get reranker service instance.
    
    Args:
        settings: Application settings
        
    Returns:
        RerankerService instance
    """
    api_key = settings.cohere_api_key or ""
    return RerankerService(api_key=api_key)


async def get_search_domain_service() -> SearchDomainService:
    """Get search domain service instance.
    
    Returns:
        SearchDomainService instance
    """
    return SearchDomainService()


async def get_intent_service(
    settings: Settings = Depends(get_settings)
) -> Optional[LLMIntentService]:
    """Get LLM intent service instance.
    
    Args:
        settings: Application settings
        
    Returns:
        LLMIntentService instance or None if disabled
    """
    if not settings.llm_intent_enabled:
        return None
    
    return LLMIntentService(
        api_key=settings.openai_api_key,
        model=settings.llm_intent_model
    )


async def get_search_service(
    product_repo: ProductRepository = Depends(get_product_repository),
    embedding_service: SimpleEmbeddingService = Depends(get_embedding_service),
    reranker_service: RerankerService = Depends(get_reranker_service),
    domain_service: SearchDomainService = Depends(get_search_domain_service),
    intent_service: Optional[LLMIntentService] = Depends(get_intent_service),
    settings: Settings = Depends(get_settings)
) -> SearchService:
    """Get search service instance with all dependencies injected.
    
    Args:
        product_repo: Product repository
        embedding_service: Embedding service
        reranker_service: Reranker service
        domain_service: Search domain service
        
    Returns:
        SearchService instance
    """
    search_service = SearchService(
        product_repository=product_repo,
        domain_service=domain_service,
        embedding_service=embedding_service,
        reranker_service=reranker_service,
        intent_service=intent_service,
        settings=settings
    )
    
    await search_service.initialize()
    return search_service


def get_settings_dependency() -> Settings:
    """Get settings dependency."""
    return get_settings()
