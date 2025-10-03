"""Dependency injection for FastAPI endpoints."""

from app.config import settings


def get_settings():
    """Return global settings instance."""
    return settings
