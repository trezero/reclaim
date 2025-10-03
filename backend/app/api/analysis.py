"""Analysis API endpoints."""

from fastapi import APIRouter, HTTPException
from app.services.analyzer import DriveAnalyzer

router = APIRouter()


@router.get("/analyze")
async def analyze_drives():
    """
    Analyze all drives and return usage statistics.

    Returns drive information, top space consumers, and imbalance detection.
    """
    try:
        analyzer = DriveAnalyzer()
        result = await analyzer.analyze()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
