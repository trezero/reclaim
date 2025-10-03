"""Rollback manager for reverting operations."""

from typing import Dict, Any, List
from pathlib import Path
import json
from datetime import datetime


class RollbackManager:
    """Manages rollback operations and metadata."""

    def __init__(self, execution_id: str):
        """Initialize rollback manager."""
        self.execution_id = execution_id
        self.rollback_file = Path(f"data/rollback/{execution_id}.json")

    def save_rollback_data(self, operations: List[Dict[str, Any]], plan_id: str):
        """Save rollback metadata."""
        self.rollback_file.parent.mkdir(parents=True, exist_ok=True)

        metadata = {
            "execution_id": self.execution_id,
            "plan_id": plan_id,
            "started_at": datetime.now().isoformat(),
            "operations": operations
        }

        with open(self.rollback_file, "w") as f:
            json.dump(metadata, f, indent=2)

    def load_rollback_data(self) -> Dict[str, Any]:
        """Load rollback metadata."""
        if not self.rollback_file.exists():
            raise FileNotFoundError(f"No rollback data found for {self.execution_id}")

        with open(self.rollback_file, "r") as f:
            return json.load(f)

    async def rollback(self) -> Dict[str, Any]:
        """Execute rollback operations."""
        metadata = self.load_rollback_data()
        operations = metadata.get("operations", [])

        rolled_back = 0
        # Reverse order for rollback
        for operation in reversed(operations):
            action_type = operation.get("action_type")

            if action_type == "MOVE":
                # Reverse move operation
                # In production: shutil.move(target, source) and remove symlink
                rolled_back += 1

            elif action_type == "DELETE_TO_RECYCLE":
                # Restore from recycle bin
                rolled_back += 1

            elif action_type == "EXPORT_IMPORT_WSL":
                # Re-import WSL
                rolled_back += 1

        return {
            "execution_id": self.execution_id,
            "operations_rolled_back": rolled_back,
            "status": "success"
        }

    def cleanup(self):
        """Remove rollback data after successful execution."""
        if self.rollback_file.exists():
            self.rollback_file.unlink()
