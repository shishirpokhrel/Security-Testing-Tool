# Security Scanner Tool

A comprehensive Python-based security scanning tool that combines network scanning, subdomain enumeration, credential brute forcing, and XSS vulnerability detection.

## Features

- **🔍 Nmap Port Scanner**: Network reconnaissance with port scanning, service detection, OS detection, and vulnerability scanning
- **🌐 Subfinder Integration**: Passive subdomain enumeration for target domains
- **🔐 Brute Force Module**: Credential testing for HTTP (Basic/Form), SSH, and FTP
- ⚠️ **XSS Scanner**: Cross-site scripting vulnerability detection with multiple payload injection vectors
- ☕ **Java Scanner**: Vulnerability scanning for Maven (pom.xml) and Gradle (build.gradle) dependencies
- 🅰️ **Angular/Node Scanner**: Vulnerability scanning for npm (package.json) dependencies

## Prerequisites

### Required Software

1. **Python 3.7+**
   ```bash
   python --version
   ```

2. **Nmap** - Network scanning tool
   - Windows: Download from [nmap.org](https://nmap.org/download.html)
   - Linux: `sudo apt-get install nmap` or `sudo yum install nmap`
   - macOS: `brew install nmap`

3. **Subfinder** (Optional but recommended)
   ```bash
   go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
   ```
   
   Or download binary from: https://github.com/projectdiscovery/subfinder/releases

### Python Dependencies

Install required Python packages:

```bash
pip install -r requirements.txt
```

## Installation

1. Clone or download this repository

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Ensure Nmap is installed and accessible from command line:
   ```bash
   nmap --version
   ```

4. (Optional) Install Subfinder for subdomain enumeration

## Usage

## 🚀 How to Run

I've included helper scripts that automatically handle the virtual environment for you. You don't need to manually install dependencies or activate the venv!

### 🍎 macOS & 🐧 Linux
1.  Open your terminal.
2.  Make the script executable (run this once):
    ```bash
    chmod +x run.sh
    ```
3.  Run the tool:
    ```bash
    # Auto-scan a project
    ./run.sh scan -d /path/to/your/project

    # Interactive mode
    ./run.sh
    ```

### 🪟 Windows
1.  Open Command Prompt (cmd) or PowerShell.
2.  Run the batch file directly:
    ```cmd
    :: Auto-scan a project
    run.bat scan -d C:\path\to\your\project

    :: Interactive mode
    run.bat
    ```

### ⚡ Available Commands
Once you have the helper script (`./run.sh` or `run.bat`), you can use any of these commands:

| Feature | Command |
| :--- | :--- |
| **Auto-Discover** | `scan -d <dir>` |
| **Java/Spring** | `java-scan -d <dir>` |
| **Angular/Node** | `angular-scan -d <dir>` |
| **Android** | `android-scan -d <dir>` |
| **iOS** | `ios-scan -d <dir>` |
| **Nmap** | `nmap -u <ip> -p common` |
| **Subfinder** | `subfinder -u <domain>` |
| **Help** | `--help` |

### 🛠️ Manual Run (Advanced)
If you prefer not to use the helper scripts:

1.  **Install/Active venv**:
    ```bash
    # macOS/Linux
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    # Windows
    python -m venv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```
2.  **Run Tool**:
    ```bash
    python securityscanner.py scan -d ...
    ```

#### Nmap Port Scanning

Scan common ports:
```bash
python securityscanner.py nmap -u 192.168.1.1 -p common
```

Scan all ports:
```bash
python securityscanner.py nmap -u example.com -p all
```

Scan specific ports:
```bash
python securityscanner.py nmap -u 192.168.1.1 -p 80,443,8080
```

Vulnerability scan:
```bash
python securityscanner.py nmap -u 192.168.1.1 -v
```

Save results to file:
```bash
python securityscanner.py nmap -u 192.168.1.1 -p common -o scan_results.json
```

#### Subfinder Subdomain Enumeration

Enumerate subdomains:
```bash
python securityscanner.py subfinder -u example.com
```

Save results:
```bash
python securityscanner.py subfinder -u example.com -o subdomains.json
```

Specify sources:
```bash
python securityscanner.py subfinder -u example.com -s virustotal,shodan
```

#### Brute Force Attacks

HTTP Basic Authentication:
```bash
python securityscanner.py bruteforce -u http://example.com/admin -P http-basic --user-list wordlists/usernames.txt --pass-list wordlists/passwords.txt
```

HTTP Form Authentication:
```bash
python securityscanner.py bruteforce -u http://example.com/login -P http-form --username-field username --password-field password --user-list wordlists/usernames.txt --pass-list wordlists/passwords.txt
```

SSH Brute Force:
```bash
python securityscanner.py bruteforce -u 192.168.1.1:22 -P ssh --user-list wordlists/usernames.txt --pass-list wordlists/passwords.txt
```

FTP Brute Force:
```bash
python securityscanner.py bruteforce -u 192.168.1.1:21 -P ftp --user-list wordlists/usernames.txt --pass-list wordlists/passwords.txt
```

#### XSS Vulnerability Scanning

Scan URL for XSS:
```bash
python securityscanner.py xss -u "http://example.com/search?q=test"
```

Scan with custom payloads:
```bash
python securityscanner.py xss -u "http://example.com/search?q=test" -pf custom_payloads.txt
```

Skip form testing:
```bash
python securityscanner.py xss -u "http://example.com/search?q=test" --no-forms
```

Save results:
```bash
python securityscanner.py xss -u "http://example.com/search?q=test" -o xss_results.json
```

## Scan with custom payloads:
```bash
python securityscanner.py xss -u "http://example.com/search?q=test" -pf custom_payloads.txt
```

#### Java/Spring Boot Scan

Scan a single file:
```bash
python securityscanner.py java-scan -f path/to/pom.xml
```

Scan a directory:
```bash
python securityscanner.py java-scan -d path/to/project/root
```

#### AngularJS/Node Scan

Scan a single file:
```bash
python securityscanner.py angular-scan -f path/to/package.json
```

Scan a directory:
```bash
python securityscanner.py angular-scan -d path/to/project/root
```

## Project Structure

```
secTest/
├── securityscanner.py      # Main CLI interface
├── config.py               # Configuration settings
├── requirements.txt        # Python dependencies
├── modules/
│   ├── __init__.py
│   ├── nmap_scanner.py     # Nmap integration
│   ├── subfinder_module.py # Subfinder integration
│   ├── bruteforce.py       # Brute force module
│   ├── xss_scanner.py      # XSS vulnerability scanner
│   ├── java_scanner.py     # Java dependency scanner
│   └── angular_scanner.py  # AngularJS/Node scanner
├── utils/
│   ├── __init__.py
│   └── logger.py           # Colored logging utility
├── wordlists/
│   ├── usernames.txt       # Sample usernames
│   └── passwords.txt       # Sample passwords
├── payloads/
│   └── xss_payloads.txt    # XSS injection payloads
└── output/                 # Scan results directory
```

## Configuration

Edit `config.py` to customize:

- Default wordlist paths
- Nmap timeout and scan arguments
- Subfinder settings
- Brute force delays and threading
- XSS scanner parameters
- User agents and logging settings

## Output

All scan results are saved in JSON format to the `output/` directory. Results include:

- Timestamp of scan
- Target information
- Detailed findings
- Vulnerability details (if applicable)

## Important Notes

### ⚠️ Legal Disclaimer

**THIS TOOL IS FOR AUTHORIZED SECURITY TESTING ONLY**

- You **MUST** have explicit written permission to scan target systems
- Unauthorized access to computer systems is **ILLEGAL**
- The authors assume **NO LIABILITY** for misuse of this tool
- Always comply with local laws and regulations
- Use responsibly and ethically

### Safety Features

- Rate limiting on brute force attempts
- Configurable delays between requests
- Timeout controls
- Progress tracking
- Comprehensive logging

### Limitations

- Nmap requires system-level installation (not just Python library)
- Subfinder is optional but recommended for best results
- Some features may require elevated privileges
- Brute force effectiveness depends on wordlist quality
- XSS detection may produce false positives (manual verification recommended)

## Troubleshooting

### "Nmap not found"
- Ensure Nmap is installed and in system PATH
- On Windows, add Nmap installation directory to PATH

### "Subfinder not found"
- Install Subfinder using Go or download binary
- Add to system PATH or configure path in `config.py`

### "Permission denied" errors
- Some Nmap scans require administrator/root privileges
- Run with elevated permissions or adjust scan type

### Slow scans
- Adjust timeout values in `config.py`
- Reduce wordlist sizes for brute force
- Limit ports being scanned

## Contributing

Contributions are welcome! Please ensure:

- Code follows existing style
- New features include documentation
- Testing is performed before submission
- Ethical use guidelines are maintained

## License

This tool is provided for educational and authorized security testing purposes only.

## Credits

- **Nmap**: Network scanning - https://nmap.org
- **Subfinder**: Subdomain enumeration by ProjectDiscovery - https://github.com/projectdiscovery/subfinder
- **Python Libraries**: python-nmap, requests, beautifulsoup4, colorama, tqdm

---

**Remember**: Always obtain proper authorization before scanning any systems you don't own.
