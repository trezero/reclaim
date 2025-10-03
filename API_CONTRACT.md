# Backend API Contract

This document defines the API contract between the Tauri frontend and the Python FastAPI backend.

## Base URL

```
http://127.0.0.1:8000
```

---

## Endpoints

### 1. Analysis - `GET /analyze`

Returns drive analysis and top space consumers.

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
      "status": "critical"
    },
    {
      "letter": "D",
      "total_bytes": 1000000000000,
      "used_bytes": 120000000000,
      "free_bytes": 880000000000,
      "percent_used": 12.0,
      "status": "healthy"
    },
    {
      "letter": "F",
      "total_bytes": 500000000000,
      "used_bytes": 200000000000,
      "free_bytes": 300000000000,
      "percent_used": 40.0,
      "status": "warning"
    }
  ],
  "top_consumers": [
    {
      "name": "Docker Desktop",
      "path": "C:\\Users\\winadmin\\AppData\\Local\\Docker Desktop",
      "size_bytes": 85200000000,
      "type": "docker"
    },
    {
      "name": "WSL Distributions",
      "path": "C:\\Users\\winadmin\\AppData\\Local\\Packages\\CanonicalGroupLimited.Ubuntu",
      "size_bytes": 32100000000,
      "type": "wsl"
    },
    {
      "name": "Downloads Folder",
      "path": "C:\\Users\\winadmin\\Downloads",
      "size_bytes": 18700000000,
      "type": "downloads"
    },
    {
      "name": "Temp Files",
      "path": "C:\\Windows\\Temp",
      "size_bytes": 12300000000,
      "type": "temp"
    },
    {
      "name": "Browser Caches",
      "path": "C:\\Users\\winadmin\\AppData\\Local\\Google\\Chrome",
      "size_bytes": 8900000000,
      "type": "cache"
    }
  ],
  "total_recoverable_bytes": 157200000000,
  "has_imbalance": true,
  "imbalance_message": "C: drive is 90% full while D: has 880GB free"
}
```

**Status Codes:**
- `200 OK` - Success
- `500 Internal Server Error` - Analysis failed

---

### 2. Get Plans - `GET /plans`

Returns 3 AI-generated cleanup plans.

**Response:**
```json
[
  {
    "id": "conservative",
    "name": "Conservative",
    "space_saved_bytes": 45200000000,
    "risk_level": "low",
    "estimated_minutes": 15,
    "rationale": "Clean temporary files and caches only. Safest option with minimal changes to your system.",
    "recommended": false,
    "actions": [
      {
        "id": "action_1",
        "type": "CLEANUP",
        "description": "Clear Browser Caches",
        "size_bytes": 8900000000,
        "safety_explanation": "Browsers will rebuild cache automatically",
        "rollback_option": "Not needed (cache data)"
      },
      {
        "id": "action_2",
        "type": "DELETE_TO_RECYCLE",
        "description": "Clean Temp Files",
        "source_path": "C:\\Windows\\Temp",
        "size_bytes": 12300000000,
        "safety_explanation": "Temp files are safe to delete",
        "rollback_option": "Restore from Recycle Bin if needed"
      }
    ]
  },
  {
    "id": "balanced",
    "name": "Balanced",
    "space_saved_bytes": 78900000000,
    "risk_level": "medium",
    "estimated_minutes": 25,
    "rationale": "Move Docker to D: drive and perform cleanup. Balanced approach with good space savings.",
    "recommended": true,
    "actions": [
      {
        "id": "action_3",
        "type": "MOVE",
        "description": "Move Docker Desktop Data",
        "source_path": "C:\\Users\\winadmin\\AppData\\Local\\Docker Desktop",
        "target_path": "D:\\Docker",
        "size_bytes": 45200000000,
        "safety_explanation": "Docker will auto-detect new location",
        "rollback_option": "Symlink preserved for easy revert"
      },
      {
        "id": "action_4",
        "type": "CLEANUP",
        "description": "Clear Browser Caches",
        "size_bytes": 8900000000,
        "safety_explanation": "Browsers will rebuild cache automatically",
        "rollback_option": "Not needed (cache data)"
      },
      {
        "id": "action_5",
        "type": "DELETE_TO_RECYCLE",
        "description": "Clean Temp Files",
        "source_path": "C:\\Windows\\Temp",
        "size_bytes": 12300000000,
        "safety_explanation": "Temp files are safe to delete",
        "rollback_option": "Restore from Recycle Bin if needed"
      }
    ]
  },
  {
    "id": "aggressive",
    "name": "Aggressive",
    "space_saved_bytes": 125300000000,
    "risk_level": "high",
    "estimated_minutes": 45,
    "rationale": "Relocate user folders and perform full cleanup. Maximum space savings with higher complexity.",
    "recommended": false,
    "actions": [
      {
        "id": "action_6",
        "type": "MOVE",
        "description": "Move Docker Desktop Data",
        "source_path": "C:\\Users\\winadmin\\AppData\\Local\\Docker Desktop",
        "target_path": "D:\\Docker",
        "size_bytes": 45200000000,
        "safety_explanation": "Docker will auto-detect new location",
        "rollback_option": "Symlink preserved for easy revert"
      },
      {
        "id": "action_7",
        "type": "EXPORT_IMPORT_WSL",
        "description": "Export & Relocate WSL Distributions",
        "source_path": "C:\\Users\\winadmin\\AppData\\Local\\Packages",
        "target_path": "D:\\WSL",
        "size_bytes": 32100000000,
        "command": "wsl --export Ubuntu D:\\WSL\\ubuntu.tar && wsl --import Ubuntu D:\\WSL\\Ubuntu D:\\WSL\\ubuntu.tar",
        "safety_explanation": "WSL data exported before relocation",
        "rollback_option": "Re-import from exported tar file"
      },
      {
        "id": "action_8",
        "type": "MOVE",
        "description": "Move Downloads Folder",
        "source_path": "C:\\Users\\winadmin\\Downloads",
        "target_path": "D:\\Downloads",
        "size_bytes": 18700000000,
        "safety_explanation": "Windows will update folder location",
        "rollback_option": "Restore original path in folder properties"
      }
    ]
  }
]
```

**Status Codes:**
- `200 OK` - Success
- `500 Internal Server Error` - Plan generation failed

---

### 3. Get Plan Details - `GET /plan/{plan_id}`

Returns detailed information for a specific plan.

**Parameters:**
- `plan_id` (path) - Plan ID (e.g., "balanced")

**Response:**
Same structure as single plan object from `/plans` endpoint.

**Status Codes:**
- `200 OK` - Success
- `404 Not Found` - Plan not found
- `500 Internal Server Error` - Failed to fetch plan

---

### 4. Execute Plan - `POST /execute`

Starts execution of a cleanup plan.

**Request Body:**
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
  "status": "started"
}
```

**Status Codes:**
- `200 OK` - Execution started
- `400 Bad Request` - Invalid plan_id
- `500 Internal Server Error` - Execution failed to start

---

### 5. Progress WebSocket - `WS /progress/{execution_id}`

WebSocket endpoint for live progress updates.

**Connection:**
```javascript
const ws = new WebSocket('ws://127.0.0.1:8000/progress/550e8400-e29b-41d4-a716-446655440000')
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
      "progress_percent": 100
    },
    {
      "id": "step_2",
      "action_id": "action_3",
      "status": "completed",
      "description": "Docker service stopped",
      "progress_percent": 100
    },
    {
      "id": "step_3",
      "action_id": "action_3",
      "status": "active",
      "description": "Moving Docker data...",
      "progress_percent": 65
    },
    {
      "id": "step_4",
      "action_id": "action_4",
      "status": "pending",
      "description": "Clear browser caches"
    },
    {
      "id": "step_5",
      "action_id": "action_3",
      "status": "pending",
      "description": "Restart Docker service"
    }
  ],
  "logs": [
    {
      "timestamp": "14:23:15",
      "level": "info",
      "message": "Starting Docker data migration..."
    },
    {
      "timestamp": "14:23:16",
      "level": "info",
      "message": "Creating backup at D:\\Backups\\docker_backup"
    },
    {
      "timestamp": "14:23:45",
      "level": "info",
      "message": "Stopping Docker Desktop service..."
    },
    {
      "timestamp": "14:23:52",
      "level": "success",
      "message": "Service stopped successfully"
    },
    {
      "timestamp": "14:23:53",
      "level": "info",
      "message": "Moving files: 29.2 GB of 45.2 GB copied..."
    }
  ]
}
```

**Status Values:**
- `running` - Execution in progress
- `completed` - All steps completed successfully
- `failed` - Execution failed
- `cancelled` - User cancelled execution

**Step Status Values:**
- `pending` - Not started yet
- `active` - Currently executing
- `completed` - Successfully finished
- `failed` - Step failed with error

**Log Levels:**
- `info` - Information message
- `success` - Success message
- `warning` - Warning message
- `error` - Error message

---

### 6. Get Settings - `GET /settings`

Returns user settings.

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

**Status Codes:**
- `200 OK` - Success
- `500 Internal Server Error` - Failed to fetch settings

---

### 7. Update Settings - `POST /settings`

Updates user settings.

**Request Body:**
```json
{
  "use_ai": true,
  "ai_provider": "anthropic",
  "api_key": "sk-ant-...",
  "dry_run": true,
  "use_recycle_bin": true,
  "create_backups": true,
  "primary_target_drive": "D:",
  "secondary_target_drive": "F:",
  "backup_location": "D:\\Backups\\",
  "backend_url": "http://127.0.0.1:8000"
}
```

**Response:**
Same as GET /settings (updated settings)

**Status Codes:**
- `200 OK` - Settings updated
- `400 Bad Request` - Invalid settings
- `500 Internal Server Error` - Update failed

---

## Data Types

### Drive Status
- `critical` - 80%+ usage (red)
- `warning` - 50-79% usage (orange/yellow)
- `healthy` - <50% usage (green)

### Risk Level
- `low` - Minimal risk, basic operations
- `medium` - Moderate risk, some system changes
- `high` - Higher risk, significant changes

### Action Types
- `MOVE` - Move files/folders to another location
- `CLEANUP` - Clear caches/temp files
- `DELETE_TO_RECYCLE` - Delete files to recycle bin
- `EXPORT_IMPORT_WSL` - Export and relocate WSL distributions
- `PRUNE` - Docker/system cleanup commands

### Consumer Types
- `docker` - Docker Desktop data
- `wsl` - WSL distributions
- `downloads` - Downloads folder
- `temp` - Temporary files
- `cache` - Browser/app caches
- `other` - Other space consumers

---

## Error Handling

All endpoints should return appropriate HTTP status codes and error messages:

```json
{
  "error": "Error message",
  "detail": "Detailed error information",
  "code": "ERROR_CODE"
}
```

Common error codes:
- `ANALYSIS_FAILED` - Drive analysis failed
- `PLAN_NOT_FOUND` - Requested plan doesn't exist
- `EXECUTION_FAILED` - Execution failed to start
- `INVALID_SETTINGS` - Settings validation failed
- `BACKEND_ERROR` - Internal server error

---

## Testing with Mock Data

For development without a Python backend, you can use a mock server or tools like `json-server`:

```bash
npm install -g json-server

# Create db.json with mock data
json-server --watch db.json --port 8000
```

Or use the frontend's error states to develop UI components independently.
