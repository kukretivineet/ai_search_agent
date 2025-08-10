#!/usr/bin/env python3
"""
Pydantic schemas for API request/response models.
"""

from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class EmbeddingGenerationRequest(BaseModel):
    """Request model for embedding generation."""
    
    batch_size: int = Field(
        default=1000,
        description="Number of products to process per batch",
        ge=1,
        le=5000
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "batch_size": 1000
            }
        }


class EmbeddingGenerationResponse(BaseModel):
    """Response model for embedding generation."""
    
    status: str = Field(description="Operation status")
    message: str = Field(description="Human readable message")
    stats: Dict[str, Any] = Field(description="Processing statistics")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Embedding generation completed",
                "stats": {
                    "total_processed": 1000,
                    "total_updated": 950,
                    "total_errors": 50,
                    "batches_processed": 1
                }
            }
        }


class EmbeddingStatsResponse(BaseModel):
    """Response model for embedding statistics."""
    
    total_products: int = Field(description="Total number of products")
    with_embeddings: int = Field(description="Products with embeddings")
    without_embeddings: int = Field(description="Products without embeddings")
    completion_percentage: float = Field(description="Completion percentage")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_products": 50000,
                "with_embeddings": 35000,
                "without_embeddings": 15000,
                "completion_percentage": 70.0
            }
        }


class SingleEmbeddingRequest(BaseModel):
    """Request model for single embedding generation."""
    
    product_id: str = Field(
        description="Product ID to generate embedding for",
        min_length=24,
        max_length=24
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "product_id": "507f1f77bcf86cd799439011"
            }
        }


class SingleEmbeddingResponse(BaseModel):
    """Response model for single embedding generation."""
    
    status: str = Field(description="Operation status")
    message: str = Field(description="Human readable message")
    product_id: str = Field(description="Product ID processed")
    embedding_dimensions: Optional[int] = Field(
        description="Number of dimensions in embedding vector"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "message": "Embedding generated successfully",
                "product_id": "507f1f77bcf86cd799439011",
                "embedding_dimensions": 1536
            }
        }


class ProgressUpdate(BaseModel):
    """Model for progress updates during embedding generation."""
    
    timestamp: datetime = Field(description="Update timestamp")
    processed: int = Field(description="Number of products processed so far")
    total: int = Field(description="Total number of products to process")
    batch_number: int = Field(description="Current batch number")
    percentage: float = Field(description="Completion percentage")
    
    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2024-01-01T12:00:00Z",
                "processed": 1500,
                "total": 50000,
                "batch_number": 2,
                "percentage": 3.0
            }
        }


class ErrorResponse(BaseModel):
    """Standard error response model."""
    
    error: str = Field(description="Error type")
    message: str = Field(description="Error message")
    details: Optional[Dict[str, Any]] = Field(description="Additional error details")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid product ID format",
                "details": {
                    "field": "product_id",
                    "value": "invalid_id"
                }
            }
        }
