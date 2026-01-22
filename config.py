"""
Configuration settings for the security scanner
"""
import os

# Base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORDLISTS_DIR = os.path.join(BASE_DIR, 'wordlists')
PAYLOADS_DIR = os.path.join(BASE_DIR, 'payloads')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output')

# Default wordlists
DEFAULT_USERNAMES = os.path.join(WORDLISTS_DIR, 'usernames.txt')
DEFAULT_PASSWORDS = os.path.join(WORDLISTS_DIR, 'passwords.txt')
XSS_PAYLOADS_FILE = os.path.join(PAYLOADS_DIR, 'xss_payloads.txt')

# Nmap settings
NMAP_TIMEOUT = 300  # 5 minutes
NMAP_COMMON_PORTS = '21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080'
NMAP_ARGS = '-sV -sC -O'  # Service version, default scripts, OS detection

# Subfinder settings
SUBFINDER_TIMEOUT = 120  # 2 minutes
SUBFINDER_PATH = 'subfinder'  # Assumes subfinder is in PATH

# Brute force settings
BRUTEFORCE_DELAY = 0.5  # Delay between attempts in seconds
BRUTEFORCE_TIMEOUT = 10  # Timeout for each request
MAX_THREADS = 5  # Maximum concurrent threads for brute force

# XSS Scanner settings
XSS_TIMEOUT = 10  # Timeout for each request
XSS_MAX_PAYLOADS = 50  # Maximum number of payloads to test per parameter
XSS_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

# User agents for requests
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
]

# Logging settings
LOG_LEVEL = 'INFO'
LOG_FILE = os.path.join(OUTPUT_DIR, 'scanner.log')

# Create necessary directories
os.makedirs(WORDLISTS_DIR, exist_ok=True)
os.makedirs(PAYLOADS_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)
