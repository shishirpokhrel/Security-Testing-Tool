#!/bin/bash
# Installation script for Linux/WSL

echo "=========================================="
echo "Security Scanner - Installation Script"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
    echo "✓ Python3 found: $(python3 --version)"
elif command -v python &> /dev/null; then
    PYTHON_CMD="python"
    PIP_CMD="pip"
    echo "✓ Python found: $(python --version)"
else
    echo "✗ Python not found!"
    echo "Please install Python 3.7+ first:"
    echo "  sudo apt update"
    echo "  sudo apt install python3 python3-pip"
    exit 1
fi

echo ""
echo "=========================================="
echo "Installing Python dependencies..."
echo "=========================================="
echo ""

# Upgrade pip
echo "Upgrading pip..."
$PYTHON_CMD -m pip install --upgrade pip

# Install requirements
echo ""
echo "Installing packages from requirements.txt..."
$PYTHON_CMD -m pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Python dependencies installed successfully!"
else
    echo ""
    echo "✗ Failed to install dependencies"
    echo "Try running manually:"
    echo "  $PYTHON_CMD -m pip install -r requirements.txt"
    exit 1
fi

echo ""
echo "=========================================="
echo "Checking external dependencies..."
echo "=========================================="
echo ""

# Check for Nmap
if command -v nmap &> /dev/null; then
    echo "✓ Nmap found: $(nmap --version | head -n1)"
else
    echo "✗ Nmap not found"
    echo "Install with:"
    echo "  sudo apt install nmap"
fi

# Check for Subfinder
if command -v subfinder &> /dev/null; then
    echo "✓ Subfinder found: $(subfinder -version 2>&1 | head -n1)"
else
    echo "⚠ Subfinder not found (optional)"
    echo "Install with Go:"
    echo "  go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest"
fi

echo ""
echo "=========================================="
echo "Running import test..."
echo "=========================================="
echo ""

$PYTHON_CMD test_imports.py

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ Installation successful!"
    echo "=========================================="
    echo ""
    echo "To run the scanner:"
    echo "  $PYTHON_CMD securityscanner.py"
    echo ""
    echo "For help:"
    echo "  $PYTHON_CMD securityscanner.py --help"
    echo ""
else
    echo ""
    echo "=========================================="
    echo "✗ Installation incomplete"
    echo "=========================================="
    echo ""
    echo "Please check the errors above and fix them."
    exit 1
fi
