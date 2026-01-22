import os
import re
import config
import plistlib
from utils.logger import setup_logger

class iOSScanner:
    def __init__(self):
        self.logger = setup_logger('iOSScanner')

    def scan_directory(self, directory_path):
        """Scans directory for iOS vulnerabilities."""
        self.logger.info(f"Scanning directory for iOS projects: {directory_path}")
        results = {
            'plist_issues': [],
            'code_issues': [],
            'files_analyzed': []
        }

        if not os.path.isdir(directory_path):
            self.logger.error(f"Invalid directory: {directory_path}")
            return results

        for root, dirs, files in os.walk(directory_path):
            # Check for Info.plist
            if config.IOS_SCAN_CONFIG['plist_file'] in files:
                plist_path = os.path.join(root, config.IOS_SCAN_CONFIG['plist_file'])
                results['files_analyzed'].append(plist_path)
                issues = self.scan_plist(plist_path)
                results['plist_issues'].extend(issues)

            # Check for source code files
            for file in files:
                if any(file.endswith(ext) for ext in config.IOS_SCAN_CONFIG['extensions']):
                    # Skip plist as it is already scanned
                    if file == config.IOS_SCAN_CONFIG['plist_file']:
                        continue
                        
                    file_path = os.path.join(root, file)
                    issues = self.scan_code(file_path)
                    results['code_issues'].extend(issues)

        return results

    def scan_plist(self, plist_path):
        """Checks Info.plist for insecure configurations."""
        issues = []
        try:
            with open(plist_path, 'rb') as f:
                try:
                    plist_data = plistlib.load(f)
                except Exception:
                    # Fallback for XML plists that failing binary load
                    f.seek(0)
                    # Simple text check if plistlib fails
                    content = f.read().decode('utf-8', errors='ignore')
                    if 'NSAllowsArbitraryLoads' in content:
                         issues.append({
                            'file': plist_path,
                            'rule': 'App Transport Security',
                            'severity': 'HIGH',
                            'description': 'Potential ATS bypass detected (NSAllowsArbitraryLoads).'
                        })
                    return issues

            # Check parsed plist structure
            for check_name, check_data in config.IOS_PLIST_CHECKS.items():
                key = check_data.get('key')
                sub_key = check_data.get('sub_key')
                target_value = check_data.get('value')

                if key in plist_data:
                    val = plist_data[key]
                    if sub_key and isinstance(val, dict):
                        if val.get(sub_key) == target_value:
                            issues.append({
                                'file': plist_path,
                                'rule': check_name,
                                'severity': check_data['severity'],
                                'description': check_data['description']
                            })
                    elif val == target_value:
                        issues.append({
                            'file': plist_path,
                            'rule': check_name,
                            'severity': check_data['severity'],
                            'description': check_data['description']
                        })
        except Exception as e:
            self.logger.error(f"Error scanning plist {plist_path}: {str(e)}")
        return issues

    def scan_code(self, file_path):
        """Scans Swift/ObjC code for pattern-based vulnerabilities."""
        issues = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                for rule_name, rule_data in config.IOS_SAST_RULES.items():
                    if re.search(rule_data['pattern'], line):
                        issues.append({
                            'file': file_path,
                            'line': i + 1,
                            'rule': rule_name,
                            'severity': rule_data['severity'],
                            'description': rule_data['description'],
                            'snippet': line.strip()[:100]
                        })
        except Exception as e:
            self.logger.error(f"Error scanning file {file_path}: {str(e)}")
        return issues
