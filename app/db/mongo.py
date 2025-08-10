#!/usr/bin/env python3
"""
MongoDB connection and lifecycle management.
"""

import logging
from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection

from app.core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class AsyncMongoClient:
    """Async MongoDB client wrapper."""
    
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database: Optional[AsyncIOMotorDatabase] = None
    
    async def connect(self) -> None:
        """Connect to MongoDB."""
        try:
            self.client = AsyncIOMotorClient(settings.mongodb_uri)
            self.database = self.client[settings.db_name]
            
            # Test connection
            await self.client.admin.command('ping')
            logger.info(f"Connected to async MongoDB: {settings.db_name}")
            
        except Exception as e:
            logger.error(f"Failed to connect to async MongoDB: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from MongoDB."""
        if self.client:
            self.client.close()
            self.client = None
            logger.info("Disconnected from async MongoDB")
    
    def get_database(self):
        """Get the database instance."""
        if not self.client:
            raise RuntimeError("Not connected to MongoDB. Call connect() first.")
        return self.client[settings.db_name]
    
    def get_collection(self, collection_name: Optional[str] = None) -> AsyncIOMotorCollection:
        """Get a collection."""
        if not self.database:
            raise RuntimeError("Database not initialized. Call connect() first.")
        
        collection_name = collection_name or settings.collection_name
        return self.database[collection_name]


class SyncMongoClient:
    """Sync MongoDB client wrapper."""
    
    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.database: Optional[Database] = None
    
    def connect(self) -> None:
        """Connect to MongoDB."""
        try:
            self.client = MongoClient(settings.mongodb_uri)
            self.database = self.client[settings.db_name]
            
            # Test connection
            self.client.admin.command('ping')
            logger.info(f"Connected to sync MongoDB: {settings.db_name}")
            
        except Exception as e:
            logger.error(f"Failed to connect to sync MongoDB: {e}")
            raise
    
    def close(self) -> None:
        """Close MongoDB connection."""
        if self.client:
            self.client.close()
            logger.info("Closed sync MongoDB connection")
    
    def get_collection(self, collection_name: Optional[str] = None) -> Collection:
        """Get a collection."""
        if not self.database:
            raise RuntimeError("Database not initialized. Call connect() first.")
        
        collection_name = collection_name or settings.collection_name
        return self.database[collection_name]


# Global instances
async_mongo_client = AsyncMongoClient()
sync_mongo_client = SyncMongoClient()


async def get_async_db() -> AsyncIOMotorDatabase:
    """Get async database connection."""
    if not async_mongo_client.database:
        await async_mongo_client.connect()
    return async_mongo_client.database


def get_sync_db() -> Database:
    """Get sync database connection."""
    if not sync_mongo_client.database:
        sync_mongo_client.connect()
    return sync_mongo_client.database


async def get_async_collection(collection_name: Optional[str] = None) -> AsyncIOMotorCollection:
    """Get async collection."""
    return async_mongo_client.get_collection(collection_name)


def get_sync_collection(collection_name: Optional[str] = None) -> Collection:
    """Get sync collection."""
    return sync_mongo_client.get_collection(collection_name)


# Lifecycle functions for FastAPI
async def connect_to_mongo():
    """Connect to MongoDB on startup."""
    await async_mongo_client.connect()
    sync_mongo_client.connect()


async def close_mongo_connection():
    """Close MongoDB connection on shutdown."""
    await async_mongo_client.close()
    sync_mongo_client.close()
