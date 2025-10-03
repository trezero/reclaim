"""WebSocket progress tracking endpoint."""

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.services.progress import get_progress_manager
from app.models import ExecutionStatus
import asyncio

router = APIRouter()


@router.websocket("/progress/{execution_id}")
async def progress_websocket(websocket: WebSocket, execution_id: str):
    """
    Real-time progress updates via WebSocket.

    Sends progress updates every second until execution completes.

    Args:
        execution_id: The execution ID from /execute endpoint
    """
    await websocket.accept()
    progress_manager = get_progress_manager(execution_id)

    try:
        while True:
            # Get current progress
            progress = await progress_manager.get_progress()

            # Send to client
            await websocket.send_json(progress)

            # Check if execution is done
            status = progress.get("status")
            if status in [
                ExecutionStatus.COMPLETED.value,
                ExecutionStatus.FAILED.value,
                ExecutionStatus.CANCELLED.value
            ]:
                # Send final update and close
                await asyncio.sleep(1)
                break

            # Wait before next update
            await asyncio.sleep(1)

    except WebSocketDisconnect:
        pass
    finally:
        await websocket.close()
