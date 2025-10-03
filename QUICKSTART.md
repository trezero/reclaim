# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Prerequisites

**Windows 11 Users:**

```powershell
# Install Node.js
winget install OpenJS.NodeJS.LTS

# Install Rust
winget install Rustlang.Rustup

# Restart your terminal after installation
```

### Step 2: Install Dependencies

```bash
# Clone the repo (or extract the zip)
cd storage-manager

# Install Node packages
npm install

# Install Tauri CLI globally (optional but recommended)
npm install -g @tauri-apps/cli
```

### Step 3: Configure Environment

```bash
# Copy environment file
cp .env.example .env

# The default values should work if your Python backend is on port 8000
# VITE_API_URL=http://127.0.0.1:8000
```

### Step 4: Start the Python Backend

**In a separate terminal:**

```bash
# Navigate to your Python backend directory
cd ../backend  # or wherever your Python backend is

# Start FastAPI server
uvicorn main:app --reload --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 5: Run the Frontend

**Back in the storage-manager directory:**

```bash
npm run tauri:dev
```

This will:
1. Start Vite dev server (http://localhost:1420)
2. Open the Tauri desktop window
3. Enable hot-reload

### Step 6: Build for Production (Optional)

```bash
npm run tauri:build
```

Your executable will be at:
```
src-tauri/target/release/storage-manager.exe
```

---

## 🐛 Common Issues

### "Rust not found"
```bash
# Install Rust
winget install Rustlang.Rustup

# Restart terminal and verify
rustc --version
```

### "Cannot connect to backend"
- Ensure Python backend is running on port 8000
- Check `.env` has correct `VITE_API_URL`
- Try: `curl http://127.0.0.1:8000/analyze`

### "npm install fails"
```bash
# Clear cache and retry
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

### "Tauri build fails"
```bash
# Clean and rebuild
cd src-tauri
cargo clean
cd ..
npm run tauri:build
```

---

## 📁 Project Structure at a Glance

```
storage-manager/
├── src/
│   ├── pages/          # Dashboard, Plans, PlanDetails, Execution, Settings
│   ├── components/     # DriveCard, PlanCard, ActionCard, ProgressLog
│   ├── hooks/          # API integration hooks
│   └── lib/            # API client & utilities
├── src-tauri/          # Rust backend (Tauri)
└── package.json        # Dependencies
```

---

## 🎯 Next Steps

1. **Customize Styling**: Edit `tailwind.config.js` and `src/index.css`
2. **Add Features**: Extend API hooks in `src/hooks/`
3. **Backend Integration**: Ensure Python endpoints match the API contract
4. **Build & Ship**: Run `npm run tauri:build` for production

---

## 📚 Full Documentation

See [README.md](README.md) for complete documentation.

---

**Need Help?** Open an issue on GitHub or check the troubleshooting section in the README.
