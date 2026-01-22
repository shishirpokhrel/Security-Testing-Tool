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

# OSV API
OSV_API_URL = "https://api.osv.dev/v1/query"

# Java/Android Scan Settings
JAVA_SCAN_CONFIG = {
    'maven_file': 'pom.xml',
    'gradle_file': 'build.gradle',
    'extensions': ['.jar', '.war', '.ear']
}

# Angular Scan Settings
ANGULAR_SCAN_CONFIG = {
    'package_file': 'package.json',
    'extensions': ['.js', '.ts']
}

# Java Static Analysis Rules (SAST)
JAVA_SAST_RULES = {
    'Hardcoded Password': {
        'pattern': r'(?i)(password|passwd|pwd|secret|token|api_key|apikey)\s*=\s*["\'][^"\']+["\']',
        'severity': 'HIGH',
        'description': 'Potential hardcoded secret found.'
    },
    'SQL Injection': {
        'pattern': r'(?i)("select\s+.*"\s*\+\s*[a-zA-Z0-9_]+|Statement\.execute)',
        'severity': 'HIGH',
        'description': 'Potential SQL Injection due to string concatenation in query.'
    },
    'Command Injection': {
        'pattern': r'(Runtime\.getRuntime\(\)\.exec|ProcessBuilder)',
        'severity': 'CRITICAL',
        'description': 'Execution of external system commands found.'
    },
    'Insecure Cryptography': {
        'pattern': r'(?i)(MD5|SHA-1|DES)',
        'severity': 'MEDIUM',
        'description': 'Weak cryptographic algorithm usage.'
    },
    'System Print Usage': {
        'pattern': r'System\.out\.print',
        'severity': 'LOW',
        'description': 'Use a logger instead of System.out.print.'
    },
    'Stack Trace Exposure': {
        'pattern': r'\.printStackTrace\(',
        'severity': 'LOW',
        'description': 'Stack trace exposure can leak sensitive information.'
    }
}

# Android Scan Settings
ANDROID_SCAN_CONFIG = {
    'manifest_file': 'AndroidManifest.xml',
    'gradle_file': 'build.gradle',
    'extensions': ['.java', '.kt', '.xml']
}

ANDROID_SAST_RULES = {
    'Insecure WebView': {
        'pattern': r'setJavaScriptEnabled\(true\)',
        'severity': 'HIGH',
        'description': 'WebView with JavaScript enabled can be vulnerable to XSS.'
    },
    'External Storage': {
        'pattern': r'(getExternalStorageDirectory|getExternalFilesDir)',
        'severity': 'MEDIUM',
        'description': 'Insecure usage of external storage.'
    },
    'Hardcoded API Key': {
        'pattern': r'(?i)(api_key|apikey|secret)\s*=\s*["\'][^"\']+["\']',
        'severity': 'HIGH',
        'description': 'Potential hardcoded API key.'
    },
    'Broadcast Receiver': {
        'pattern': r'registerReceiver',
        'severity': 'LOW',
        'description': 'Dynamic BroadcastReceiver registration should be protected.'
    }
}

ANDROID_MANIFEST_CHECKS = {
    'Debuggable': {
        'pattern': r'android:debuggable=["\']true["\']',
        'severity': 'CRITICAL',
        'description': 'Application is debuggable. Attackers can hook into the process.'
    },
    'Allow Backup': {
        'pattern': r'android:allowBackup=["\']true["\']',
        'severity': 'MEDIUM',
        'description': 'Application data can be backed up and potentially accessed.'
    },
    'Exported Activity': {
        'pattern': r'android:exported=["\']true["\']',
        'severity': 'HIGH',
        'description': 'Activity is exported and accessible to other apps.'
    }
}

# iOS Scan Settings
IOS_SCAN_CONFIG = {
    'plist_file': 'Info.plist',
    'podfile_lock': 'Podfile.lock',
    'extensions': ['.swift', '.m', '.h', '.plist']
}

IOS_SAST_RULES = {
    'Insecure HTTP': {
        'pattern': r'http://',
        'severity': 'MEDIUM',
        'description': 'Usage of insecure HTTP protocol.'
    },
    'Weak Randomness': {
        'pattern': r'(arc4random|rand\(\))',
        'severity': 'MEDIUM',
        'description': 'Weak random number generator usage.'
    },
    'Hardcoded Credential': {
        'pattern': r'(?i)(password|secret|token)\s*=\s*@?["\'][^"\']+["\']',
        'severity': 'HIGH',
        'description': 'Potential hardcoded credential.'
    },
    'MD5 Usage': {
        'pattern': r'CC_MD5',
        'severity': 'MEDIUM',
        'description': 'Weak hashing algorithm (MD5).'
    }
}

IOS_PLIST_CHECKS = {
    'App Transport Security': {
        'key': 'NSAppTransportSecurity',
        'sub_key': 'NSAllowsArbitraryLoads',
        'value': True,
        'severity': 'HIGH',
        'description': 'App allows arbitrary loads (insecure HTTP).'
    }
}
