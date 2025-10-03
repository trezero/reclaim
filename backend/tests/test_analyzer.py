"""Tests for drive analyzer service."""

import pytest
from app.services.analyzer import DriveAnalyzer


@pytest.mark.asyncio
async def test_analyzer_returns_drives():
    """Test that analyzer returns drive information."""
    analyzer = DriveAnalyzer()
    result = await analyzer.analyze()

    assert "drives" in result
    assert isinstance(result["drives"], list)


@pytest.mark.asyncio
async def test_analyzer_identifies_consumers():
    """Test that analyzer identifies space consumers."""
    analyzer = DriveAnalyzer()
    result = await analyzer.analyze()

    assert "top_consumers" in result
    assert isinstance(result["top_consumers"], list)


@pytest.mark.asyncio
async def test_analyzer_detects_imbalance():
    """Test imbalance detection."""
    analyzer = DriveAnalyzer()
    result = await analyzer.analyze()

    assert "has_imbalance" in result
    assert isinstance(result["has_imbalance"], bool)
