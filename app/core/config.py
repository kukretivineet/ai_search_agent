#!/usr/bin/env python3
"""
Core configuration for the search agent application.
Uses pydantic-settings for environment variable management.
"""

import os
from typing import Optional, List
from pydantic_settings import BaseSettings
from pydantic import Field, validator
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
        # Application
    app_name: str = "Search Agent API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database
    mongodb_uri: str = "mongodb://localhost:27017/"
    mongodb_atlas_uri: Optional[str] = None
    db_name: str = "ecom_search"
    collection_name: str = "products"
    
    # OpenAI
    openai_api_key: str
    embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = 1536
    
    # Processing
    default_batch_size: int = 1000
    max_retries: int = 3
    rate_limit_delay: float = 0.5
    
    # Search
    default_search_limit: int = 10
    max_search_limit: int = 100
    similarity_threshold: float = 0.7
    
    # Reranking
    rerank_enabled: bool = True
    rerank_threshold: float = 0.92
    cohere_api_key: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    
    # Caching
    cache_enabled: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        validate_assignment = True
        extra = "ignore"


# Global settings instance
# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings
