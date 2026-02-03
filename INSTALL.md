# Security Scanner Installation Guide

## ⚡ Quick Install (Recommended)

I've created automated installation scripts for you!

### For WSL/Linux:
```bash
# Make the script executable
chmod +x install.sh

# Run the installer
./install.sh
```

### For Windows:
```powershell
# Just double-click install.bat
# Or run from PowerShell:
.\install.bat
```

These scripts will:
1. ✅ Check Python installation
2. ✅ Upgrade pip
3. ✅ Install all dependencies from requirements.txt
4. ✅ Check for Nmap and Subfinder
5. ✅ Run import tests to verify everything works

---

## 🔧 Manual Installation

If you want to set up the tool manually or want to run the **Web UI**, follow these steps:

### Prerequisites

1. **Python 3.7+** (Required for all modes)
2. **Node.js & npm** (Required for Web UI only)
   - Download: [nodejs.org](https://nodejs.org/)
   - Verify: `node -v` and `npm -v`
3. **Nmap** (Required for scanning)
   - Download: [nmap.org](https://nmap.org/download.html)

### 1. Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies (Web UI)

```bash
cd frontend
npm install
cd ..
```

---

## Running the Application

### 🌐 Web UI Mode (Recommended)

You need to run the Backend and Frontend in separate terminals.

**Terminal 1 (Backend):**
```bash
python api.py
# Server runs on http://localhost:8000
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
# Interface runs on http://localhost:5173 (check console for exact URL)
```

### 💻 CLI Mode (Legacy)

Run the classic command-line interface:

```bash
python securityscanner.py
```

---

## 🔧 Detailed Manual Installation (Windows)

If the automated scripts don't work for you, follow these steps:

## Quick Start for Windows

Since Python may not be in your PATH, here's how to get started:

### Option 1: Using Windows Store Python

If you don't have Python installed:
1. Open Microsoft Store
2. Search for "Python 3.11" or "Python 3.12"
3. Install Python
4. It will automatically be added to PATH as `python`

### Option 2: Finding Your Python Installation

If Python is installed but not in PATH, try:

```powershell
# Find Python installations
where.exe python*
# or
Get-Command python* -ErrorAction SilentlyContinue
```

### Option 3: Using Full Path

If you know where Python is installed (e.g., `C:\Python311\python.exe`), use full path:

```powershell
# Install dependencies with full path
C:\Python311\python.exe -m pip install -r requirements.txt

# Run the tool with full path
C:\Python311\python.exe securityscanner.py
```

### Option 4: Add Python to PATH

1. Find Python installation directory
2. Open System Properties → Environment Variables
3. Add Python directory to PATH
4. Restart PowerShell

## Installation Steps

### 1. Install Dependencies

Try these commands in order until one works:

```powershell
# Try 1: Direct pip
pip install -r requirements.txt

# Try 2: Python module
python -m pip install -r requirements.txt

# Try 3: Python3
python3 -m pip install -r requirements.txt

# Try 4: Windows Python launcher
py -m pip install -r requirements.txt

# Try 5: Full path (replace with your Python path)
C:\Python311\python.exe -m pip install -r requirements.txt
```

### 2. Install Nmap

Download and install from: https://nmap.org/download.html

**Important**: During installation, make sure to check "Add Nmap to system PATH"

Verify installation:
```powershell
nmap --version
```

### 3. (Optional) Install Subfinder

**Using Go**:
```powershell
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
```

**Or download binary**: https://github.com/projectdiscovery/subfinder/releases

Verify installation:
```powershell
subfinder -version
```

## Running the Tool

### Interactive Mode (Recommended for First Run)

```powershell
# Try these in order:
python securityscanner.py
# or
python3 securityscanner.py
# or
py securityscanner.py
# or (with full path)
C:\Python311\python.exe securityscanner.py
```

### Command-Line Mode Examples

```powershell
# Nmap scan (localhost is safe to test)
python securityscanner.py nmap -t 127.0.0.1 -p common

# Subfinder (use a domain you own)
python securityscanner.py subfinder -d example.com

# XSS scan (test your own site)
python securityscanner.py xss -u "http://localhost/search?q=test"
```

## Troubleshooting

### "Python not recognized"
- Python not installed or not in PATH
- Install from Microsoft Store or python.org
- Or use full path to python.exe

### "pip not recognized"
- Use `python -m pip` instead of just `pip`
- Or install pip: `python -m ensurepip --upgrade`

### "Nmap not found"
- Install Nmap from nmap.org
- Make sure it's added to PATH during installation
- Or specify full path in config.py

### "Permission denied" during Nmap scan
- Some Nmap scans require administrator privileges
- Run PowerShell as Administrator
- Or use non-privileged scan options

### ImportError for modules
- Dependencies not installed
- Run: `python -m pip install -r requirements.txt`
- Check for error messages during installation

## Testing Installation

Run these safe tests to verify everything works:

```powershell
# Test 1: Check tool starts
python securityscanner.py

# Test 2: Scan localhost (safe)
python securityscanner.py nmap -t 127.0.0.1 -p 80

# Test 3: Check help
python securityscanner.py --help
python securityscanner.py nmap --help
```

## Next Steps

1. ✅ Verify Python is working
2. ✅ Install all dependencies from requirements.txt
3. ✅ Install and verify Nmap
4. ✅ Run a safe test scan on localhost
5. ✅ Review README.md for full documentation
6. ✅ Only scan systems you have permission to test!

---

**Remember**: Always obtain proper authorization before scanning any systems!
