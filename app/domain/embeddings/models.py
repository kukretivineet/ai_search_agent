#!/usr/bin/env python3
"""
Domain models for embeddings.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, validator


class EmbeddingText(BaseModel):
    """Value object for structured embedding text."""
    
    title: str
    brand: Optional[str] = None
    category: str
    attributes: Dict[str, Any] = Field(default_factory=dict)
    price_inr: Optional[float] = None
    description: str
    
    def to_structured_text(self) -> str:
        """Convert to structured embedding text format."""
        parts = [self.title]
        
        if self.brand:
            parts.append(f"brand:{self.brand.lower()}")
        
        parts.append(f"category:{self.category.lower()}")
        
        # Add attributes
        for key, value in self.attributes.items():
            if value:
                parts.append(f"{key}:{str(value).lower()}")
        
        if self.price_inr:
            parts.append(f"price_inr:{self.price_inr}")
        
        if self.description:
            # Truncate description if too long
            desc = self.description[:200] + "..." if len(self.description) > 200 else self.description
            parts.append(f"desc:{desc}")
        
        return " | ".join(parts)


class ProductEmbedding(BaseModel):
    """Domain entity for product embeddings."""
    
    id: str = Field(..., alias="_id")
    embedding_text: Optional[str] = None
    embedding_vector: Optional[List[float]] = None
    embedding_model: Optional[str] = None
    embedding_updated_at: Optional[datetime] = None
    
    # Original product data
    title: str
    brand: Optional[str] = None
    category: str
    sub_category: Optional[str] = None
    description: str
    selling_price: Optional[float] = None
    actual_price: Optional[float] = None
    product_details: List[Dict[str, Any]] = Field(default_factory=list)
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
    
    @property
    def has_embedding(self) -> bool:
        """Check if product has embedding."""
        return bool(self.embedding_text and self.embedding_vector)
    
    @property
    def embedding_dimension(self) -> int:
        """Get embedding dimension."""
        return len(self.embedding_vector) if self.embedding_vector else 0
    
    def needs_embedding_update(self, new_text: str) -> bool:
        """Check if embedding needs update."""
        return self.embedding_text != new_text or not self.embedding_vector


class EmbeddingGenerationRequest(BaseModel):
    """Request for generating embeddings."""
    
    product_ids: Optional[List[str]] = None
    batch_size: int = Field(default=1000, ge=1, le=10000)
    force_regenerate: bool = False
    dry_run: bool = False


class EmbeddingGenerationResponse(BaseModel):
    """Response for embedding generation."""
    
    total_processed: int
    embeddings_generated: int
    embeddings_skipped: int
    errors: int
    duration_seconds: float
    processing_rate: float
    dry_run: bool
