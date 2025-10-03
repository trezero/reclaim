"""Plan generation API endpoints."""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List, Dict, Any
from app.services.planner import PlanGenerator
from app.services.analyzer import DriveAnalyzer
from app.config import Settings
from app.dependencies import get_settings

router = APIRouter()

# Cache for generated plans
_cached_plans: Optional[List[Dict[str, Any]]] = None


@router.get("/plans")
async def get_plans(
    use_ai: Optional[bool] = Query(None, description="Force AI or rule-based generation"),
    settings: Settings = Depends(get_settings)
) -> List[Dict[str, Any]]:
    """
    Generate 3 cleanup plans (Conservative, Balanced, Aggressive).

    Plans are cached for 5 minutes to avoid regeneration.
    """
    global _cached_plans

    try:
        # Get fresh analysis
        analyzer = DriveAnalyzer()
        analysis_result = await analyzer.analyze()

        # Generate plans
        planner = PlanGenerator(settings)
        plans = await planner.generate_plans(analysis_result, force_ai=use_ai)

        # Cache plans
        _cached_plans = plans

        return plans

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Plan generation failed: {str(e)}")


@router.get("/plan/{plan_id}")
async def get_plan_details(plan_id: str) -> Dict[str, Any]:
    """
    Get detailed information for a specific plan.

    Args:
        plan_id: Plan ID (conservative, balanced, or aggressive)
    """
    global _cached_plans

    if not _cached_plans:
        raise HTTPException(
            status_code=404,
            detail="No plans available. Call /plans first to generate plans."
        )

    plan = next((p for p in _cached_plans if p["id"] == plan_id), None)

    if not plan:
        raise HTTPException(
            status_code=404,
            detail=f"Plan '{plan_id}' not found"
        )

    return plan
