"""Tests for API endpoints."""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_root_endpoint():
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert "name" in response.json()


def test_health_check():
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_analyze_endpoint():
    """Test analyze endpoint."""
    response = client.get("/analyze")
    assert response.status_code == 200
    data = response.json()
    assert "drives" in data
    assert "top_consumers" in data


def test_plans_endpoint():
    """Test plans generation endpoint."""
    response = client.get("/plans")
    assert response.status_code == 200
    plans = response.json()
    assert isinstance(plans, list)
    assert len(plans) == 3


def test_settings_endpoint():
    """Test settings endpoint."""
    response = client.get("/settings")
    assert response.status_code == 200
    settings = response.json()
    assert "use_ai" in settings
    assert "dry_run" in settings
