# Quick Start Guide

## For WSL/Linux Users (Recommended)

Since you're using WSL, follow these steps:

### 1. Run the automated installer

```bash
cd /mnt/c/Users/eSewa/secTest

# Make scripts executable
chmod +x install.sh

# Run installer
./install.sh
```

This will:
- Install all Python dependencies
- Check for Nmap and Subfinder
- Test all imports

### 2. Install Nmap (if not installed)

```bash
sudo apt update
sudo apt install nmap
```

### 3. (Optional) Install Subfinder

```bash
# If you have Go installed:
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest

# Or download binary from:
# https://github.com/projectdiscovery/subfinder/releases
```

### 4. Run the scanner

```bash
# Interactive mode
python3 securityscanner.py

# Command-line mode examples
python3 securityscanner.py nmap -u 127.0.0.1 -p common
python3 securityscanner.py xss -u "http://testphp.vulnweb.com/search.php?test=query"
python3 securityscanner.py --help
```

---

## For Windows PowerShell Users

### 1. Run the automated installer

```powershell
cd C:\Users\eSewa\secTest

# Just double-click install.bat or run:
.\install.bat
```

### 2. Install Nmap

Download from: https://nmap.org/download.html

### 3. Run the scanner

```powershell
python securityscanner.py
```

---

## Troubleshooting the Import Error

The error you saw:
```
ModuleNotFoundError: No module named 'nmap'
```

Means the dependencies aren't installed yet. Fix it with:

### In WSL/Linux:
```bash
pip3 install -r requirements.txt
# or
python3 -m pip install -r requirements.txt
```

### In Windows:
```powershell
pip install -r requirements.txt
# or
python -m pip install -r requirements.txt
```

---

## Testing Your Installation

After installation, run the test script:

```bash
# WSL/Linux
python3 test_imports.py

# Windows
python test_imports.py
```

This will check all modules and tell you exactly what's missing.

---

## Safe Testing Commands

Once installed, test with these safe commands:

```bash
# 1. Test help system
python3 securityscanner.py --help

# 2. Test Nmap on localhost (safe)
python3 securityscanner.py nmap -u 127.0.0.1 -p 80,443

# 3. Test XSS scanner on a vulnerable test site
python3 securityscanner.py xss -u "http://testphp.vulnweb.com/search.php?test=query"

# 4. Interactive mode
python3 securityscanner.py
```

---

## Common Issues

**"python3 not recognized"**
- In Windows PowerShell: Use `python` instead of `python3`
- In WSL: Python3 should be installed by default

**"Permission denied" on install.sh**
- Run: `chmod +x install.sh`

**Nmap scans fail**
- Install Nmap: `sudo apt install nmap` (WSL) or download for Windows
- Some scans need admin/root privileges

**No module named 'paramiko'**
- Dependencies not fully installed
- Run: `pip3 install -r requirements.txt` again

---

For detailed instructions, see [INSTALL.md](INSTALL.md)
