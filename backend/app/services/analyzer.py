"""Drive analysis engine."""

from typing import Dict, Any
from datetime import datetime
from app.models import AnalysisResult
from app.storage.scanner import DriveScanner


class DriveAnalyzer:
    """Analyzes drive usage and identifies optimization opportunities."""

    async def analyze(self) -> Dict[str, Any]:
        """Perform comprehensive drive analysis."""
        scanner = DriveScanner()

        # Get all drives
        drives = scanner.get_all_drives()

        # Identify space consumers
        consumers = scanner.identify_space_consumers()

        # Calculate total recoverable space
        total_recoverable = sum(c.size_bytes for c in consumers)

        # Check for imbalance
        has_imbalance = False
        imbalance_message = None

        if len(drives) >= 2:
            c_drive = next((d for d in drives if d.letter == "C"), None)
            other_drives = [d for d in drives if d.letter != "C"]

            if c_drive and c_drive.percent_used > 70:
                for other in other_drives:
                    if other.percent_used < 30:
                        has_imbalance = True
                        free_gb = other.free_bytes / (1024 ** 3)
                        imbalance_message = (
                            f"{c_drive.letter}: drive is {c_drive.percent_used}% full "
                            f"while {other.letter}: has {free_gb:.0f}GB free"
                        )
                        break

        result = AnalysisResult(
            drives=drives,
            top_consumers=consumers,
            total_recoverable_bytes=total_recoverable,
            has_imbalance=has_imbalance,
            imbalance_message=imbalance_message,
            analyzed_at=datetime.now()
        )

        return result.model_dump()
