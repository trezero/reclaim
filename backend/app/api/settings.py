"""Settings API endpoints."""

from fastapi import APIRouter, Depends
from app.models import UserSettings, UpdateSettingsRequest
from app.config import Settings
from app.dependencies import get_settings
from pathlib import Path
import json

router = APIRouter()

# Settings file path
SETTINGS_FILE = Path("data/settings.json")


def _load_user_settings() -> UserSettings:
    """Load user settings from file."""
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            return UserSettings(**data)
    return UserSettings()


def _save_user_settings(settings: UserSettings):
    """Save user settings to file."""
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings.model_dump(), f, indent=2)


@router.get("/settings", response_model=UserSettings)
async def get_settings_endpoint():
    """
    Retrieve user settings.

    Returns all user preferences including AI configuration,
    safety settings, and storage locations.
    """
    return _load_user_settings()


@router.post("/settings", response_model=UserSettings)
async def update_settings_endpoint(request: UpdateSettingsRequest):
    """
    Update user settings.

    Only provided fields will be updated. Others remain unchanged.
    """
    # Load current settings
    current = _load_user_settings()

    # Update only provided fields
    update_data = request.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current, key, value)

    # Save updated settings
    _save_user_settings(current)

    return current
