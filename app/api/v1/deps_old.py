#!/usr/bin/env python3
"""
Dependencies for FastAPI routes.
"""

from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from app.core.config import Settings, get_settings
from app.db.mongo import AsyncMongoClient
from app.repositories.product_repository import ProductRepository
from app.services.embedding_service import EmbeddingService


async def get_database() -> AsyncIOMotorDatabase:
    """
    Get database dependency.
    
    Returns:
        AsyncIOMotorDatabase instance
    """
    mongo_client = AsyncMongoClient()
    try:
        await mongo_client.connect()
        return mongo_client.get_database()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database connection failed: {str(e)}"
        )


async def get_product_repository(
    database: AsyncIOMotorDatabase = Depends(get_database)
) -> ProductRepository:
    """
    Get product repository dependency.
    
    Args:
        database: Database instance
        
    Returns:
        ProductRepository instance
    """
    return ProductRepository(database)


async def get_embedding_service(
    product_repo: ProductRepository = Depends(get_product_repository)
) -> EmbeddingService:
    """
    Get embedding service dependency.
    
    Args:
        product_repo: Product repository instance
        
    Returns:
        EmbeddingService instance
    """
    return EmbeddingService(product_repo)


def get_settings_dependency() -> Settings:
    """Get settings dependency."""
    return get_settings()
