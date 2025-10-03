"""Plan generation service with AI and rule-based fallback."""

from typing import List, Dict, Any, Optional
from datetime import datetime
from app.models import Plan, PlanAction, RiskLevel, ActionType
from app.ai.openai_client import OpenAIClient
from app.ai.anthropic_client import AnthropicClient
from app.config import Settings
from pathlib import Path
import os


class PlanGenerator:
    """Generates cleanup plans using AI or rule-based logic."""

    def __init__(self, settings: Settings):
        """Initialize plan generator."""
        self.settings = settings

    async def generate_plans(
        self,
        analysis_result: Dict[str, Any],
        force_ai: Optional[bool] = None
    ) -> List[Dict[str, Any]]:
        """Generate 3-tier cleanup plans."""
        use_ai = force_ai if force_ai is not None else False

        # Try AI generation if enabled and API key available
        if use_ai:
            if self.settings.openai_api_key:
                plans = await self._generate_with_openai(analysis_result)
                if plans:
                    return plans
            elif self.settings.anthropic_api_key:
                plans = await self._generate_with_anthropic(analysis_result)
                if plans:
                    return plans

        # Fallback to rule-based generation
        return self._generate_rule_based(analysis_result)

    async def _generate_with_openai(
        self,
        analysis_result: Dict[str, Any]
    ) -> Optional[List[Dict[str, Any]]]:
        """Generate plans using OpenAI."""
        try:
            client = OpenAIClient(self.settings.openai_api_key)

            drive_data = {"drives": analysis_result["drives"]}
            consumers_data = analysis_result["top_consumers"]

            plans = await client.generate_plans(
                drive_data=drive_data,
                consumers_data=consumers_data,
                target_drive=self.settings.default_target_drive,
                backup_location=self.settings.backup_location
            )

            return plans
        except Exception as e:
            print(f"OpenAI generation failed: {e}")
            return None

    async def _generate_with_anthropic(
        self,
        analysis_result: Dict[str, Any]
    ) -> Optional[List[Dict[str, Any]]]:
        """Generate plans using Anthropic."""
        try:
            client = AnthropicClient(self.settings.anthropic_api_key)

            drive_data = {"drives": analysis_result["drives"]}
            consumers_data = analysis_result["top_consumers"]

            plans = await client.generate_plans(
                drive_data=drive_data,
                consumers_data=consumers_data,
                target_drive=self.settings.default_target_drive,
                backup_location=self.settings.backup_location
            )

            return plans
        except Exception as e:
            print(f"Anthropic generation failed: {e}")
            return None

    def _generate_rule_based(
        self,
        analysis_result: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate plans using rule-based logic."""
        consumers = analysis_result.get("top_consumers", [])
        home = Path.home()

        # Find specific consumers
        docker_consumer = next((c for c in consumers if c["type"] == "docker"), None)
        wsl_consumers = [c for c in consumers if c["type"] == "wsl"]
        cache_consumers = [c for c in consumers if c["type"] == "cache"]
        temp_consumers = [c for c in consumers if c["type"] == "temp"]
        downloads_consumer = next((c for c in consumers if c["type"] == "downloads"), None)

        # Conservative Plan
        conservative_actions = []
        conservative_space = 0

        # Clear browser caches
        for idx, cache in enumerate(cache_consumers[:3], 1):
            conservative_actions.append({
                "id": f"conservative_action_{idx}",
                "type": "CLEANUP",
                "description": f"Clear {cache['name']}",
                "size_bytes": cache["size_bytes"],
                "safety_explanation": "Browsers will rebuild cache automatically",
                "rollback_option": "Not needed (cache data)",
                "estimated_seconds": 120
            })
            conservative_space += cache["size_bytes"]

        # Clear temp files
        for idx, temp in enumerate(temp_consumers[:2], len(conservative_actions) + 1):
            conservative_actions.append({
                "id": f"conservative_action_{idx}",
                "type": "CLEANUP",
                "description": f"Clear Temporary Files: {temp['name']}",
                "size_bytes": temp["size_bytes"],
                "safety_explanation": "Safe to delete temporary files",
                "rollback_option": "Not needed (temporary data)",
                "estimated_seconds": 180
            })
            conservative_space += temp["size_bytes"]

        # Balanced Plan
        balanced_actions = list(conservative_actions)  # Include all conservative actions
        balanced_space = conservative_space

        # Move Docker if exists
        if docker_consumer:
            balanced_actions.append({
                "id": f"balanced_action_{len(balanced_actions) + 1}",
                "type": "MOVE",
                "description": "Move Docker Desktop data",
                "source_path": docker_consumer["path"],
                "target_path": f"{self.settings.default_target_drive}\\Docker",
                "size_bytes": docker_consumer["size_bytes"],
                "safety_explanation": "Symlink maintains compatibility; Docker will function normally",
                "rollback_option": "Reverse move and restore symlink",
                "estimated_seconds": 600
            })
            balanced_space += docker_consumer["size_bytes"]

        # Prune Docker
        if docker_consumer:
            balanced_actions.append({
                "id": f"balanced_action_{len(balanced_actions) + 1}",
                "type": "PRUNE",
                "description": "Clean Docker unused images and containers",
                "command": "docker system prune -af --volumes",
                "size_bytes": int(docker_consumer["size_bytes"] * 0.3),  # Estimate 30%
                "safety_explanation": "Only removes unused Docker resources",
                "rollback_option": "Images can be re-downloaded",
                "estimated_seconds": 300
            })
            balanced_space += int(docker_consumer["size_bytes"] * 0.3)

        # Aggressive Plan
        aggressive_actions = list(balanced_actions)  # Include all balanced actions
        aggressive_space = balanced_space

        # Move WSL distributions
        for idx, wsl in enumerate(wsl_consumers[:2], 1):
            distro_name = wsl["name"].replace("WSL - ", "")
            aggressive_actions.append({
                "id": f"aggressive_action_{len(aggressive_actions) + 1}",
                "type": "EXPORT_IMPORT_WSL",
                "description": f"Relocate WSL: {distro_name}",
                "source_path": wsl["path"],
                "target_path": f"{self.settings.default_target_drive}\\WSL\\{distro_name}",
                "size_bytes": wsl["size_bytes"],
                "safety_explanation": "WSL export/import preserves all data",
                "rollback_option": "Re-import from backup tar",
                "estimated_seconds": 900
            })
            aggressive_space += wsl["size_bytes"]

        # Move Downloads
        if downloads_consumer:
            aggressive_actions.append({
                "id": f"aggressive_action_{len(aggressive_actions) + 1}",
                "type": "MOVE",
                "description": "Relocate Downloads folder",
                "source_path": downloads_consumer["path"],
                "target_path": f"{self.settings.default_target_drive}\\Downloads",
                "size_bytes": downloads_consumer["size_bytes"],
                "safety_explanation": "Symlink maintains file access; all programs work normally",
                "rollback_option": "Reverse move and restore symlink",
                "estimated_seconds": 300
            })
            aggressive_space += downloads_consumer["size_bytes"]

        # Build plans
        plans = [
            {
                "id": "conservative",
                "name": "Conservative",
                "space_saved_bytes": conservative_space,
                "risk_level": "low",
                "estimated_minutes": sum(a["estimated_seconds"] for a in conservative_actions) // 60,
                "rationale": "Clean temporary files and caches only. No files are moved or deleted permanently. Safe for all users.",
                "recommended": False,
                "actions": conservative_actions,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "balanced",
                "name": "Balanced",
                "space_saved_bytes": balanced_space,
                "risk_level": "medium",
                "estimated_minutes": sum(a["estimated_seconds"] for a in balanced_actions) // 60,
                "rationale": "Recommended approach. Cleans caches and temp files, relocates Docker to free up C: drive. Uses symlinks for compatibility. Includes Docker cleanup.",
                "recommended": True,
                "actions": balanced_actions,
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "aggressive",
                "name": "Aggressive",
                "space_saved_bytes": aggressive_space,
                "risk_level": "high",
                "estimated_minutes": sum(a["estimated_seconds"] for a in aggressive_actions) // 60,
                "rationale": "Maximum space savings. Relocates Docker, WSL distributions, and Downloads folder. Uses symlinks and WSL export/import. Requires more time but frees the most space.",
                "recommended": False,
                "actions": aggressive_actions,
                "created_at": datetime.now().isoformat()
            }
        ]

        return plans
