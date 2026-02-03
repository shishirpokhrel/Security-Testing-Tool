# ⚡ Quick Start Guide

We have created helper scripts to make running the tool incredibly easy. No need to memorize complex commands!

---

## 🚀 For Windows Users (Recommended)

### Option 1: Run the Web UI (Easier)
1. **Double-click** `start_ui.bat`
2. This will:
   - Setup the environment
   - Start the Backend (API)
   - Start the Frontend (Web Dashboard) and open it in your browser

### Option 2: Run the CLI (Advanced)
1. **Double-click** `run.bat` OR open CMD/PowerShell and type:
   ```powershell
   .\run.bat
   ```
2. You can pass arguments directly:
   ```powershell
   .\run.bat scan -d C:\path\to\project    # Auto-scan a project
   .\run.bat nmap -u 127.0.0.1 -p common   # Nmap scan
   ```

---

## 🐧 For Linux / macOS / WSL Users

First, make the scripts executable (one-time setup):
```bash
chmod +x run.sh start_ui.sh install.sh
```

### Option 1: Run the Web UI
```bash
./start_ui.sh
```

### Option 2: Run the CLI
```bash
./run.sh help
./run.sh scan -d /path/to/project
```

---

## 📦 Zero-Setup Installation

The `run` and `start_ui` scripts will **automatically create a virtual environment and install dependencies** if they are missing.

However, if you want to install everything manually first:

**Windows:**
```powershell
.\install.bat
```

**Linux/macOS:**
```bash
./install.sh
```

---

## 🛠️ Prerequisites

You still need these installed on your system:
1. **Python 3.7+**
2. **Node.js** (Only for Web UI)
3. **Nmap** (Required for network scanning)

For detailed manual installation, see [INSTALL.md](INSTALL.md).

