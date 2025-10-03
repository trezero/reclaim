"""Input validation utilities."""

from pathlib import Path
import re


def validate_drive_letter(letter: str) -> bool:
    """Validate Windows drive letter."""
    return bool(re.match(r'^[A-Z]$', letter))


def validate_path(path_str: str) -> bool:
    """Validate file system path."""
    try:
        path = Path(path_str)
        # Check for directory traversal
        if '..' in path.parts:
            return False
        return True
    except Exception:
        return False


def validate_api_key(key: str, provider: str) -> bool:
    """Validate API key format."""
    if provider == "openai":
        return key.startswith("sk-") and len(key) > 20
    elif provider == "anthropic":
        return key.startswith("sk-ant-") and len(key) > 20
    return False
