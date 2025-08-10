"""
Search API Schemas - Request/Response Models
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional, Literal


class SearchRequest(BaseModel):
    """Search request model"""
    
    query: str = Field(..., description="Search query string", min_length=1, max_length=200)
    mode: Literal["text", "vector", "hybrid"] = Field(
        default="hybrid", 
        description="Search mode: text, vector, or hybrid"
    )
    limit: int = Field(
        default=20, 
        description="Maximum number of results to return",
        ge=1,
        le=100
    )
    page: int = Field(
        default=1,
        description="Page number for pagination",
        ge=1
    )
    use_reranking: bool = Field(
        default=True,
        description="Whether to apply Cohere reranking"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "query": "blue shirt",
                "mode": "hybrid",
                "limit": 10,
                "page": 1,
                "use_reranking": True
            }
        }


class ProductResult(BaseModel):
    """Product result model"""
    
    id: str = Field(..., description="Product ID", alias="_id")
    title: str = Field(..., description="Product title")
    brand: Optional[str] = Field(None, description="Product brand")
    category: Optional[str] = Field(None, description="Product category")
    sub_category: Optional[str] = Field(None, description="Product sub-category")
    description: Optional[str] = Field(None, description="Product description")
    selling_price_numeric: Optional[float] = Field(None, description="Selling price")
    price_inr: Optional[float] = Field(None, description="Price in INR")
    images: Optional[List[str]] = Field(None, description="Product images")
    vector_score: Optional[float] = Field(None, description="Vector similarity score")
    search_score: Optional[float] = Field(None, description="Combined search score")
    search_type: Optional[str] = Field(None, description="Search type (text/vector)")
    relevance_score: Optional[float] = Field(None, description="Reranking relevance score")
    
    class Config:
        allow_population_by_field_name = True


class SearchResponse(BaseModel):
    """Search response model"""
    
    results: List[ProductResult] = Field(..., description="Search results")
    total: int = Field(..., description="Total number of matching results")
    returned: int = Field(..., description="Number of results returned")
    query: str = Field(..., description="Original search query")
    mode: str = Field(..., description="Search mode used")
    execution_time: float = Field(..., description="Search execution time in seconds")
    reranked: bool = Field(default=False, description="Whether results were reranked")
    page: int = Field(default=1, description="Current page number")
    total_pages: int = Field(default=1, description="Total number of pages")
    has_next: bool = Field(default=False, description="Whether there are more pages")
    has_prev: bool = Field(default=False, description="Whether there are previous pages")

    class Config:
        json_schema_extra = {
            "example": {
                "results": [
                    {
                        "_id": "123",
                        "title": "Blue Cotton Shirt",
                        "brand": "Brand X",
                        "category": "Clothing",
                        "selling_price_numeric": 999.0,
                        "vector_score": 0.85,
                        "relevance_score": 0.92
                    }
                ],
                "total": 150,
                "returned": 10,
                "query": "blue shirt",
                "mode": "hybrid",
                "execution_time": 0.245,
                "reranked": True,
                "page": 1,
                "total_pages": 15,
                "has_next": True,
                "has_prev": False
            }
        }
