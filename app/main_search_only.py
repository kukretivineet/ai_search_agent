#!/usr/bin/env python3
"""
FastAPI application for DDD-based search system.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.core.config import get_settings
from app.core.logging_simple import setup_logging
from app.db.mongo import AsyncMongoClient
from app.api.v1.routes.search import router as search_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    settings = get_settings()
    setup_logging(settings.log_level)
    
    logger = logging.getLogger(__name__)
    logger.info("Starting Search Agent API")
    
    # Initialize database connection
    mongo_client = AsyncMongoClient()
    await mongo_client.connect()
    app.state.mongo_client = mongo_client
    
    logger.info("Application startup completed")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")
    if hasattr(app.state, 'mongo_client'):
        await app.state.mongo_client.disconnect()
    logger.info("Application shutdown completed")


def create_app() -> FastAPI:
    """
    Create and configure FastAPI application.
    
    Returns:
        Configured FastAPI application
    """
    settings = get_settings()
    
    app = FastAPI(
        title="Search Agent API",
        description="Domain-driven search API with OpenAI embeddings and Cohere reranking",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan
    )
    
    # Initialize templates
    templates = Jinja2Templates(directory="templates")
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Configure appropriately for production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include routers
    app.include_router(
        search_router,
        prefix="/api/v1/search",
        tags=["search"]
    )
    
    # Add compatibility route for the UI
    app.include_router(
        search_router,
        prefix="/api/search",
        tags=["search-compat"]
    )
    
    @app.get("/", response_class=HTMLResponse)
    async def read_root(request: Request):
        """Serve the main UI template."""
        return templates.TemplateResponse("index.html", {"request": request})
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy", "service": "search-agent"}
    
    @app.get("/api")
    async def api_info():
        """API info endpoint."""
        return {
            "message": "Search Agent API - DDD Architecture",
            "docs": "/docs",
            "health": "/health",
            "search": "/api/v1/search/",
            "version": "1.0.0"
        }
    
    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    settings = get_settings()
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level=settings.log_level.lower()
    )
