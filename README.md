# Security Scanner Tool

A comprehensive Python-based security scanning tool that combines network scanning, subdomain enumeration, credential brute forcing, and XSS vulnerability detection.

## Features

- **🔍 Nmap Port Scanner**: Network reconnaissance with port scanning, service detection, OS detection, and vulnerability scanning
- **🌐 Subfinder Integration**: Passive subdomain enumeration for target domains
- **🔐 Brute Force Module**: Credential testing for HTTP (Basic/Form), SSH, and FTP
- **⚠️ XSS Scanner**: Cross-site scripting vulnerability detection with multiple payload injection vectors

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

### Interactive Mode

Run without arguments for an interactive menu:

```bash
python securityscanner.py
```

### Command-Line Mode

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
│   └── xss_scanner.py      # XSS vulnerability scanner
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
