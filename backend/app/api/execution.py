"""Execution API endpoints."""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from datetime import datetime
import uuid
from app.models import ExecuteRequest, ExecuteResponse
from app.services.executor import ExecutionEngine
from app.api.plans import _cached_plans

router = APIRouter()


@router.post("/execute", response_model=ExecuteResponse)
async def execute_plan(
    request: ExecuteRequest,
    background_tasks: BackgroundTasks
):
    """
    Start execution of a cleanup plan.

    The execution runs in the background. Use the WebSocket endpoint
    to monitor progress in real-time.

    Args:
        request: Execution request with plan_id and dry_run flag
    """
    # Find the plan
    if not _cached_plans:
        raise HTTPException(
            status_code=404,
            detail="No plans available. Call /plans first to generate plans."
        )

    plan = next((p for p in _cached_plans if p["id"] == request.plan_id), None)

    if not plan:
        raise HTTPException(
            status_code=404,
            detail=f"Plan '{request.plan_id}' not found"
        )

    # Create execution
    execution_id = str(uuid.uuid4())
    executor = ExecutionEngine(execution_id, plan, dry_run=request.dry_run)

    # Run in background
    background_tasks.add_task(executor.execute)

    return ExecuteResponse(
        execution_id=execution_id,
        status="started",
        started_at=datetime.now()
    )
