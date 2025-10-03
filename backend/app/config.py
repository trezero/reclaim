"""Application configuration using Pydantic Settings."""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Server Configuration
    host: str = "127.0.0.1"
    port: int = 8000
    reload: bool = True
    log_level: str = "INFO"

    # CORS Settings
    allowed_origins: List[str] = ["http://localhost:1420", "tauri://localhost"]

    # AI Configuration
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    # Storage Settings
    backup_location: str = "D:\\Backups"
    default_target_drive: str = "D:"

    # Safety Settings
    dry_run_default: bool = False
    use_recycle_bin: bool = True
    create_backups: bool = True

    # Database
    database_url: str = "sqlite:///data/executions.db"

    # Logging
    log_file: str = "logs/app.log"
    log_max_bytes: int = 10485760  # 10MB
    log_backup_count: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


# Global settings instance
settings = Settings()
