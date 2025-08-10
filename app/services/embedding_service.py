#!/usr/bin/env python3
"""
Application service for managing embedding generation workflow.
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional, Tuple
from openai import AsyncOpenAI
from app.core.config import get_settings
from app.domain.embeddings.models import ProductEmbedding, EmbeddingMetadata
from app.domain.embeddings.services import EmbeddingTextService
from app.repositories.product_repository import ProductRepository


class EmbeddingService:
    """Application service for embedding generation and processing."""
    
    def __init__(self, product_repo: ProductRepository):
        """
        Initialize embedding service.
        
        Args:
            product_repo: Repository for product data access
        """
        self.product_repo = product_repo
        self.settings = get_settings()
        self.openai_client = AsyncOpenAI(api_key=self.settings.openai.api_key)
        self.logger = logging.getLogger(__name__)
    
    async def generate_embeddings_batch(
        self,
        batch_size: int = 1000,
        progress_callback: Optional[callable] = None
    ) -> Dict[str, Any]:
        """
        Generate embeddings for all products in batches.
        
        Args:
            batch_size: Number of products to process per batch
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dict containing processing statistics
        """
        stats = {
            "total_processed": 0,
            "total_updated": 0,
            "total_errors": 0,
            "batches_processed": 0
        }
        
        # Get total count for progress tracking
        total_products = await self.product_repo.count_products_without_embeddings()
        self.logger.info(f"Starting embedding generation for {total_products} products")
        
        batch_num = 0
        while True:
            batch_num += 1
            
            # Fetch batch of products without embeddings
            products = await self.product_repo.get_products_without_embeddings(
                limit=batch_size,
                skip=0  # Always skip 0 since we're processing products without embeddings
            )
            
            if not products:
                self.logger.info("No more products to process")
                break
            
            try:
                # Process batch
                batch_stats = await self._process_batch(products, batch_num)
                
                # Update overall stats
                stats["total_processed"] += batch_stats["processed"]
                stats["total_updated"] += batch_stats["updated"]
                stats["total_errors"] += batch_stats["errors"]
                stats["batches_processed"] += 1
                
                # Progress callback
                if progress_callback:
                    progress_callback(stats, batch_stats)
                
                # Log progress every 10 records
                if stats["total_processed"] % 10 == 0:
                    self.logger.info(
                        f"✅ Progress: {stats['total_processed']}/{total_products} products processed "
                        f"({stats['total_updated']} updated, {stats['total_errors']} errors)"
                    )
                
            except Exception as e:
                self.logger.error(f"Error processing batch {batch_num}: {e}")
                stats["total_errors"] += len(products)
            
            # Rate limiting pause
            await asyncio.sleep(0.1)
        
        return stats
    
    async def _process_batch(
        self, 
        products: List[Dict[str, Any]], 
        batch_num: int
    ) -> Dict[str, int]:
        """
        Process a batch of products to generate embeddings.
        
        Args:
            products: List of product documents
            batch_num: Batch number for logging
            
        Returns:
            Dict with batch processing statistics
        """
        batch_stats = {"processed": 0, "updated": 0, "errors": 0}
        
        self.logger.info(f"Processing batch {batch_num} with {len(products)} products")
        
        # Generate embedding texts
        embedding_requests = []
        product_map = {}
        
        for product in products:
            try:
                # Generate structured embedding text
                embedding_text = EmbeddingTextService.build_embedding_text(product)
                
                embedding_requests.append(embedding_text)
                product_map[embedding_text] = product
                
            except Exception as e:
                self.logger.error(f"Error generating text for product {product.get('_id')}: {e}")
                batch_stats["errors"] += 1
        
        if not embedding_requests:
            return batch_stats
        
        try:
            # Generate embeddings in bulk
            embeddings = await self._generate_openai_embeddings(embedding_requests)
            
            # Prepare updates
            updates = []
            for embedding_text, embedding_vector in zip(embedding_requests, embeddings):
                try:
                    product = product_map[embedding_text]
                    
                    # Create embedding metadata
                    metadata = EmbeddingMetadata(
                        model=self.settings.openai.embedding_model,
                        dimensions=len(embedding_vector),
                        source_text=embedding_text
                    )
                    
                    # Create product embedding
                    product_embedding = ProductEmbedding(
                        product_id=str(product["_id"]),
                        embedding_vector=embedding_vector,
                        metadata=metadata
                    )
                    
                    updates.append(product_embedding)
                    
                except Exception as e:
                    self.logger.error(f"Error preparing update for product: {e}")
                    batch_stats["errors"] += 1
            
            # Bulk update database
            if updates:
                updated_count = await self.product_repo.bulk_update_embeddings(updates)
                batch_stats["updated"] = updated_count
            
        except Exception as e:
            self.logger.error(f"Error generating embeddings for batch {batch_num}: {e}")
            batch_stats["errors"] += len(embedding_requests)
        
        batch_stats["processed"] = len(products)
        return batch_stats
    
    async def _generate_openai_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings using OpenAI API.
        
        Args:
            texts: List of texts to embed
            
        Returns:
            List of embedding vectors
        """
        try:
            response = await self.openai_client.embeddings.create(
                model=self.settings.openai.embedding_model,
                input=texts,
                encoding_format="float"
            )
            
            return [embedding.embedding for embedding in response.data]
            
        except Exception as e:
            self.logger.error(f"OpenAI embedding generation failed: {e}")
            raise
    
    async def generate_single_embedding(self, product_id: str) -> Optional[ProductEmbedding]:
        """
        Generate embedding for a single product.
        
        Args:
            product_id: Product ID to generate embedding for
            
        Returns:
            ProductEmbedding or None if failed
        """
        try:
            # Get product
            product = await self.product_repo.get_product_by_id(product_id)
            if not product:
                self.logger.warning(f"Product not found: {product_id}")
                return None
            
            # Generate embedding text
            embedding_text = EmbeddingTextService.build_embedding_text(product)
            
            # Generate embedding
            embeddings = await self._generate_openai_embeddings([embedding_text])
            
            if not embeddings:
                return None
            
            # Create metadata
            metadata = EmbeddingMetadata(
                model=self.settings.openai.embedding_model,
                dimensions=len(embeddings[0]),
                source_text=embedding_text
            )
            
            # Create product embedding
            product_embedding = ProductEmbedding(
                product_id=product_id,
                embedding_vector=embeddings[0],
                metadata=metadata
            )
            
            # Update database
            await self.product_repo.update_product_embedding(product_embedding)
            
            return product_embedding
            
        except Exception as e:
            self.logger.error(f"Error generating single embedding for {product_id}: {e}")
            return None
    
    async def get_embedding_stats(self) -> Dict[str, int]:
        """Get embedding generation statistics."""
        return await self.product_repo.get_embedding_stats()
