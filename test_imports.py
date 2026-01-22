#!/usr/bin/env python3
"""
Test script to verify all modules can be imported
"""
import sys
import os

print("=" * 60)
print("Security Scanner - Module Import Test")
print("=" * 60)
print(f"\nPython Version: {sys.version}")
print(f"Python Path: {sys.executable}")
print(f"Current Directory: {os.getcwd()}")
print("\n" + "=" * 60)
print("Testing Module Imports...")
print("=" * 60)

# Test standard library imports
modules_to_test = [
    ("json", "standard library"),
    ("datetime", "standard library"),
    ("argparse", "standard library"),
    ("subprocess", "standard library"),
    ("colorama", "pip package"),
    ("requests", "pip package"),
    ("tqdm", "pip package"),
    ("bs4", "pip package (beautifulsoup4)"),
    ("nmap", "pip package (python-nmap)"),
    ("urllib3", "pip package"),
    ("lxml", "pip package"),
]

failed_imports = []
successful_imports = []

for module_name, source in modules_to_test:
    try:
        if module_name == "bs4":
            from bs4 import BeautifulSoup
        elif module_name == "nmap":
            import nmap
        else:
            __import__(module_name)
        print(f"✓ {module_name:20s} - OK ({source})")
        successful_imports.append(module_name)
    except ImportError as e:
        print(f"✗ {module_name:20s} - FAILED ({source})")
        print(f"  Error: {str(e)}")
        failed_imports.append((module_name, source, str(e)))

print("\n" + "=" * 60)
print("Testing Project Modules...")
print("=" * 60)

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

project_modules = [
    "config",
    "utils.logger",
    "modules.nmap_scanner",
    "modules.subfinder_module",
    "modules.bruteforce",
    "modules.xss_scanner",
]

for module_name in project_modules:
    try:
        __import__(module_name)
        print(f"✓ {module_name:30s} - OK")
        successful_imports.append(module_name)
    except ImportError as e:
        print(f"✗ {module_name:30s} - FAILED")
        print(f"  Error: {str(e)}")
        failed_imports.append((module_name, "project", str(e)))

print("\n" + "=" * 60)
print("Summary")
print("=" * 60)
print(f"Successful: {len(successful_imports)}")
print(f"Failed: {len(failed_imports)}")

if failed_imports:
    print("\n" + "=" * 60)
    print("FAILED IMPORTS - Action Required:")
    print("=" * 60)
    
    pip_packages = []
    for module_name, source, error in failed_imports:
        if source.startswith("pip"):
            pip_packages.append(module_name)
            print(f"\n✗ {module_name}")
            print(f"  Source: {source}")
            print(f"  Error: {error}")
    
    if pip_packages:
        print("\n" + "=" * 60)
        print("TO FIX: Install missing packages with:")
        print("=" * 60)
        print("\nIf using WSL/Linux:")
        print("  pip3 install -r requirements.txt")
        print("  # or")
        print("  python3 -m pip install -r requirements.txt")
        print("\nIf using Windows PowerShell:")
        print("  pip install -r requirements.txt")
        print("  # or")
        print("  python -m pip install -r requirements.txt")
        print("\nOr install individually:")
        for pkg in pip_packages:
            pkg_name = pkg
            if pkg == "nmap":
                pkg_name = "python-nmap"
            elif pkg == "bs4":
                pkg_name = "beautifulsoup4"
            print(f"  pip install {pkg_name}")
    
    print("\n" + "=" * 60)
    sys.exit(1)
else:
    print("\n✓ All modules imported successfully!")
    print("\nYou can now run the security scanner:")
    print("  python securityscanner.py")
    print("  # or")
    print("  python3 securityscanner.py")
    print("\n" + "=" * 60)
    sys.exit(0)
