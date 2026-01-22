#!/usr/bin/env python3
"""
Security Scanner Tool
Comprehensive security scanning tool with Nmap, Subfinder, Brute Force, and XSS scanning
"""
import argparse
import sys
import os
import json
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from modules.nmap_scanner import NmapScanner
from modules.subfinder_module import SubfinderScanner
from modules.bruteforce import BruteForce
from modules.xss_scanner import XSSScanner
from modules.java_scanner import JavaScanner
from modules.angular_scanner import AngularScanner
from modules.android_scanner import AndroidScanner
from modules.ios_scanner import iOSScanner
from utils.logger import setup_logger, success
import config

# Suppress SSL warnings
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = setup_logger('SecurityScanner', log_file=config.LOG_FILE)

BANNER = """
╔═══════════════════════════════════════════════════════════╗
║           SECURITY SCANNER TOOL v1.0                      ║
║   Network Scanning | Subdomain Enum | Brute Force | XSS  ║
╚═══════════════════════════════════════════════════════════╝

⚠️  LEGAL DISCLAIMER ⚠️
This tool is designed for AUTHORIZED SECURITY TESTING ONLY.
You must have EXPLICIT PERMISSION to scan target systems.
Unauthorized access to computer systems is ILLEGAL.
The authors assume NO LIABILITY for misuse of this tool.
"""


def print_banner():
    """Print tool banner"""
    print(BANNER)


def save_results(results, output_file):
    """Save scan results to JSON file"""
    try:
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        success(logger, f"Results saved to {output_file}")
    except Exception as e:
        logger.error(f"Error saving results: {str(e)}")


def nmap_scan_mode(args):
    """Run Nmap scanning"""
    logger.info("=" * 60)
    logger.info("NMAP SCANNING MODE")
    logger.info("=" * 60)
    
    scanner = NmapScanner(timeout=args.timeout)
    
    if args.vuln_scan:
        results = scanner.vulnerability_scan(args.target, ports=args.ports)
    else:
        nmap_args = args.nmap_args if args.nmap_args else '-sV -sC'
        results = scanner.scan_ports(args.target, ports=args.ports, arguments=nmap_args)
    
    if args.output:
        scanner.save_results(results, args.output)
    
    return results


def subfinder_mode(args):
    """Run Subfinder subdomain enumeration"""
    logger.info("=" * 60)
    logger.info("SUBFINDER SUBDOMAIN ENUMERATION MODE")
    logger.info("=" * 60)
    
    scanner = SubfinderScanner(timeout=args.timeout)
    results = scanner.enumerate_subdomains(
        args.domain,
        output_file=args.output,
        sources=args.sources
    )
    
    return results


def bruteforce_mode(args):
    """Run brute force attack"""
    logger.info("=" * 60)
    logger.info("BRUTE FORCE MODE")
    logger.info("=" * 60)
    
    bf = BruteForce(delay=args.delay, timeout=args.timeout)
    
    # Load wordlists
    usernames = args.usernames if args.usernames else config.DEFAULT_USERNAMES
    passwords = args.passwords if args.passwords else config.DEFAULT_PASSWORDS
    
    if args.protocol == 'http-basic':
        results = bf.http_basic_auth(args.target, usernames, passwords)
    elif args.protocol == 'http-form':
        results = bf.http_form_auth(
            args.target,
            args.username_field,
            args.password_field,
            usernames,
            passwords,
            success_string=args.success_string,
            failure_string=args.failure_string
        )
    elif args.protocol == 'ssh':
        host, port = args.target.split(':') if ':' in args.target else (args.target, 22)
        results = bf.ssh_bruteforce(host, int(port), usernames, passwords)
    elif args.protocol == 'ftp':
        host, port = args.target.split(':') if ':' in args.target else (args.target, 21)
        results = bf.ftp_bruteforce(host, int(port), usernames, passwords)
    else:
        logger.error(f"Unknown protocol: {args.protocol}")
        return None
    
    if args.output:
        save_results(results, args.output)
    
    return results


def xss_scan_mode(args):
    """Run XSS scanning"""
    logger.info("=" * 60)
    logger.info("XSS VULNERABILITY SCANNING MODE")
    logger.info("=" * 60)
    
    payload_file = args.payload_file if args.payload_file else config.XSS_PAYLOADS_FILE
    
    scanner = XSSScanner(timeout=args.timeout, max_payloads=args.max_payloads)
    results = scanner.scan_url(args.url, payload_file, test_forms=not args.no_forms)
    
    if args.output:
        save_results(results, args.output)
    
    return results


def android_scan_mode(args):
    """Run Android security scanning"""
    logger.info("=" * 60)
    logger.info("ANDROID SECURITY SCANNING MODE")
    logger.info("=" * 60)
    
    scanner = AndroidScanner()
    if args.directory:
        results = scanner.scan_directory(args.directory)
    else:
        logger.error("Please specify a directory to scan.")
        return

    # Print summary
    if results.get('manifest_issues'):
         logger.warning(f"Found {len(results['manifest_issues'])} manifest issues!")
         for issue in results['manifest_issues']:
             print(f"\n[!] {issue['rule']} ({issue['severity']}) in {issue['file']}")
             print(f"    Possible issue: {issue['description']}")

    if results.get('code_issues'):
         logger.warning(f"Found {len(results['code_issues'])} code security issues!")
         for issue in results['code_issues']:
             print(f"\n[!] {issue['rule']} ({issue['severity']}) in {issue['file']}:{issue['line']}")
             print(f"    Possible issue: {issue['description']}")
             print(f"    Code: {issue['snippet']}")

    if args.output:
        save_results(results, args.output)
    
    return results


def ios_scan_mode(args):
    """Run iOS security scanning"""
    logger.info("=" * 60)
    logger.info("iOS SECURITY SCANNING MODE")
    logger.info("=" * 60)
    
    scanner = iOSScanner()
    if args.directory:
        results = scanner.scan_directory(args.directory)
    else:
        logger.error("Please specify a directory to scan.")
        return

    # Print summary
    if results.get('plist_issues'):
         logger.warning(f"Found {len(results['plist_issues'])} configuration issues!")
         for issue in results['plist_issues']:
             print(f"\n[!] {issue['rule']} ({issue['severity']}) in {issue['file']}")
             print(f"    Possible issue: {issue['description']}")

    if results.get('code_issues'):
         logger.warning(f"Found {len(results['code_issues'])} code security issues!")
         for issue in results['code_issues']:
             print(f"\n[!] {issue['rule']} ({issue['severity']}) in {issue['file']}:{issue['line']}")
             print(f"    Possible issue: {issue['description']}")
             print(f"    Code: {issue['snippet']}")

    if args.output:
        save_results(results, args.output)
    
    return results


    return results


def java_scan_mode(args):
    """Run Java/Spring Boot dependency scanning"""
    logger.info("=" * 60)
    logger.info("JAVA/SPRING BOOT SECURITY SCANNING MODE")
    logger.info("=" * 60)
    
    scanner = JavaScanner()
    if args.file:
        # Scan single file
        if args.file.endswith('pom.xml'):
            vulns = scanner.scan_maven(args.file)
        elif args.file.endswith('build.gradle'):
            vulns = scanner.scan_gradle(args.file)
        else:
            logger.error("Unsupported file type. Use pom.xml or build.gradle")
            return
            
        results = {
            'vulnerabilities': vulns,
            'code_issues': [],
            'files_analyzed': [args.file]
        }
    else:
        # Scan directory
        results = scanner.scan_directory(args.directory)
    
    # Print summary
    if results['vulnerabilities']:
        logger.warning(f"Found {len(results['vulnerabilities'])} dependency vulnerabilities!")
        for vuln in results['vulnerabilities']:
            print(f"\n[!] Vulnerability in {vuln['dependency']} ({vuln['file']}):")
            for v in vuln['vulnerability']:
                print(f"    - {v.get('id')}: {v.get('summary')}")
    else:
        success(logger, "No vulnerabilities found in dependencies.")

    # SAST Summary
    if results.get('code_issues'):
         logger.warning(f"Found {len(results['code_issues'])} code security issues!")
         for issue in results['code_issues']:
             print(f"\n[!] {issue['rule']} ({issue['severity']}) in {issue['file']}:{issue['line']}")
             print(f"    Possible issue: {issue['description']}")
             print(f"    Code: {issue['snippet']}")

    if args.output:
        save_results(results, args.output)
    
    return results


def angular_scan_mode(args):
    """Run AngularJS/Node dependency scanning"""
    logger.info("=" * 60)
    logger.info("ANGULARJS/NODE SECURITY SCANNING MODE")
    logger.info("=" * 60)
    
    scanner = AngularScanner()
    if args.file:
        # Scan single file
        if args.file.endswith('package.json'):
            vulns = scanner.scan_package_json(args.file)
        else:
            logger.error("Unsupported file type. Use package.json")
            return
            
        results = {
            'vulnerabilities': vulns,
            'files_analyzed': [args.file]
        }
    else:
        # Scan directory
        results = scanner.scan_directory(args.directory)
    
    # Print summary
    if results['vulnerabilities']:
        logger.warning(f"Found {len(results['vulnerabilities'])} vulnerabilities!")
        for vuln in results['vulnerabilities']:
            print(f"\n[!] Vulnerability in {vuln['dependency']} ({vuln['file']}):")
            for v in vuln['vulnerability']:
                print(f"    - {v.get('id')}: {v.get('summary')}")
    else:
        success(logger, "No vulnerabilities found in dependencies.")
        
    if args.output:
        save_results(results, args.output)
    
    return results


def interactive_mode():
    """Interactive menu-driven interface"""
    print_banner()
    
    while True:
        print("\n" + "=" * 60)
        print("SELECT SCANNING MODE:")
        print("=" * 60)
        print("1. Nmap Port Scanning")
        print("2. Subfinder Subdomain Enumeration")
        print("3. Brute Force Attack")
        print("4. XSS Vulnerability Scanning")
        print("5. Java/Spring Boot Dependency Scan")
        print("6. AngularJS/Node Dependency Scan")
        print("7. Android Security Scan")
        print("8. iOS Security Scan")
        print("9. Exit")
        print("=" * 60)
        
        choice = input("\nEnter your choice (1-9): ").strip()
        
        if choice == '1':
            target = input("Enter target IP/hostname: ").strip()
            ports = input("Enter ports (common/all/custom): ").strip() or 'common'
            
            scanner = NmapScanner()
            results = scanner.scan_ports(target, ports=ports)
            
            output = input("\nSave results? (y/N): ").strip().lower()
            if output == 'y':
                filename = f"output/nmap_{target.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                save_results(results, filename)
        
        elif choice == '2':
            domain = input("Enter target domain: ").strip()
            
            scanner = SubfinderScanner()
            results = scanner.enumerate_subdomains(domain)
            
            output = input("\nSave results? (y/N): ").strip().lower()
            if output == 'y':
                filename = f"output/subfinder_{domain.replace('.', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                save_results(results, filename)
        
        elif choice == '3':
            print("\nBRUTE FORCE OPTIONS:")
            print("1. HTTP Basic Auth")
            print("2. HTTP Form Auth")
            print("3. SSH")
            print("4. FTP")
            
            bf_choice = input("Select protocol (1-4): ").strip()
            target = input("Enter target URL/host: ").strip()
            
            bf = BruteForce()
            
            if bf_choice == '1':
                results = bf.http_basic_auth(target, config.DEFAULT_USERNAMES, config.DEFAULT_PASSWORDS)
            elif bf_choice == '2':
                username_field = input("Username field name: ").strip()
                password_field = input("Password field name: ").strip()
                results = bf.http_form_auth(target, username_field, password_field, 
                                           config.DEFAULT_USERNAMES, config.DEFAULT_PASSWORDS)
            elif bf_choice == '3':
                host, port = target.split(':') if ':' in target else (target, 22)
                results = bf.ssh_bruteforce(host, int(port), config.DEFAULT_USERNAMES, config.DEFAULT_PASSWORDS)
            elif bf_choice == '4':
                host, port = target.split(':') if ':' in target else (target, 21)
                results = bf.ftp_bruteforce(host, int(port), config.DEFAULT_USERNAMES, config.DEFAULT_PASSWORDS)
            
            output = input("\nSave results? (y/N): ").strip().lower()
            if output == 'y':
                filename = f"output/bruteforce_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                save_results(results, filename)
        
        elif choice == '4':
            url = input("Enter target URL: ").strip()
            
            scanner = XSSScanner()
            results = scanner.scan_url(url, config.XSS_PAYLOADS_FILE)
            
            output = input("\nSave results? (y/N): ").strip().lower()
            if output == 'y':
                filename = f"output/xss_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                save_results(results, filename)

        elif choice == '5':
            path = input("Enter directory or file path (pom.xml/build.gradle): ").strip()
            scanner = JavaScanner()
            if os.path.isfile(path):
                if path.endswith('pom.xml'):
                    vulns = scanner.scan_maven(path)
                elif path.endswith('build.gradle'):
                    vulns = scanner.scan_gradle(path)
                else: 
                    print("Invalid file.")
                    continue
                results = {'vulnerabilities': vulns, 'files_analyzed': [path]}
            else:
                 results = scanner.scan_directory(path)

            output = input("\nSave results? (y/N): ").strip().lower()
            if output == 'y':
                filename = f"output/java_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                save_results(results, filename)

        elif choice == '6':
            path = input("Enter directory or file path (package.json): ").strip()
            scanner = AngularScanner()
            if os.path.isfile(path):
                vulns = scanner.scan_package_json(path)
                results = {'vulnerabilities': vulns, 'files_analyzed': [path]}
            else:
                results = scanner.scan_directory(path)

            output = input("\nSave results? (y/N): ").strip().lower()
            if output == 'y':
                filename = f"output/angular_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                save_results(results, filename)
        
        elif choice == '7':
            path = input("Enter project directory to scan: ").strip()
            scanner = AndroidScanner()
            results = scanner.scan_directory(path)
            
            output = input("\nSave results? (y/N): ").strip().lower()
            if output == 'y':
                filename = f"output/android_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                save_results(results, filename)

        elif choice == '8':
            path = input("Enter project directory to scan: ").strip()
            scanner = iOSScanner()
            results = scanner.scan_directory(path)
            
            output = input("\nSave results? (y/N): ").strip().lower()
            if output == 'y':
                filename = f"output/ios_scan_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                save_results(results, filename)

        elif choice == '9':
            print("\nExiting... Stay safe!")
            break
        
        else:
            print("\n❌ Invalid choice. Please try again.")


def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Security Scanner Tool - Nmap, Subfinder, Brute Force, and XSS Scanner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode
  python securityscanner.py
  
  # Nmap scan
  python securityscanner.py nmap -u 192.168.1.1 -p common
  
  # Subfinder
  python securityscanner.py subfinder -u example.com
  
  # Brute force HTTP
  python securityscanner.py bruteforce -u http://example.com -P http-basic
  
  # XSS scan
  python securityscanner.py xss -u "http://example.com/search?q=test"
        """
    )
    
    subparsers = parser.add_subparsers(dest='mode', help='Scanning mode')
    
    # Nmap scanner
    nmap_parser = subparsers.add_parser('nmap', help='Nmap port scanning')
    nmap_parser.add_argument('-u', '--url', required=True, help='Target IP or hostname', dest='target')
    nmap_parser.add_argument('-p', '--ports', default='common', help='Ports to scan (common/all/custom)')
    nmap_parser.add_argument('-a', '--nmap-args', help='Additional Nmap arguments')
    nmap_parser.add_argument('-v', '--vuln-scan', action='store_true', help='Run vulnerability scan')
    nmap_parser.add_argument('-o', '--output', help='Output file')
    nmap_parser.add_argument('--timeout', type=int, default=300, help='Scan timeout')
    
    # Subfinder
    subfinder_parser = subparsers.add_parser('subfinder', help='Subfinder subdomain enumeration')
    subfinder_parser.add_argument('-u', '--url', required=True, help='Target domain', dest='domain')
    subfinder_parser.add_argument('-s', '--sources', help='Specific sources (comma-separated)')
    subfinder_parser.add_argument('-o', '--output', help='Output file')
    subfinder_parser.add_argument('--timeout', type=int, default=120, help='Scan timeout')
    
    # Brute force
    bf_parser = subparsers.add_parser('bruteforce', help='Brute force attack')
    bf_parser.add_argument('-u', '--url', required=True, help='Target URL or host', dest='target')
    bf_parser.add_argument('-P', '--protocol', required=True, 
                          choices=['http-basic', 'http-form', 'ssh', 'ftp'],
                          help='Authentication protocol')
    bf_parser.add_argument('--user-list', help='Username wordlist file', dest='usernames')
    bf_parser.add_argument('--pass-list', help='Password wordlist file', dest='passwords')
    bf_parser.add_argument('--username-field', help='Username field name (for http-form)')
    bf_parser.add_argument('--password-field', help='Password field name (for http-form)')
    bf_parser.add_argument('--success-string', help='Success indicator string')
    bf_parser.add_argument('--failure-string', help='Failure indicator string')
    bf_parser.add_argument('--delay', type=float, default=0.5, help='Delay between attempts')
    bf_parser.add_argument('--timeout', type=int, default=10, help='Request timeout')
    bf_parser.add_argument('-o', '--output', help='Output file')
    
    # XSS scanner
    xss_parser = subparsers.add_parser('xss', help='XSS vulnerability scanning')
    xss_parser.add_argument('-u', '--url', required=True, help='Target URL', dest='url')
    xss_parser.add_argument('-pf', '--payload-file', help='XSS payload file')
    xss_parser.add_argument('--max-payloads', type=int, default=50, help='Maximum payloads to test')
    xss_parser.add_argument('--no-forms', action='store_true', help='Skip form testing')
    xss_parser.add_argument('--timeout', type=int, default=10, help='Request timeout')
    xss_parser.add_argument('-o', '--output', help='Output file')
    
    # Java Scanner
    java_parser = subparsers.add_parser('java-scan', help='Java/Spring Boot dependency scanning')
    java_group = java_parser.add_mutually_exclusive_group(required=True)
    java_group.add_argument('-d', '--directory', help='Project directory to scan')
    java_group.add_argument('-f', '--file', help='Specific pom.xml or build.gradle file')
    java_parser.add_argument('-o', '--output', help='Output file')

    # Angular Scanner
    ng_parser = subparsers.add_parser('angular-scan', help='AngularJS/Node dependency scanning')
    ng_group = ng_parser.add_mutually_exclusive_group(required=True)
    ng_group.add_argument('-d', '--directory', help='Project directory to scan')
    ng_group.add_argument('-f', '--file', help='Specific package.json file')
    ng_parser.add_argument('-o', '--output', help='Output file')

    # Android Scanner
    android_parser = subparsers.add_parser('android-scan', help='Android security scanning')
    android_parser.add_argument('-d', '--directory', required=True, help='Project directory to scan')
    android_parser.add_argument('-o', '--output', help='Output file')

    # iOS Scanner
    ios_parser = subparsers.add_parser('ios-scan', help='iOS security scanning')
    ios_parser.add_argument('-d', '--directory', required=True, help='Project directory to scan')
    ios_parser.add_argument('-o', '--output', help='Output file')
    
    args = parser.parse_args()
    
    # If no mode specified, run interactive mode
    if not args.mode:
        interactive_mode()
        return 0
    
    # Print banner for CLI mode
    print_banner()
    
    # Execute selected mode
    try:
        if args.mode == 'nmap':
            nmap_scan_mode(args)
        elif args.mode == 'subfinder':
            subfinder_mode(args)
        elif args.mode == 'bruteforce':
            bruteforce_mode(args)
        elif args.mode == 'xss':
            xss_scan_mode(args)
        elif args.mode == 'java-scan':
            java_scan_mode(args)
        elif args.mode == 'angular-scan':
            angular_scan_mode(args)
        elif args.mode == 'android-scan':
            android_scan_mode(args)
        elif args.mode == 'ios-scan':
            ios_scan_mode(args)
        
        success(logger, "Scan completed successfully!")
        return 0
        
    except KeyboardInterrupt:
        logger.warning("\nScan interrupted by user")
        return 1
    except Exception as e:
        logger.error(f"Error during scan: {str(e)}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
