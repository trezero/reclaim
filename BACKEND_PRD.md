# Product Requirements Document (PRD)
## Storage Manager Backend - Python FastAPI

**Version:** 1.0.0
**Last Updated:** 2025-10-03
**Status:** Ready for Implementation
**Target Platform:** Windows 11

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Project Overview](#project-overview)
3. [System Architecture](#system-architecture)
4. [Functional Requirements](#functional-requirements)
5. [Technical Requirements](#technical-requirements)
6. [API Specifications](#api-specifications)
7. [Data Models](#data-models)
8. [AI Integration](#ai-integration)
9. [Storage Operations](#storage-operations)
10. [Safety & Rollback Mechanisms](#safety--rollback-mechanisms)
11. [Performance Requirements](#performance-requirements)
12. [Security Requirements](#security-requirements)
13. [Testing Requirements](#testing-requirements)
14. [Deployment Guide](#deployment-guide)
15. [Future Enhancements](#future-enhancements)

---

## Executive Summary

The Storage Manager Backend is a **Python FastAPI application** that powers an AI-driven Windows storage optimization tool. It analyzes disk usage, generates intelligent cleanup strategies, and safely executes storage management operations with comprehensive rollback capabilities.

### Key Features
- 🔍 **Real-time drive analysis** - Scan NTFS drives and identify space consumers
- 🤖 **AI-powered recommendations** - Generate 3-tier cleanup plans (Conservative/Balanced/Aggressive)
- ⚡ **Safe execution engine** - Execute operations with backups and rollback support
- 📊 **WebSocket progress** - Real-time updates during execution
- 🔒 **Safety-first design** - Dry-run mode, recycle bin, symlinks, backups

### Target Users
- Windows 11 power users with multiple drives
- Developers with Docker, WSL, and large development environments
- Users experiencing C: drive space issues

---

## Project Overview

### Problem Statement
Windows users frequently face C: drive capacity issues while other drives (D:, F:) remain underutilized. Manual cleanup is time-consuming, risky, and requires technical knowledge. Users need:
- Automated identification of space consumers (Docker, WSL, caches)
- AI-generated cleanup strategies with risk assessment
- Safe execution with rollback capabilities
- Real-time progress monitoring

### Solution
A FastAPI backend that:
1. Analyzes drive usage using `psutil`, `shutil`, and Windows APIs
2. Uses OpenAI/Anthropic to generate context-aware cleanup plans
3. Executes operations (move, delete, cleanup) with comprehensive safety measures
4. Streams progress via WebSockets
5. Maintains execution history and rollback data

### Success Metrics
- Analysis completes in <5 seconds for typical systems
- AI plan generation in <10 seconds
- 95%+ accuracy in space calculations
- Zero data loss in production (with proper backups)
- <100ms API response time for non-blocking endpoints

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Tauri Frontend (React)                   │
│                   (Port 1420 - Dev Mode)                    │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP/WebSocket
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (Python)                   │
│                      (Port 8000)                            │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Analysis   │  │  AI Planner  │  │   Executor   │     │
│  │    Engine    │  │    (LLM)     │  │    Engine    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   Storage    │  │   Progress   │  │   Rollback   │     │
│  │   Scanner    │  │   Manager    │  │   Manager    │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                 Windows File System (NTFS)                  │
│          C:\ (System)  D:\ (Data)  F:\ (Backup)            │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              External Services (Optional)                   │
│         OpenAI API / Anthropic API (Claude)                │
└─────────────────────────────────────────────────────────────┘
```

### Technology Stack

**Core Framework:**
- Python 3.9+ (3.11 recommended)
- FastAPI 0.104+
- Uvicorn (ASGI server)
- Pydantic v2 (data validation)

**Storage & System:**
- `psutil` - Drive info, disk usage
- `shutil` - File operations (move, copy)
- `pathlib` - Path manipulation
- `win32file` / `pywin32` - Windows-specific operations
- `subprocess` - Docker, WSL commands

**AI Integration:**
- `openai` - OpenAI GPT-4 API
- `anthropic` - Claude API
- `tiktoken` - Token counting

**Real-time Communication:**
- `websockets` - WebSocket support
- `asyncio` - Async operations

**Database (Optional):**
- SQLite / TinyDB - Execution history, rollback metadata
- JSON files - Settings persistence

**Testing:**
- `pytest` - Unit tests
- `pytest-asyncio` - Async tests
- `httpx` - API testing
- `faker` - Mock data

---

## Functional Requirements

### FR-1: Drive Analysis

**Description:** Scan all detected drives and identify space consumers.

**Requirements:**
- **FR-1.1** Detect all mounted NTFS drives (C:, D:, F:, etc.)
- **FR-1.2** Calculate total/used/free space per drive
- **FR-1.3** Determine drive status (critical >80%, warning 50-80%, healthy <50%)
- **FR-1.4** Identify top 10 space consumers across all drives
- **FR-1.5** Categorize consumers by type (Docker, WSL, Downloads, Temp, Cache, Other)
- **FR-1.6** Calculate total recoverable space
- **FR-1.7** Detect imbalances (e.g., C: 90% full, D: 10% full)
- **FR-1.8** Complete analysis in <5 seconds

**Acceptance Criteria:**
- All drives detected accurately
- Space calculations match Windows Explorer (±100MB tolerance)
- Top consumers identified correctly
- Imbalance detection works for common scenarios

---

### FR-2: AI Plan Generation

**Description:** Generate 3-tier cleanup strategies using AI or rule-based logic.

**Requirements:**
- **FR-2.1** Generate Conservative plan (low risk, basic cleanup)
- **FR-2.2** Generate Balanced plan (medium risk, recommended)
- **FR-2.3** Generate Aggressive plan (high risk, maximum savings)
- **FR-2.4** Each plan includes:
  - Estimated space saved (bytes)
  - Risk level (low/medium/high)
  - Estimated time (minutes)
  - Rationale (why this plan)
  - List of actions (MOVE, DELETE, CLEANUP, etc.)
- **FR-2.5** Use AI if API key provided, fallback to rule-based
- **FR-2.6** Plans prioritize based on:
  - Current drive usage
  - Available target drives
  - User preferences (from settings)
- **FR-2.7** Generate plans in <10 seconds

**Acceptance Criteria:**
- 3 distinct plans generated
- Conservative plan is always safest
- Balanced plan is marked as recommended
- Aggressive plan saves most space
- AI rationale is contextual and helpful

---

### FR-3: Plan Execution

**Description:** Execute cleanup operations safely with progress tracking.

**Requirements:**
- **FR-3.1** Support dry-run mode (preview without changes)
- **FR-3.2** Create backups before major operations
- **FR-3.3** Execute actions sequentially:
  - MOVE - Move files/folders with symlinks
  - DELETE_TO_RECYCLE - Send to recycle bin
  - CLEANUP - Clear caches/temp files
  - PRUNE - Docker/WSL cleanup commands
  - EXPORT_IMPORT_WSL - Relocate WSL distributions
- **FR-3.4** Update progress in real-time (WebSocket)
- **FR-3.5** Log all operations with timestamps
- **FR-3.6** Handle errors gracefully (pause, rollback)
- **FR-3.7** Support cancellation mid-execution
- **FR-3.8** Verify disk space after each operation

**Acceptance Criteria:**
- All action types execute correctly
- Progress updates every 1-2 seconds
- Errors don't crash the system
- Cancellation stops immediately
- Symlinks work for moved folders

---

### FR-4: Rollback Mechanism

**Description:** Restore system to pre-execution state if needed.

**Requirements:**
- **FR-4.1** Save rollback metadata before each operation
- **FR-4.2** Support rollback for:
  - MOVE operations (reverse move, restore symlink)
  - DELETE operations (restore from recycle bin)
  - WSL exports (re-import from tar)
- **FR-4.3** Rollback executes in reverse order
- **FR-4.4** Provide rollback status via WebSocket
- **FR-4.5** Store rollback data for 7 days
- **FR-4.6** Clean up rollback data after successful execution

**Acceptance Criteria:**
- Rollback restores all moved files
- Symlinks removed during rollback
- Recycle bin items restored correctly
- WSL distributions re-imported successfully

---

### FR-5: Settings Management

**Description:** Persist user preferences and configuration.

**Requirements:**
- **FR-5.1** Store settings in JSON file or SQLite
- **FR-5.2** Settings include:
  - AI enabled (bool)
  - AI provider (openai/anthropic)
  - API key (encrypted)
  - Dry-run mode (bool)
  - Use recycle bin (bool)
  - Create backups (bool)
  - Primary target drive (string)
  - Secondary target drive (string)
  - Backup location (string)
  - Backend URL (string)
- **FR-5.3** Validate settings on update
- **FR-5.4** Load defaults if settings file missing
- **FR-5.5** Encrypt sensitive data (API keys)

**Acceptance Criteria:**
- Settings persist across restarts
- Invalid settings rejected with error message
- API keys stored securely
- Defaults work out-of-the-box

---

### FR-6: WebSocket Progress Updates

**Description:** Stream real-time progress during execution.

**Requirements:**
- **FR-6.1** Establish WebSocket connection per execution
- **FR-6.2** Send updates every 1-2 seconds
- **FR-6.3** Update format includes:
  - Overall progress (%)
  - Current step number / total steps
  - Step statuses (pending/active/completed/failed)
  - Logs (timestamp, level, message)
  - Execution status (running/completed/failed)
- **FR-6.4** Support multiple concurrent connections
- **FR-6.5** Close connection gracefully on completion
- **FR-6.6** Handle client disconnects (pause execution)

**Acceptance Criteria:**
- Progress updates smooth and accurate
- Multiple clients can monitor same execution
- Connection stable for long operations (30+ min)
- Logs appear in real-time

---

## Technical Requirements

### TR-1: Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                  # FastAPI app entry point
│   ├── config.py                # Configuration & settings
│   ├── models.py                # Pydantic models
│   ├── dependencies.py          # Dependency injection
│   │
│   ├── api/                     # API routes
│   │   ├── __init__.py
│   │   ├── analysis.py          # GET /analyze
│   │   ├── plans.py             # GET /plans, /plan/{id}
│   │   ├── execution.py         # POST /execute
│   │   ├── progress.py          # WS /progress/{id}
│   │   └── settings.py          # GET/POST /settings
│   │
│   ├── services/                # Business logic
│   │   ├── __init__.py
│   │   ├── analyzer.py          # Drive analysis engine
│   │   ├── planner.py           # Plan generation (AI + rules)
│   │   ├── executor.py          # Execution engine
│   │   ├── rollback.py          # Rollback manager
│   │   └── progress.py          # Progress tracking
│   │
│   ├── storage/                 # Storage operations
│   │   ├── __init__.py
│   │   ├── scanner.py           # Drive scanning
│   │   ├── mover.py             # File move operations
│   │   ├── cleaner.py           # Cleanup operations
│   │   ├── docker.py            # Docker operations
│   │   └── wsl.py               # WSL operations
│   │
│   ├── ai/                      # AI integration
│   │   ├── __init__.py
│   │   ├── openai_client.py     # OpenAI integration
│   │   ├── anthropic_client.py  # Anthropic integration
│   │   └── prompts.py           # AI prompts
│   │
│   └── utils/                   # Utilities
│       ├── __init__.py
│       ├── logger.py            # Logging setup
│       ├── validators.py        # Input validation
│       └── helpers.py           # Helper functions
│
├── tests/                       # Unit & integration tests
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_planner.py
│   ├── test_executor.py
│   └── test_api.py
│
├── data/                        # Data storage
│   ├── settings.json            # User settings
│   ├── executions.db            # Execution history (SQLite)
│   └── rollback/                # Rollback metadata
│
├── logs/                        # Application logs
│   └── app.log
│
├── requirements.txt             # Python dependencies
├── requirements-dev.txt         # Development dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
├── README.md                    # Backend documentation
└── pytest.ini                   # Pytest configuration
```

### TR-2: Environment Variables

**.env file:**
```bash
# Server Configuration
HOST=127.0.0.1
PORT=8000
RELOAD=true  # Development only
LOG_LEVEL=INFO

# CORS Settings
ALLOWED_ORIGINS=http://localhost:1420,tauri://localhost

# AI Configuration
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Storage Settings
BACKUP_LOCATION=D:\Backups
DEFAULT_TARGET_DRIVE=D:

# Safety Settings
DRY_RUN_DEFAULT=false
USE_RECYCLE_BIN=true
CREATE_BACKUPS=true

# Database
DATABASE_URL=sqlite:///data/executions.db

# Logging
LOG_FILE=logs/app.log
LOG_MAX_BYTES=10485760  # 10MB
LOG_BACKUP_COUNT=5
```

### TR-3: Dependencies

**requirements.txt:**
```txt
# Core Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0

# WebSockets
websockets==12.0

# Storage & System
psutil==5.9.6
pywin32==306  # Windows-specific

# AI Integration
openai==1.3.0
anthropic==0.8.1
tiktoken==0.5.2

# Utilities
python-dotenv==1.0.0
python-multipart==0.0.6
aiofiles==23.2.1

# Database (Optional)
aiosqlite==0.19.0
# or
tinydb==4.8.0

# Cryptography (for API key encryption)
cryptography==41.0.7
```

**requirements-dev.txt:**
```txt
# Testing
pytest==7.4.3
pytest-asyncio==0.21.1
pytest-cov==4.1.0
httpx==0.25.2
faker==20.1.0

# Linting & Formatting
black==23.12.0
ruff==0.1.8
mypy==1.7.1

# Development
ipython==8.18.1
```

---

## API Specifications

### Endpoint 1: Analyze Drives

**`GET /analyze`**

**Description:** Analyze all drives and return usage statistics.

**Request:**
```http
GET /analyze HTTP/1.1
Host: 127.0.0.1:8000
```

**Response:**
```json
{
  "drives": [
    {
      "letter": "C",
      "total_bytes": 500000000000,
      "used_bytes": 450000000000,
      "free_bytes": 50000000000,
      "percent_used": 90.0,
      "status": "critical",
      "filesystem": "NTFS"
    }
  ],
  "top_consumers": [
    {
      "name": "Docker Desktop",
      "path": "C:\\Users\\winadmin\\AppData\\Local\\Docker Desktop",
      "size_bytes": 85200000000,
      "type": "docker",
      "last_modified": "2025-10-01T10:30:00Z"
    }
  ],
  "total_recoverable_bytes": 157200000000,
  "has_imbalance": true,
  "imbalance_message": "C: drive is 90% full while D: has 880GB free",
  "analyzed_at": "2025-10-03T14:23:15Z"
}
```

**Implementation Details:**
```python
from fastapi import APIRouter
from app.services.analyzer import DriveAnalyzer

router = APIRouter()

@router.get("/analyze")
async def analyze_drives():
    analyzer = DriveAnalyzer()
    result = await analyzer.analyze()
    return result
```

**Error Codes:**
- `200 OK` - Success
- `500 Internal Server Error` - Analysis failed

---

### Endpoint 2: Get Plans

**`GET /plans`**

**Description:** Generate 3 cleanup plans (Conservative, Balanced, Aggressive).

**Query Parameters:**
- `use_ai` (optional, bool) - Force AI or rule-based generation

**Request:**
```http
GET /plans?use_ai=true HTTP/1.1
Host: 127.0.0.1:8000
```

**Response:**
```json
[
  {
    "id": "conservative",
    "name": "Conservative",
    "space_saved_bytes": 45200000000,
    "risk_level": "low",
    "estimated_minutes": 15,
    "rationale": "Clean temporary files and caches only...",
    "recommended": false,
    "actions": [
      {
        "id": "action_1",
        "type": "CLEANUP",
        "description": "Clear Browser Caches",
        "size_bytes": 8900000000,
        "safety_explanation": "Browsers will rebuild cache automatically",
        "rollback_option": "Not needed (cache data)",
        "estimated_seconds": 120
      }
    ],
    "created_at": "2025-10-03T14:25:00Z"
  }
]
```

**Implementation Details:**
```python
@router.get("/plans")
async def get_plans(
    use_ai: bool = None,
    settings: Settings = Depends(get_settings)
):
    planner = PlanGenerator(settings)
    plans = await planner.generate_plans(force_ai=use_ai)
    return plans
```

---

### Endpoint 3: Get Plan Details

**`GET /plan/{plan_id}`**

**Description:** Get detailed information for a specific plan.

**Path Parameters:**
- `plan_id` (string) - Plan ID (conservative/balanced/aggressive)

**Request:**
```http
GET /plan/balanced HTTP/1.1
Host: 127.0.0.1:8000
```

**Response:**
Same as single plan object from `/plans`

---

### Endpoint 4: Execute Plan

**`POST /execute`**

**Description:** Start execution of a cleanup plan.

**Request:**
```json
{
  "plan_id": "balanced",
  "dry_run": false
}
```

**Response:**
```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "started",
  "started_at": "2025-10-03T14:30:00Z"
}
```

**Implementation Details:**
```python
from app.services.executor import ExecutionEngine

@router.post("/execute")
async def execute_plan(
    request: ExecuteRequest,
    background_tasks: BackgroundTasks
):
    execution_id = str(uuid.uuid4())
    executor = ExecutionEngine(execution_id, request.plan_id)

    # Run in background
    background_tasks.add_task(
        executor.execute,
        dry_run=request.dry_run
    )

    return {
        "execution_id": execution_id,
        "status": "started",
        "started_at": datetime.now().isoformat()
    }
```

---

### Endpoint 5: Progress WebSocket

**`WS /progress/{execution_id}`**

**Description:** Real-time progress updates via WebSocket.

**Connection:**
```javascript
const ws = new WebSocket('ws://127.0.0.1:8000/progress/550e8400-...')
```

**Message Format:**
```json
{
  "plan_id": "balanced",
  "overall_percent": 65,
  "current_step": 3,
  "total_steps": 5,
  "status": "running",
  "steps": [
    {
      "id": "step_1",
      "action_id": "action_3",
      "status": "completed",
      "description": "Backup created",
      "progress_percent": 100,
      "started_at": "2025-10-03T14:30:05Z",
      "completed_at": "2025-10-03T14:30:15Z"
    }
  ],
  "logs": [
    {
      "timestamp": "14:30:15",
      "level": "info",
      "message": "Starting Docker data migration..."
    }
  ],
  "updated_at": "2025-10-03T14:30:30Z"
}
```

**Implementation Details:**
```python
from fastapi import WebSocket
from app.services.progress import ProgressManager

@router.websocket("/progress/{execution_id}")
async def progress_websocket(
    websocket: WebSocket,
    execution_id: str
):
    await websocket.accept()
    progress_manager = ProgressManager(execution_id)

    try:
        while True:
            progress = await progress_manager.get_progress()
            await websocket.send_json(progress)

            if progress["status"] in ["completed", "failed", "cancelled"]:
                break

            await asyncio.sleep(1)  # Update every second
    except WebSocketDisconnect:
        pass
    finally:
        await websocket.close()
```

---

### Endpoint 6: Get Settings

**`GET /settings`**

**Description:** Retrieve user settings.

**Response:**
```json
{
  "use_ai": true,
  "ai_provider": "openai",
  "api_key": "sk-...",
  "dry_run": false,
  "use_recycle_bin": true,
  "create_backups": true,
  "primary_target_drive": "D:",
  "secondary_target_drive": "F:",
  "backup_location": "D:\\Backups\\",
  "backend_url": "http://127.0.0.1:8000"
}
```

---

### Endpoint 7: Update Settings

**`POST /settings`**

**Description:** Update user settings.

**Request:**
```json
{
  "use_ai": true,
  "ai_provider": "anthropic",
  "api_key": "sk-ant-...",
  "dry_run": true
}
```

**Response:**
Updated settings object (same as GET /settings)

---

## Data Models

### Drive Model

```python
from pydantic import BaseModel, Field
from enum import Enum

class DriveStatus(str, Enum):
    CRITICAL = "critical"  # >80% used
    WARNING = "warning"    # 50-80% used
    HEALTHY = "healthy"    # <50% used

class Drive(BaseModel):
    letter: str = Field(..., pattern="^[A-Z]$")
    total_bytes: int = Field(..., ge=0)
    used_bytes: int = Field(..., ge=0)
    free_bytes: int = Field(..., ge=0)
    percent_used: float = Field(..., ge=0, le=100)
    status: DriveStatus
    filesystem: str = "NTFS"
```

### Consumer Model

```python
class ConsumerType(str, Enum):
    DOCKER = "docker"
    WSL = "wsl"
    DOWNLOADS = "downloads"
    TEMP = "temp"
    CACHE = "cache"
    OTHER = "other"

class SpaceConsumer(BaseModel):
    name: str
    path: str
    size_bytes: int = Field(..., ge=0)
    type: ConsumerType
    last_modified: Optional[datetime] = None
```

### Plan Model

```python
class ActionType(str, Enum):
    MOVE = "MOVE"
    PRUNE = "PRUNE"
    DELETE_TO_RECYCLE = "DELETE_TO_RECYCLE"
    EXPORT_IMPORT_WSL = "EXPORT_IMPORT_WSL"
    CLEANUP = "CLEANUP"

class PlanAction(BaseModel):
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
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Plan(BaseModel):
    id: str
    name: str
    space_saved_bytes: int = Field(..., ge=0)
    risk_level: RiskLevel
    estimated_minutes: int = Field(..., ge=0)
    rationale: str
    actions: List[PlanAction]
    recommended: bool = False
    created_at: datetime = Field(default_factory=datetime.now)
```

### Execution Model

```python
class ExecutionStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class StepStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"

class ExecutionStep(BaseModel):
    id: str
    action_id: str
    status: StepStatus
    description: str
    progress_percent: Optional[float] = None
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class LogLevel(str, Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"

class LogEntry(BaseModel):
    timestamp: str
    level: LogLevel
    message: str

class ExecutionProgress(BaseModel):
    plan_id: str
    overall_percent: float = Field(..., ge=0, le=100)
    current_step: int
    total_steps: int
    steps: List[ExecutionStep]
    logs: List[LogEntry]
    status: ExecutionStatus
    updated_at: datetime = Field(default_factory=datetime.now)
```

---

## AI Integration

### AI Provider Selection

**Decision Logic:**
1. Check if `use_ai` is enabled in settings
2. If disabled, use rule-based generation
3. If enabled, check `ai_provider` (openai/anthropic)
4. Validate API key exists
5. Call appropriate AI service
6. Fallback to rules if AI fails

### OpenAI Integration

**Model:** GPT-4 or GPT-4-Turbo
**Temperature:** 0.7
**Max Tokens:** 2000

**Prompt Structure:**
```python
PLAN_GENERATION_PROMPT = """
You are a Windows storage optimization expert. Analyze the following drive usage data and generate 3 cleanup plans.

Drive Analysis:
{drive_data}

Top Space Consumers:
{consumers_data}

User Settings:
- Primary target drive: {target_drive}
- Backup location: {backup_location}

Generate 3 plans:
1. Conservative (low risk, basic cleanup)
2. Balanced (medium risk, recommended)
3. Aggressive (high risk, maximum savings)

For each plan, provide:
- Specific actions (MOVE, DELETE, CLEANUP, PRUNE)
- Space savings estimate
- Risk assessment
- Detailed rationale
- Safety explanations

Return valid JSON matching this schema:
{schema}
"""
```

**Error Handling:**
- Timeout: 30 seconds
- Retry: 2 times with exponential backoff
- Fallback: Rule-based generation

### Anthropic Integration

**Model:** Claude 3 Opus or Sonnet
**Max Tokens:** 4000

Similar prompt structure, adjusted for Claude's style.

### Rule-Based Fallback

If AI unavailable, use predefined rules:

**Conservative:**
- Clear browser caches (all browsers)
- Delete Windows temp files
- Clean download folder (files >30 days old)

**Balanced:**
- All Conservative actions
- Move Docker data to D: drive
- Clean WSL distributions (unused)

**Aggressive:**
- All Balanced actions
- Relocate Downloads folder
- Relocate user folders (Documents, Pictures if large)
- Export and move all WSL distributions

---

## Storage Operations

### Operation 1: Move Files/Folders

**Implementation:**

```python
import shutil
import os
from pathlib import Path

async def move_with_symlink(
    source: Path,
    target: Path,
    create_backup: bool = True
) -> Dict[str, Any]:
    """
    Move folder and create symlink at source location.
    """
    # Validate paths
    if not source.exists():
        raise FileNotFoundError(f"Source not found: {source}")

    # Create backup if enabled
    if create_backup:
        backup_path = await create_backup(source)

    # Move files
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(target))

    # Create symlink
    os.symlink(str(target), str(source), target_is_directory=True)

    return {
        "source": str(source),
        "target": str(target),
        "symlink_created": True,
        "backup_path": str(backup_path) if create_backup else None
    }
```

**Safety Measures:**
- Verify sufficient space on target drive
- Create backup before moving
- Use symlink to maintain compatibility
- Log all operations
- Support rollback (reverse move + delete symlink)

---

### Operation 2: Delete to Recycle Bin

**Implementation:**

```python
from win32com.shell import shell, shellcon

async def delete_to_recycle_bin(path: Path) -> Dict[str, Any]:
    """
    Send file/folder to Windows Recycle Bin.
    """
    result = shell.SHFileOperation((
        0,  # hwnd
        shellcon.FO_DELETE,  # operation
        str(path),  # source
        None,  # target
        shellcon.FOF_ALLOWUNDO | shellcon.FOF_NOCONFIRMATION,  # flags
        None,  # progress title
        None   # progress
    ))

    if result[0] != 0:
        raise Exception(f"Failed to delete: {result}")

    return {
        "path": str(path),
        "in_recycle_bin": True,
        "recoverable": True
    }
```

---

### Operation 3: Docker Operations

**Implementation:**

```python
import subprocess

async def move_docker_data(target_drive: str) -> Dict[str, Any]:
    """
    Move Docker Desktop data to target drive.
    """
    # Stop Docker
    subprocess.run(["docker", "stop"], check=True)

    # Move data
    docker_data = Path.home() / "AppData/Local/Docker Desktop"
    target_path = Path(f"{target_drive}/Docker")

    await move_with_symlink(docker_data, target_path)

    # Start Docker
    subprocess.run(["docker", "start"], check=True)

    return {
        "original_path": str(docker_data),
        "new_path": str(target_path),
        "service_restarted": True
    }

async def prune_docker() -> Dict[str, Any]:
    """
    Clean up Docker unused data.
    """
    result = subprocess.run(
        ["docker", "system", "prune", "-af", "--volumes"],
        capture_output=True,
        text=True
    )

    # Parse output for space reclaimed
    space_reclaimed = parse_docker_output(result.stdout)

    return {
        "space_reclaimed_bytes": space_reclaimed,
        "output": result.stdout
    }
```

---

### Operation 4: WSL Operations

**Implementation:**

```python
async def export_wsl_distro(
    distro_name: str,
    target_drive: str
) -> Dict[str, Any]:
    """
    Export WSL distribution to target drive.
    """
    export_path = Path(f"{target_drive}/WSL/{distro_name}.tar")
    export_path.parent.mkdir(parents=True, exist_ok=True)

    # Export
    subprocess.run([
        "wsl",
        "--export",
        distro_name,
        str(export_path)
    ], check=True)

    # Unregister original
    subprocess.run([
        "wsl",
        "--unregister",
        distro_name
    ], check=True)

    # Import to new location
    import_path = Path(f"{target_drive}/WSL/{distro_name}")
    subprocess.run([
        "wsl",
        "--import",
        distro_name,
        str(import_path),
        str(export_path)
    ], check=True)

    return {
        "distro": distro_name,
        "exported_to": str(export_path),
        "imported_to": str(import_path)
    }
```

---

### Operation 5: Cache Cleanup

**Implementation:**

```python
async def clear_browser_caches() -> Dict[str, Any]:
    """
    Clear caches for Chrome, Edge, Firefox.
    """
    cache_paths = [
        Path.home() / "AppData/Local/Google/Chrome/User Data/Default/Cache",
        Path.home() / "AppData/Local/Microsoft/Edge/User Data/Default/Cache",
        Path.home() / "AppData/Local/Mozilla/Firefox/Profiles/*/cache2",
    ]

    total_cleared = 0

    for cache_path in cache_paths:
        if cache_path.exists():
            size = get_dir_size(cache_path)
            shutil.rmtree(cache_path, ignore_errors=True)
            total_cleared += size

    return {
        "browsers_cleared": 3,
        "space_cleared_bytes": total_cleared
    }

async def clear_temp_files() -> Dict[str, Any]:
    """
    Clear Windows temp files.
    """
    temp_paths = [
        Path("C:/Windows/Temp"),
        Path.home() / "AppData/Local/Temp",
    ]

    total_cleared = 0

    for temp_path in temp_paths:
        if temp_path.exists():
            for item in temp_path.iterdir():
                try:
                    if item.is_file():
                        size = item.stat().st_size
                        item.unlink()
                        total_cleared += size
                    elif item.is_dir():
                        size = get_dir_size(item)
                        shutil.rmtree(item, ignore_errors=True)
                        total_cleared += size
                except Exception:
                    pass  # Skip locked files

    return {
        "locations_cleared": len(temp_paths),
        "space_cleared_bytes": total_cleared
    }
```

---

## Safety & Rollback Mechanisms

### Backup Strategy

**Before Each Major Operation:**
1. Calculate backup size
2. Verify target has sufficient space
3. Create timestamped backup folder
4. Copy files to backup location
5. Store metadata (source, target, timestamp)
6. Validate backup integrity

**Backup Retention:**
- Keep for 7 days after successful execution
- Clean up automatically
- User can trigger manual cleanup

### Rollback Implementation

**Rollback Metadata:**
```json
{
  "execution_id": "uuid",
  "plan_id": "balanced",
  "started_at": "2025-10-03T14:30:00Z",
  "operations": [
    {
      "id": "op_1",
      "type": "MOVE",
      "source": "C:\\Users\\...",
      "target": "D:\\Docker",
      "backup_path": "D:\\Backups\\20251003_143000",
      "symlink_created": true,
      "completed": true
    }
  ]
}
```

**Rollback Process:**
```python
async def rollback_execution(execution_id: str) -> Dict[str, Any]:
    """
    Rollback all operations for an execution.
    """
    metadata = load_rollback_metadata(execution_id)

    # Reverse order
    for operation in reversed(metadata["operations"]):
        if operation["type"] == "MOVE":
            # Remove symlink
            if operation["symlink_created"]:
                os.remove(operation["source"])

            # Move back
            shutil.move(operation["target"], operation["source"])

        elif operation["type"] == "DELETE_TO_RECYCLE":
            # Restore from recycle bin
            restore_from_recycle_bin(operation["path"])

        elif operation["type"] == "EXPORT_IMPORT_WSL":
            # Re-import from backup tar
            reimport_wsl(operation["distro"], operation["backup_tar"])

    return {
        "execution_id": execution_id,
        "operations_rolled_back": len(metadata["operations"]),
        "status": "success"
    }
```

---

## Performance Requirements

### Response Time Targets

| Endpoint | Target | Acceptable | Max |
|----------|--------|------------|-----|
| GET /analyze | <3s | <5s | 10s |
| GET /plans | <5s | <10s | 20s |
| POST /execute | <100ms | <500ms | 1s |
| WS updates | Every 1-2s | Every 3s | Every 5s |

### Resource Limits

**Memory:**
- Baseline: <100MB
- Peak (during execution): <500MB
- Maximum: 1GB

**CPU:**
- Idle: <1%
- Analysis: <30%
- Execution: <50%

**Disk I/O:**
- Move operations: Limited by drive speed
- Progress: Batch disk writes (every 5s)

### Optimization Strategies

1. **Caching:**
   - Cache drive analysis for 30 seconds
   - Cache plan generation for 5 minutes

2. **Async Operations:**
   - Use `asyncio` for all I/O
   - Background tasks for execution

3. **Progress Updates:**
   - Batch updates (send every 1-2s, not every file)
   - Use in-memory queue

4. **File Operations:**
   - Use `shutil` with buffer size optimization
   - Parallel file copying (if multiple targets)

---

## Security Requirements

### Authentication (Future)

Current version: No authentication (localhost only)

Future:
- API key authentication
- JWT tokens for WebSocket
- Rate limiting

### Data Protection

**API Keys:**
- Encrypt using `cryptography.fernet`
- Store in secure location
- Never log or expose in responses

**File Permissions:**
- Validate user has permission before operations
- Use Windows ACLs
- Respect system files

**Input Validation:**
- Sanitize all file paths
- Prevent directory traversal
- Validate drive letters
- Whitelist allowed operations

### CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:1420",  # Vite dev
        "tauri://localhost",      # Tauri production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Testing Requirements

### Unit Tests

**Coverage Target:** 80%+

**Test Categories:**
1. **Analyzer Tests** (`test_analyzer.py`)
   - Drive detection
   - Space calculation
   - Consumer identification
   - Imbalance detection

2. **Planner Tests** (`test_planner.py`)
   - Rule-based generation
   - AI integration (mocked)
   - Plan validation
   - Risk assessment

3. **Executor Tests** (`test_executor.py`)
   - Action execution (mocked file ops)
   - Progress tracking
   - Error handling
   - Cancellation

4. **Rollback Tests** (`test_rollback.py`)
   - Metadata creation
   - Rollback execution
   - Integrity verification

### Integration Tests

**Test Scenarios:**
1. Full flow: Analyze → Generate → Execute → Rollback
2. WebSocket connection and updates
3. Dry-run mode
4. Error recovery

### Mock Data

```python
# tests/fixtures.py

@pytest.fixture
def mock_drive_data():
    return {
        "drives": [
            {
                "letter": "C",
                "total_bytes": 500_000_000_000,
                "used_bytes": 450_000_000_000,
                "free_bytes": 50_000_000_000,
                "percent_used": 90.0,
                "status": "critical"
            }
        ]
    }

@pytest.fixture
def mock_settings():
    return {
        "use_ai": False,
        "dry_run": True,
        "use_recycle_bin": True,
        "create_backups": True,
        "primary_target_drive": "D:"
    }
```

### Test Execution

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_analyzer.py -v

# Run with markers
pytest -m "slow"  # Only slow tests
pytest -m "not slow"  # Skip slow tests
```

---

## Deployment Guide

### Development Setup

```bash
# 1. Clone repository
git clone <backend-repo>
cd backend

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 4. Configure environment
copy .env.example .env
# Edit .env with your settings

# 5. Run development server
uvicorn app.main:app --reload --port 8000

# Server runs at http://127.0.0.1:8000
# Swagger docs at http://127.0.0.1:8000/docs
```

### Production Deployment

**Option 1: Windows Service (using NSSM)**

```bash
# Install NSSM
choco install nssm

# Create service
nssm install StorageManagerBackend "C:\path\to\venv\Scripts\python.exe" "-m uvicorn app.main:app --host 127.0.0.1 --port 8000"

# Start service
nssm start StorageManagerBackend
```

**Option 2: Docker (if needed)**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app
COPY data ./data

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Option 3: Standalone Executable (PyInstaller)**

```bash
pip install pyinstaller

pyinstaller --onefile --name storage-manager-backend app/main.py
```

### Health Checks

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }
```

---

## Future Enhancements

### Phase 2 Features

1. **Scheduled Cleanups**
   - Cron-like scheduling
   - Weekly/monthly automatic runs
   - Email notifications

2. **Cloud Backup Integration**
   - OneDrive sync before cleanup
   - Google Drive backup option
   - S3 backup for critical data

3. **Advanced Analytics**
   - Trend analysis (space usage over time)
   - Predictive alerts (C: will be full in 30 days)
   - Recommendations based on history

4. **Multi-User Support**
   - User profiles
   - Shared settings
   - Audit logs

5. **Enhanced AI**
   - Learn from user preferences
   - Personalized recommendations
   - Natural language queries

6. **Cross-Platform**
   - Linux support
   - macOS support
   - Unified codebase

---

## Appendix

### A. Sample AI Prompt

```
System: You are a Windows storage optimization expert with deep knowledge of Windows file systems, common applications (Docker, WSL, IDEs), and safe file operations.

User: Analyze this drive data and generate 3 cleanup plans:

Drive C: 500GB total, 450GB used (90%)
- Docker Desktop: 85GB
- WSL Ubuntu: 32GB
- Downloads: 18GB
- Temp files: 12GB
- Browser caches: 9GB

Drive D: 1TB total, 120GB used (12%)
Drive F: 500GB total, 200GB used (40%)

Primary target: D:
User prefers: Balanced risk, automatic backups enabled

Generate plans in JSON format with specific actions, safety explanations, and rollback options.
```

### B. Error Codes Reference

| Code | Description | Action |
|------|-------------|--------|
| 1001 | Drive not found | Verify drive letter |
| 1002 | Insufficient space | Free space on target |
| 1003 | Permission denied | Run as administrator |
| 2001 | AI API timeout | Use rule-based fallback |
| 2002 | Invalid API key | Update settings |
| 3001 | Execution failed | Check logs, rollback |
| 3002 | Symlink creation failed | Check permissions |
| 4001 | Rollback failed | Manual intervention needed |

### C. Logging Standards

```python
import logging

# Log levels
logging.info("Starting analysis...")
logging.warning("Drive C: is 90% full")
logging.error("Failed to move file: permission denied")
logging.critical("Execution aborted due to critical error")

# Log format
# [2025-10-03 14:30:15] [INFO] [analyzer] Starting drive analysis
# [2025-10-03 14:30:16] [WARNING] [analyzer] C: drive critical (90%)
```

### D. Performance Benchmarks

Based on typical Windows 11 system:
- **Analysis:** 2-3 seconds
- **Plan Generation (AI):** 5-8 seconds
- **Plan Generation (Rules):** <1 second
- **Move 50GB:** 5-10 minutes (HDD to SSD)
- **Delete temp files:** 30-60 seconds
- **WSL export:** 2-5 minutes per distro

---

## Document History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2025-10-03 | AI Assistant | Initial PRD |

---

## Sign-off

**Product Owner:** [Name]
**Engineering Lead:** [Name]
**Date:** [Date]

---

**End of Document**
