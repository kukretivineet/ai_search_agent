"""
Simple embedding service for search operations.
"""

import logging
from typing import List, Optional
from openai import AsyncOpenAI


class SimpleEmbeddingService:
    """Simple embedding service for generating query embeddings."""
    
    def __init__(self, api_key: str, model: str = "text-embedding-3-small"):
        """Initialize embedding service.
        
        Args:
            api_key: OpenAI API key
            model: Embedding model name
        """
        self.api_key = api_key
        self.model = model
        self.client = AsyncOpenAI(api_key=api_key)
        self.logger = logging.getLogger(__name__)
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for a single text.
        
        Args:
            text: Input text to embed
            
        Returns:
            Embedding vector as list of floats
        """
        try:
            response = await self.client.embeddings.create(
                input=text,
                model=self.model
            )
            
            embedding = response.data[0].embedding
            self.logger.debug(f"Generated embedding for text: {text[:50]}...")
            return embedding
            
        except Exception as e:
            self.logger.error(f"Error generating embedding: {e}")
            raise
    
    async def generate_embeddings_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            response = await self.client.embeddings.create(
                input=texts,
                model=self.model
            )
            
            embeddings = [data.embedding for data in response.data]
            self.logger.debug(f"Generated {len(embeddings)} embeddings")
            return embeddings
            
        except Exception as e:
            self.logger.error(f"Error generating batch embeddings: {e}")
            raise
