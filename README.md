# Storage Manager - Windows Desktop App

AI-powered Windows storage management and cleanup tool built with Tauri + React + Python backend.

![Storage Manager](https://via.placeholder.com/800x450/6366f1/ffffff?text=Storage+Manager)

## Features

- 📊 **Real-time Storage Analysis** - Visualize disk usage across all drives (C:, D:, F:)
- 🤖 **AI-Powered Recommendations** - Get 3 cleanup strategies: Conservative, Balanced, Aggressive
- 🔄 **Safe Execution** - Step-by-step execution with rollback capabilities
- 📝 **Live Progress Logs** - Real-time WebSocket updates during cleanup
- 🎨 **Modern UI** - Built with React, TailwindCSS, and Framer Motion
- 🔒 **Safety First** - Dry-run mode, recycle bin support, automatic backups

## Tech Stack

### Frontend
- **Tauri** - Rust-based desktop framework
- **React 18** + **TypeScript** - UI framework
- **TailwindCSS** - Styling
- **Framer Motion** - Animations
- **React Query** - API state management
- **Recharts** - Data visualization
- **Lucide React** - Icons

### Backend (Separate Repository)
- **FastAPI** - Python REST API
- **WebSockets** - Real-time progress updates
- **AI Integration** - OpenAI/Anthropic for plan generation

## Prerequisites

### Required Software

1. **Node.js** (v18 or later)
   ```bash
   # Download from https://nodejs.org/
   # Or use a version manager
   ```

2. **Rust** (latest stable)
   ```bash
   # Windows: Download from https://rustup.rs/
   # Or use winget
   winget install Rustlang.Rustup
   ```

3. **Tauri CLI**
   ```bash
   npm install -g @tauri-apps/cli
   ```

4. **Python Backend** (separate setup)
   - See backend repository for installation instructions
   - Backend should run on `http://127.0.0.1:8000`

## Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd storage-manager
```

### 2. Install Dependencies

```bash
npm install
# or
yarn install
```

### 3. Configure Environment

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and configure:
VITE_API_URL=http://127.0.0.1:8000
```

### 4. Start Backend Server

Make sure your Python FastAPI backend is running:

```bash
# In your backend directory
uvicorn main:app --reload --port 8000
```

## Development

### Run in Development Mode

```bash
npm run tauri:dev
# or
yarn tauri dev
```

This will:
- Start the Vite dev server on `http://localhost:1420`
- Launch the Tauri development window
- Enable hot-reload for React components

### Build for Production

```bash
npm run tauri:build
# or
yarn tauri build
```

The built executable will be in `src-tauri/target/release/`.

## Project Structure

```
storage-manager/
├── src/                          # React frontend source
│   ├── components/               # Reusable UI components
│   │   ├── ui/                   # Base UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Progress.tsx
│   │   │   └── Toggle.tsx
│   │   ├── DriveCard.tsx         # Drive usage card
│   │   ├── PlanCard.tsx          # Cleanup plan card
│   │   ├── ActionCard.tsx        # Action detail card
│   │   └── ProgressLog.tsx       # Execution progress
│   ├── pages/                    # Main application pages
│   │   ├── Dashboard.tsx         # Drive overview & top consumers
│   │   ├── Plans.tsx             # AI plan selection
│   │   ├── PlanDetails.tsx       # Detailed action list
│   │   ├── Execution.tsx         # Live execution progress
│   │   └── Settings.tsx          # App configuration
│   ├── hooks/                    # React Query hooks
│   │   ├── useAnalysis.ts        # Drive analysis
│   │   ├── usePlans.ts           # Plan fetching
│   │   ├── useExecutePlan.ts     # Execution
│   │   ├── useProgress.ts        # WebSocket progress
│   │   └── useSettings.ts        # Settings CRUD
│   ├── lib/                      # Utilities
│   │   ├── api.ts                # API client
│   │   └── utils.ts              # Helper functions
│   ├── types/                    # TypeScript types
│   │   └── api.ts                # API interfaces
│   ├── App.tsx                   # Main app component
│   ├── main.tsx                  # Entry point
│   └── index.css                 # Global styles
├── src-tauri/                    # Tauri Rust backend
│   ├── src/
│   │   └── main.rs               # Tauri main process
│   ├── Cargo.toml                # Rust dependencies
│   └── tauri.conf.json           # Tauri configuration
├── package.json                  # Node dependencies
├── tsconfig.json                 # TypeScript config
├── tailwind.config.js            # TailwindCSS config
├── vite.config.ts                # Vite bundler config
└── README.md                     # This file
```

## API Integration

### Backend Endpoints

The frontend expects these endpoints from the Python backend:

#### Analysis
- `GET /analyze` → Returns drive info + top consumers
  ```json
  {
    "drives": [...],
    "top_consumers": [...],
    "has_imbalance": true,
    "imbalance_message": "..."
  }
  ```

#### Plans
- `GET /plans` → Returns 3 AI-generated plans
- `GET /plan/{id}` → Returns detailed plan with actions

#### Execution
- `POST /execute` → Starts plan execution
  ```json
  {
    "plan_id": "balanced",
    "dry_run": false
  }
  ```
  Returns: `{ "execution_id": "uuid" }`

- `WS /progress/{execution_id}` → WebSocket for live updates
  ```json
  {
    "overall_percent": 65,
    "current_step": 3,
    "steps": [...],
    "logs": [...],
    "status": "running"
  }
  ```

#### Settings
- `GET /settings` → Returns user settings
- `POST /settings` → Updates settings

### Environment Variables

```bash
# Required
VITE_API_URL=http://127.0.0.1:8000

# Optional (can be set in UI)
VITE_OPENAI_API_KEY=sk-...
VITE_ANTHROPIC_API_KEY=sk-ant-...
```

## Configuration

### Tauri Configuration (`src-tauri/tauri.conf.json`)

- **Window Size**: 1200x800 (min: 800x600)
- **HTTP Allowlist**: `http://localhost:8000/*`, `http://127.0.0.1:8000/*`
- **Permissions**: HTTP requests, file dialogs, limited filesystem access

### Backend URL

Change backend URL in Settings page or via `.env`:
```
VITE_API_URL=http://your-backend:8000
```

## Features & Usage

### 1. Dashboard
- View all detected drives with usage bars
- See imbalance warnings (e.g., C: full, D: empty)
- Browse top space consumers (Docker, WSL, Downloads, etc.)
- Click "GET AI RECOMMENDATIONS" to proceed

### 2. Plan Selection
- AI generates 3 strategies:
  - **Conservative** (Low risk, basic cleanup)
  - **Balanced** (Recommended, medium risk)
  - **Aggressive** (High risk, max space savings)
- Each shows: space saved, risk level, ETA, rationale
- Click "View Plan" for details

### 3. Plan Details
- Expandable action cards grouped by type:
  - MOVE operations (e.g., Docker → D:)
  - CLEANUP operations (caches, temp files)
  - WSL export/import
- Each action shows:
  - Source/target paths
  - Safety explanation
  - Rollback options
- Click "Execute Plan" to start

### 4. Execution
- Real-time progress bar
- Step-by-step status (✓ completed, 🔄 active, ⏳ pending)
- Live log stream (green terminal output)
- Cancel or rollback options
- Success/failure notifications

### 5. Settings
- **AI Configuration**: Enable/disable AI, choose provider (OpenAI/Anthropic), API key
- **Safety**: Dry-run mode, recycle bin vs delete, auto-backups
- **Targets**: Default drives for relocation (D:, F:)
- **Backend URL**: Change API endpoint

## Building for Release

### Windows .exe

```bash
npm run tauri:build
```

Output: `src-tauri/target/release/storage-manager.exe` (~10-20MB)

### Build Optimizations

The app is configured for minimal size:
- Tauri uses system WebView (no Chromium bundled)
- Tree-shaking enabled in Vite
- Rust optimized for release builds

### Troubleshooting Build Issues

**Error: "Rust not found"**
```bash
# Install Rust
winget install Rustlang.Rustup
# Restart terminal
```

**Error: "tauri.conf.json invalid"**
- Check JSON syntax
- Ensure all paths exist

**Error: "Failed to bundle"**
- Run `cargo clean` in `src-tauri/`
- Delete `node_modules` and reinstall

## Development Tips

### Hot Reload
- React components hot-reload automatically
- Rust changes require restart (`Ctrl+C` → rerun `tauri dev`)

### Debugging
- React DevTools: Works in development
- Rust logs: Check terminal output
- Network: Open DevTools (`Ctrl+Shift+I` in dev mode)

### Linting & Formatting
```bash
# TypeScript/React linting
npm run lint

# Code formatting
npm run format

# Rust formatting
cd src-tauri && cargo fmt
```

## Performance

- **Bundle Size**: ~10-20MB (Tauri uses OS WebView)
- **Memory Usage**: ~50-100MB idle
- **Startup Time**: <1 second
- **API Latency**: <100ms (local backend)

## Security

- **Sandboxed**: Tauri restricts filesystem/network access
- **HTTPS Only**: Production should use HTTPS backend
- **API Keys**: Stored locally, never sent to our servers
- **No Telemetry**: Zero analytics or tracking

## Roadmap

- [ ] Multi-language support (i18n)
- [ ] Dark mode toggle
- [ ] Scheduled cleanups (cron-like)
- [ ] Cloud backup integration
- [ ] Linux/macOS support
- [ ] Portable mode (no installation)

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## License

MIT License - see [LICENSE](LICENSE) file

## Acknowledgments

- [Tauri](https://tauri.app/) - Desktop framework
- [shadcn/ui](https://ui.shadcn.com/) - UI component inspiration
- [Tailwind CSS](https://tailwindcss.com/) - Styling
- [Lucide](https://lucide.dev/) - Icons

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/storage-manager/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/storage-manager/discussions)
- **Email**: support@example.com

---

**Built with ❤️ for Windows users**