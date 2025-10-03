"""FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api import analysis, plans, execution, progress, settings as settings_api

# Create FastAPI application
app = FastAPI(
    title="Storage Manager Backend",
    description="AI-powered Windows storage optimization API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analysis.router, tags=["Analysis"])
app.include_router(plans.router, tags=["Plans"])
app.include_router(execution.router, tags=["Execution"])
app.include_router(progress.router, tags=["Progress"])
app.include_router(settings_api.router, tags=["Settings"])


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Storage Manager Backend",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )
