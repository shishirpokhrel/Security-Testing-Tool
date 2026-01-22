import os
import re
import config
from utils.logger import setup_logger

class AndroidScanner:
    def __init__(self):
        self.logger = setup_logger('AndroidScanner')

    def scan_directory(self, directory_path):
        """Scans directory for Android vulnerabilities."""
        self.logger.info(f"Scanning directory for Android projects: {directory_path}")
        results = {
            'manifest_issues': [],
            'code_issues': [],
            'files_analyzed': []
        }

        if not os.path.isdir(directory_path):
            self.logger.error(f"Invalid directory: {directory_path}")
            return results

        for root, dirs, files in os.walk(directory_path):
            # Check for AndroidManifest.xml
            if config.ANDROID_SCAN_CONFIG['manifest_file'] in files:
                manifest_path = os.path.join(root, config.ANDROID_SCAN_CONFIG['manifest_file'])
                results['files_analyzed'].append(manifest_path)
                issues = self.scan_manifest(manifest_path)
                results['manifest_issues'].extend(issues)

            # Check for source code files
            for file in files:
                if any(file.endswith(ext) for ext in config.ANDROID_SCAN_CONFIG['extensions']):
                    # Skip manifest as it is already scanned
                    if file == config.ANDROID_SCAN_CONFIG['manifest_file']:
                        continue
                        
                    file_path = os.path.join(root, file)
                    issues = self.scan_code(file_path)
                    results['code_issues'].extend(issues)

        return results

    def scan_manifest(self, manifest_path):
        """Checks AndroidManifest.xml for insecure configurations."""
        issues = []
        try:
            with open(manifest_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            for check_name, check_data in config.ANDROID_MANIFEST_CHECKS.items():
                if re.search(check_data['pattern'], content):
                    issues.append({
                        'file': manifest_path,
                        'rule': check_name,
                        'severity': check_data['severity'],
                        'description': check_data['description']
                    })
        except Exception as e:
            self.logger.error(f"Error scanning manifest {manifest_path}: {str(e)}")
        return issues

    def scan_code(self, file_path):
        """Scans Java/Kotlin code for pattern-based vulnerabilities."""
        issues = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()

            for i, line in enumerate(lines):
                for rule_name, rule_data in config.ANDROID_SAST_RULES.items():
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
