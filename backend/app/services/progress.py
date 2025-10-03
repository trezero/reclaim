"""Progress tracking for execution monitoring."""

from typing import Dict, Any, List
from datetime import datetime
from app.models import ExecutionProgress, ExecutionStep, LogEntry, ExecutionStatus, StepStatus, LogLevel
import asyncio


class ProgressManager:
    """Manages execution progress and real-time updates."""

    def __init__(self, execution_id: str):
        """Initialize progress manager."""
        self.execution_id = execution_id
        self.progress_data: Dict[str, Any] = {
            "plan_id": "",
            "overall_percent": 0.0,
            "current_step": 0,
            "total_steps": 0,
            "steps": [],
            "logs": [],
            "status": ExecutionStatus.PENDING.value,
            "updated_at": datetime.now().isoformat()
        }
        self._lock = asyncio.Lock()

    async def initialize(self, plan_id: str, actions: List[Dict[str, Any]]):
        """Initialize progress tracking for a plan."""
        async with self._lock:
            steps = []
            for idx, action in enumerate(actions, 1):
                step = {
                    "id": f"step_{idx}",
                    "action_id": action.get("id", f"action_{idx}"),
                    "status": StepStatus.PENDING.value,
                    "description": action.get("description", ""),
                    "progress_percent": 0,
                    "error_message": None,
                    "started_at": None,
                    "completed_at": None
                }
                steps.append(step)

            self.progress_data = {
                "plan_id": plan_id,
                "overall_percent": 0.0,
                "current_step": 0,
                "total_steps": len(actions),
                "steps": steps,
                "logs": [],
                "status": ExecutionStatus.RUNNING.value,
                "updated_at": datetime.now().isoformat()
            }

    async def update_step(
        self,
        step_index: int,
        status: StepStatus,
        progress_percent: float = None,
        error_message: str = None
    ):
        """Update a specific step's status."""
        async with self._lock:
            if step_index < len(self.progress_data["steps"]):
                step = self.progress_data["steps"][step_index]
                step["status"] = status.value

                if status == StepStatus.ACTIVE:
                    step["started_at"] = datetime.now().isoformat()
                    self.progress_data["current_step"] = step_index + 1
                elif status == StepStatus.COMPLETED:
                    step["completed_at"] = datetime.now().isoformat()
                    step["progress_percent"] = 100
                elif status == StepStatus.FAILED:
                    step["error_message"] = error_message

                if progress_percent is not None:
                    step["progress_percent"] = progress_percent

                # Calculate overall progress
                completed_steps = sum(
                    1 for s in self.progress_data["steps"]
                    if s["status"] == StepStatus.COMPLETED.value
                )
                self.progress_data["overall_percent"] = (
                    completed_steps / self.progress_data["total_steps"] * 100
                )

                self.progress_data["updated_at"] = datetime.now().isoformat()

    async def add_log(self, level: LogLevel, message: str):
        """Add a log entry."""
        async with self._lock:
            log_entry = {
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "level": level.value,
                "message": message
            }
            self.progress_data["logs"].append(log_entry)

            # Keep last 100 logs
            if len(self.progress_data["logs"]) > 100:
                self.progress_data["logs"] = self.progress_data["logs"][-100:]

            self.progress_data["updated_at"] = datetime.now().isoformat()

    async def set_status(self, status: ExecutionStatus):
        """Set overall execution status."""
        async with self._lock:
            self.progress_data["status"] = status.value
            self.progress_data["updated_at"] = datetime.now().isoformat()

            if status == ExecutionStatus.COMPLETED:
                self.progress_data["overall_percent"] = 100.0

    async def get_progress(self) -> Dict[str, Any]:
        """Get current progress data."""
        async with self._lock:
            return self.progress_data.copy()


# Global progress managers
_progress_managers: Dict[str, ProgressManager] = {}


def get_progress_manager(execution_id: str) -> ProgressManager:
    """Get or create progress manager for execution."""
    if execution_id not in _progress_managers:
        _progress_managers[execution_id] = ProgressManager(execution_id)
    return _progress_managers[execution_id]


def cleanup_progress_manager(execution_id: str):
    """Remove progress manager after completion."""
    if execution_id in _progress_managers:
        del _progress_managers[execution_id]
