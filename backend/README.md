# Storage Manager Backend

AI-powered Windows storage optimization API built with FastAPI.

## Overview

This backend powers an intelligent storage management application that:
- 🔍 Analyzes drive usage and identifies space consumers
- 🤖 Generates AI-powered cleanup strategies (Conservative/Balanced/Aggressive)
- ⚡ Safely executes operations with rollback support
- 📊 Provides real-time WebSocket progress updates
- 🔒 Implements safety-first design with dry-run mode

## Features

- **Drive Analysis**: Scan all NTFS drives, calculate usage, identify top consumers
- **AI Plan Generation**: Uses OpenAI GPT-4 or Anthropic Claude for intelligent recommendations
- **Rule-Based Fallback**: Works without AI API keys using predefined strategies
- **Safe Execution**: Dry-run mode, recycle bin, symlinks, backups, rollback support
- **Real-time Updates**: WebSocket-based progress tracking
- **Settings Management**: Persistent user preferences

## Quick Start

### Prerequisites

- Python 3.9+ (3.11 recommended)
- Windows 11
- pip

### Installation

1. **Clone and navigate**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   copy .env.example .env
   ```

   Edit `.env` and add your settings:
   ```env
   OPENAI_API_KEY=sk-...
   # or
   ANTHROPIC_API_KEY=sk-ant-...
   ```

5. **Run the server**
   ```bash
   python -m uvicorn app.main:app --reload
   ```

   Server runs at: `http://127.0.0.1:8000`
   API docs at: `http://127.0.0.1:8000/docs`

## API Endpoints

### Analysis
- `GET /analyze` - Analyze all drives and identify space consumers

### Plans
- `GET /plans` - Generate 3 cleanup plans (Conservative/Balanced/Aggressive)
- `GET /plan/{plan_id}` - Get details for a specific plan

### Execution
- `POST /execute` - Execute a cleanup plan
- `WS /progress/{execution_id}` - Real-time progress updates (WebSocket)

### Settings
- `GET /settings` - Get user settings
- `POST /settings` - Update user settings

### Health
- `GET /` - Root endpoint
- `GET /health` - Health check

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── config.py            # Configuration & settings
│   ├── models.py            # Pydantic models
│   ├── dependencies.py      # Dependency injection
│   │
│   ├── api/                 # API routes
│   │   ├── analysis.py      # Drive analysis endpoint
│   │   ├── plans.py         # Plan generation endpoints
│   │   ├── execution.py     # Execution endpoint
│   │   ├── progress.py      # WebSocket progress
│   │   └── settings.py      # Settings endpoints
│   │
│   ├── services/            # Business logic
│   │   ├── analyzer.py      # Drive analysis engine
│   │   ├── planner.py       # Plan generation (AI + rules)
│   │   ├── executor.py      # Execution engine
│   │   ├── rollback.py      # Rollback manager
│   │   └── progress.py      # Progress tracking
│   │
│   ├── storage/             # Storage operations
│   │   └── scanner.py       # Drive scanning
│   │
│   ├── ai/                  # AI integration
│   │   ├── openai_client.py
│   │   ├── anthropic_client.py
│   │   └── prompts.py
│   │
│   └── utils/               # Utilities
│       ├── logger.py
│       ├── validators.py
│       └── helpers.py
│
├── data/                    # Data storage
│   ├── settings.json        # User settings
│   └── rollback/            # Rollback metadata
│
├── logs/                    # Application logs
├── requirements.txt
├── .env.example
└── README.md
```

## Usage Examples

### 1. Analyze Drives

```bash
curl http://127.0.0.1:8000/analyze
```

Response:
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
    }
  ],
  "top_consumers": [
    {
      "name": "Docker Desktop",
      "path": "C:\\Users\\winadmin\\AppData\\Local\\Docker Desktop",
      "size_bytes": 85200000000,
      "type": "docker"
    }
  ],
  "total_recoverable_bytes": 157200000000,
  "has_imbalance": true
}
```

### 2. Generate Plans

```bash
curl http://127.0.0.1:8000/plans?use_ai=true
```

### 3. Execute Plan

```bash
curl -X POST http://127.0.0.1:8000/execute \
  -H "Content-Type: application/json" \
  -d '{"plan_id": "balanced", "dry_run": false}'
```

Response:
```json
{
  "execution_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "started",
  "started_at": "2025-10-03T14:30:00"
}
```

### 4. Monitor Progress (WebSocket)

```javascript
const ws = new WebSocket('ws://127.0.0.1:8000/progress/550e8400-...')

ws.onmessage = (event) => {
  const progress = JSON.parse(event.data)
  console.log(`Progress: ${progress.overall_percent}%`)
}
```

## Configuration

### Environment Variables

All settings can be configured via `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `HOST` | 127.0.0.1 | Server host |
| `PORT` | 8000 | Server port |
| `RELOAD` | true | Auto-reload on code changes |
| `LOG_LEVEL` | INFO | Logging level |
| `ALLOWED_ORIGINS` | localhost:1420,tauri://localhost | CORS origins |
| `OPENAI_API_KEY` | - | OpenAI API key (optional) |
| `ANTHROPIC_API_KEY` | - | Anthropic API key (optional) |
| `BACKUP_LOCATION` | D:\Backups | Backup storage location |
| `DEFAULT_TARGET_DRIVE` | D: | Default target for moves |
| `DRY_RUN_DEFAULT` | false | Default dry-run mode |
| `USE_RECYCLE_BIN` | true | Use recycle bin for deletes |
| `CREATE_BACKUPS` | true | Create backups before operations |

## Development

### Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_analyzer.py -v
```

### Code Quality

```bash
# Format code
black app/

# Lint code
ruff check app/

# Type checking
mypy app/
```

## Safety Features

1. **Dry-Run Mode**: Preview changes without executing
2. **Recycle Bin**: Deleted files sent to recycle bin (recoverable)
3. **Symlinks**: Moved folders replaced with symlinks (maintains compatibility)
4. **Backups**: Automatic backups before major operations
5. **Rollback**: Reverse operations if needed
6. **Progress Tracking**: Real-time monitoring
7. **Error Handling**: Graceful failure with detailed logs

## AI Integration

### OpenAI (GPT-4)
- Set `OPENAI_API_KEY` in `.env`
- Uses GPT-4 Turbo for plan generation
- Fallback to rules if API fails

### Anthropic (Claude)
- Set `ANTHROPIC_API_KEY` in `.env`
- Uses Claude 3 Sonnet
- Fallback to rules if API fails

### Rule-Based Fallback
- Works without API keys
- Predefined cleanup strategies
- Based on common Windows patterns

## Troubleshooting

### Server won't start
- Check Python version: `python --version` (3.9+ required)
- Verify dependencies: `pip install -r requirements.txt`
- Check port availability: Port 8000 might be in use

### Analysis returns empty results
- Run as Administrator (required for some system folders)
- Check drive permissions
- Verify NTFS file system

### WebSocket connection fails
- Check CORS settings in `.env`
- Verify execution ID is valid
- Ensure backend is running

## Production Deployment

### Option 1: Windows Service (NSSM)
```bash
nssm install StorageManagerBackend "C:\path\to\venv\Scripts\python.exe" "-m uvicorn app.main:app --host 127.0.0.1 --port 8000"
nssm start StorageManagerBackend
```

### Option 2: Standalone Executable
```bash
pip install pyinstaller
pyinstaller --onefile --name storage-manager-backend app/main.py
```

## License

See main project LICENSE

## Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/yourusername/reclaim/issues)
- Documentation: [Full PRD](../BACKEND_PRD.md)

## Version

**1.0.0** - Initial release (2025-10-03)
