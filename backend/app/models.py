"""Pydantic models for data validation and serialization."""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


# ==================== Drive Models ====================

class DriveStatus(str, Enum):
    """Drive usage status levels."""
    CRITICAL = "critical"  # >80% used
    WARNING = "warning"    # 50-80% used
    HEALTHY = "healthy"    # <50% used


class Drive(BaseModel):
    """Drive information model."""
    letter: str = Field(..., pattern="^[A-Z]$")
    total_bytes: int = Field(..., ge=0)
    used_bytes: int = Field(..., ge=0)
    free_bytes: int = Field(..., ge=0)
    percent_used: float = Field(..., ge=0, le=100)
    status: DriveStatus
    filesystem: str = "NTFS"


# ==================== Consumer Models ====================

class ConsumerType(str, Enum):
    """Types of space consumers."""
    DOCKER = "docker"
    WSL = "wsl"
    DOWNLOADS = "downloads"
    TEMP = "temp"
    CACHE = "cache"
    OTHER = "other"


class SpaceConsumer(BaseModel):
    """Space consumer information."""
    name: str
    path: str
    size_bytes: int = Field(..., ge=0)
    type: ConsumerType
    last_modified: Optional[datetime] = None


# ==================== Analysis Models ====================

class AnalysisResult(BaseModel):
    """Result of drive analysis."""
    drives: List[Drive]
    top_consumers: List[SpaceConsumer]
    total_recoverable_bytes: int = Field(..., ge=0)
    has_imbalance: bool
    imbalance_message: Optional[str] = None
    analyzed_at: datetime = Field(default_factory=datetime.now)


# ==================== Plan Models ====================

class ActionType(str, Enum):
    """Types of cleanup actions."""
    MOVE = "MOVE"
    PRUNE = "PRUNE"
    DELETE_TO_RECYCLE = "DELETE_TO_RECYCLE"
    EXPORT_IMPORT_WSL = "EXPORT_IMPORT_WSL"
    CLEANUP = "CLEANUP"


class PlanAction(BaseModel):
    """Individual action in a cleanup plan."""
    id: str
    type: ActionType
    description: str
    source_path: Optional[str] = None
    target_path: Optional[str] = None
    size_bytes: int = Field(..., ge=0)
    safety_explanation: str
    rollback_option: str
    command: Optional[str] = None
    estimated_seconds: int = Field(default=60, ge=0)


class RiskLevel(str, Enum):
    """Risk levels for cleanup plans."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Plan(BaseModel):
    """Cleanup plan model."""
    id: str
    name: str
    space_saved_bytes: int = Field(..., ge=0)
    risk_level: RiskLevel
    estimated_minutes: int = Field(..., ge=0)
    rationale: str
    actions: List[PlanAction]
    recommended: bool = False
    created_at: datetime = Field(default_factory=datetime.now)


# ==================== Execution Models ====================

class ExecutionStatus(str, Enum):
    """Execution status states."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class StepStatus(str, Enum):
    """Individual step status."""
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"


class ExecutionStep(BaseModel):
    """Individual execution step."""
    id: str
    action_id: str
    status: StepStatus
    description: str
    progress_percent: Optional[float] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None


class LogLevel(str, Enum):
    """Log entry levels."""
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


class LogEntry(BaseModel):
    """Log entry for execution tracking."""
    timestamp: str
    level: LogLevel
    message: str


class ExecutionProgress(BaseModel):
    """Real-time execution progress."""
    plan_id: str
    overall_percent: float = Field(..., ge=0, le=100)
    current_step: int
    total_steps: int
    steps: List[ExecutionStep]
    logs: List[LogEntry]
    status: ExecutionStatus
    updated_at: datetime = Field(default_factory=datetime.now)


# ==================== Request/Response Models ====================

class ExecuteRequest(BaseModel):
    """Request to execute a plan."""
    plan_id: str
    dry_run: bool = False


class ExecuteResponse(BaseModel):
    """Response after starting execution."""
    execution_id: str
    status: str
    started_at: datetime


# ==================== Settings Models ====================

class UserSettings(BaseModel):
    """User settings model."""
    use_ai: bool = False
    ai_provider: str = "openai"  # openai or anthropic
    api_key: str = ""
    dry_run: bool = False
    use_recycle_bin: bool = True
    create_backups: bool = True
    primary_target_drive: str = "D:"
    secondary_target_drive: str = "F:"
    backup_location: str = "D:\\Backups\\"
    backend_url: str = "http://127.0.0.1:8000"


class UpdateSettingsRequest(BaseModel):
    """Request to update settings."""
    use_ai: Optional[bool] = None
    ai_provider: Optional[str] = None
    api_key: Optional[str] = None
    dry_run: Optional[bool] = None
    use_recycle_bin: Optional[bool] = None
    create_backups: Optional[bool] = None
    primary_target_drive: Optional[str] = None
    secondary_target_drive: Optional[str] = None
    backup_location: Optional[str] = None
