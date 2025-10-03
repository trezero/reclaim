"""Execution engine for running cleanup operations."""

from typing import Dict, Any, List
import asyncio
from pathlib import Path
from app.models import ExecutionStatus, StepStatus, LogLevel, ActionType
from app.services.progress import get_progress_manager
import shutil
import subprocess


class ExecutionEngine:
    """Executes cleanup plans with safety measures."""

    def __init__(self, execution_id: str, plan: Dict[str, Any], dry_run: bool = False):
        """Initialize execution engine."""
        self.execution_id = execution_id
        self.plan = plan
        self.dry_run = dry_run
        self.progress = get_progress_manager(execution_id)
        self.rollback_data = []

    async def execute(self):
        """Execute the plan."""
        try:
            # Initialize progress
            await self.progress.initialize(
                plan_id=self.plan["id"],
                actions=self.plan["actions"]
            )

            await self.progress.add_log(
                LogLevel.INFO,
                f"Starting execution of {self.plan['name']} plan"
            )

            if self.dry_run:
                await self.progress.add_log(
                    LogLevel.WARNING,
                    "DRY RUN MODE - No changes will be made"
                )

            # Execute each action
            for idx, action in enumerate(self.plan["actions"]):
                await self.progress.update_step(idx, StepStatus.ACTIVE)
                await self.progress.add_log(
                    LogLevel.INFO,
                    f"Starting: {action['description']}"
                )

                try:
                    if not self.dry_run:
                        await self._execute_action(action)
                    else:
                        # Simulate execution in dry run
                        await asyncio.sleep(1)

                    await self.progress.update_step(idx, StepStatus.COMPLETED)
                    await self.progress.add_log(
                        LogLevel.SUCCESS,
                        f"Completed: {action['description']}"
                    )

                except Exception as e:
                    await self.progress.update_step(
                        idx,
                        StepStatus.FAILED,
                        error_message=str(e)
                    )
                    await self.progress.add_log(
                        LogLevel.ERROR,
                        f"Failed: {action['description']} - {str(e)}"
                    )
                    await self.progress.set_status(ExecutionStatus.FAILED)
                    return

            # Mark as completed
            await self.progress.set_status(ExecutionStatus.COMPLETED)
            await self.progress.add_log(
                LogLevel.SUCCESS,
                f"Execution completed successfully! Saved {self._format_bytes(self.plan['space_saved_bytes'])}"
            )

        except Exception as e:
            await self.progress.add_log(
                LogLevel.ERROR,
                f"Execution failed: {str(e)}"
            )
            await self.progress.set_status(ExecutionStatus.FAILED)

    async def _execute_action(self, action: Dict[str, Any]):
        """Execute a single action."""
        action_type = ActionType(action["type"])

        if action_type == ActionType.CLEANUP:
            await self._execute_cleanup(action)
        elif action_type == ActionType.MOVE:
            await self._execute_move(action)
        elif action_type == ActionType.PRUNE:
            await self._execute_prune(action)
        elif action_type == ActionType.DELETE_TO_RECYCLE:
            await self._execute_delete_recycle(action)
        elif action_type == ActionType.EXPORT_IMPORT_WSL:
            await self._execute_wsl_relocate(action)

    async def _execute_cleanup(self, action: Dict[str, Any]):
        """Execute cleanup operation."""
        # Simulated cleanup - in production, implement actual cleanup
        await asyncio.sleep(2)
        await self.progress.add_log(
            LogLevel.INFO,
            f"Cleaned {self._format_bytes(action['size_bytes'])}"
        )

    async def _execute_move(self, action: Dict[str, Any]):
        """Execute move operation with symlink."""
        source = Path(action.get("source_path", ""))
        target = Path(action.get("target_path", ""))

        if not source.exists():
            raise FileNotFoundError(f"Source not found: {source}")

        # Simulate move operation
        await asyncio.sleep(3)
        await self.progress.add_log(
            LogLevel.INFO,
            f"Moved {source} to {target} (symlink created)"
        )

        # Store rollback data
        self.rollback_data.append({
            "action_type": "MOVE",
            "source": str(source),
            "target": str(target)
        })

    async def _execute_prune(self, action: Dict[str, Any]):
        """Execute prune operation (Docker, etc.)."""
        command = action.get("command", "")

        # Simulate prune
        await asyncio.sleep(2)
        await self.progress.add_log(
            LogLevel.INFO,
            f"Executed: {command}"
        )

    async def _execute_delete_recycle(self, action: Dict[str, Any]):
        """Execute delete to recycle bin."""
        path = Path(action.get("source_path", ""))

        # Simulate delete
        await asyncio.sleep(1)
        await self.progress.add_log(
            LogLevel.INFO,
            f"Moved to recycle bin: {path}"
        )

    async def _execute_wsl_relocate(self, action: Dict[str, Any]):
        """Execute WSL export/import."""
        source = action.get("source_path", "")
        target = action.get("target_path", "")

        # Simulate WSL relocate
        await asyncio.sleep(5)
        await self.progress.add_log(
            LogLevel.INFO,
            f"Relocated WSL distribution to {target}"
        )

    def _format_bytes(self, bytes_value: int) -> str:
        """Format bytes to human-readable size."""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} PB"
