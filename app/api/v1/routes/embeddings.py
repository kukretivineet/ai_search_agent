#!/usr/bin/env python3
"""
FastAPI routes for embedding operations.
"""

import asyncio
import logging
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, status
from app.api.v1.schemas import (
    EmbeddingGenerationRequest,
    EmbeddingGenerationResponse,
    EmbeddingStatsResponse,
    SingleEmbeddingRequest,
    SingleEmbeddingResponse,
    ErrorResponse
)
from app.services.embedding_service import EmbeddingService
from app.repositories.product_repository import ProductRepository
from app.db.mongo import AsyncMongoClient


router = APIRouter()
logger = logging.getLogger(__name__)


async def get_embedding_service() -> EmbeddingService:
    """Dependency to get embedding service."""
    mongo_client = AsyncMongoClient()
    await mongo_client.connect()
    database = mongo_client.get_database()
    product_repo = ProductRepository(database)
    return EmbeddingService(product_repo)


@router.post(
    "/generate",
    response_model=EmbeddingGenerationResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def generate_embeddings(
    request: EmbeddingGenerationRequest,
    background_tasks: BackgroundTasks,
    embedding_service: EmbeddingService = Depends(get_embedding_service)
):
    """
    Generate embeddings for products in batches.
    
    This endpoint starts the embedding generation process in the background
    and returns immediately with a status update.
    """
    try:
        def progress_callback(overall_stats: Dict[str, Any], batch_stats: Dict[str, Any]):
            """Callback for progress updates."""
            logger.info(f"✅ Batch progress: {batch_stats}")
        
        # Start embedding generation in background
        background_tasks.add_task(
            embedding_service.generate_embeddings_batch,
            batch_size=request.batch_size,
            progress_callback=progress_callback
        )
        
        return EmbeddingGenerationResponse(
            status="started",
            message=f"Embedding generation started with batch size {request.batch_size}",
            stats={}
        )
        
    except Exception as e:
        logger.error(f"Error starting embedding generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start embedding generation: {str(e)}"
        )


@router.post(
    "/generate/sync",
    response_model=EmbeddingGenerationResponse,
    responses={
        400: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def generate_embeddings_sync(
    request: EmbeddingGenerationRequest,
    embedding_service: EmbeddingService = Depends(get_embedding_service)
):
    """
    Generate embeddings for products synchronously.
    
    This endpoint processes embeddings and waits for completion before returning.
    Use for smaller batch sizes or when you need immediate results.
    """
    try:
        stats = await embedding_service.generate_embeddings_batch(
            batch_size=request.batch_size
        )
        
        return EmbeddingGenerationResponse(
            status="completed",
            message="Embedding generation completed successfully",
            stats=stats
        )
        
    except Exception as e:
        logger.error(f"Error in synchronous embedding generation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Embedding generation failed: {str(e)}"
        )


@router.get(
    "/stats",
    response_model=EmbeddingStatsResponse,
    responses={500: {"model": ErrorResponse}}
)
async def get_embedding_stats(
    embedding_service: EmbeddingService = Depends(get_embedding_service)
):
    """Get embedding generation statistics."""
    try:
        stats = await embedding_service.get_embedding_stats()
        
        return EmbeddingStatsResponse(**stats)
        
    except Exception as e:
        logger.error(f"Error getting embedding stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get embedding statistics: {str(e)}"
        )


@router.post(
    "/generate/single",
    response_model=SingleEmbeddingResponse,
    responses={
        400: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse}
    }
)
async def generate_single_embedding(
    request: SingleEmbeddingRequest,
    embedding_service: EmbeddingService = Depends(get_embedding_service)
):
    """Generate embedding for a single product."""
    try:
        embedding = await embedding_service.generate_single_embedding(request.product_id)
        
        if not embedding:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product not found or embedding generation failed: {request.product_id}"
            )
        
        return SingleEmbeddingResponse(
            status="success",
            message="Embedding generated successfully",
            product_id=request.product_id,
            embedding_dimensions=len(embedding.embedding_vector)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating single embedding: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate embedding: {str(e)}"
        )


@router.delete(
    "/clear",
    response_model=Dict[str, Any]
)
async def clear_embeddings(
    embedding_service: EmbeddingService = Depends(get_embedding_service)
):
    """
    Clear all embeddings from products.
    
    WARNING: This will remove all embedding data!
    """
    try:
        # This would be implemented in the repository
        # For now, return a placeholder response
        return {
            "status": "not_implemented",
            "message": "Clear embeddings functionality not yet implemented"
        }
        
    except Exception as e:
        logger.error(f"Error clearing embeddings: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear embeddings: {str(e)}"
        )
