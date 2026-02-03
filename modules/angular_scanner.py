import os
import json
import config
import requests
from utils.logger import setup_logger

class AngularScanner:
    def __init__(self):
        self.logger = setup_logger('AngularScanner')
        self.osv_api_url = config.OSV_API_URL

    def scan_directory(self, directory_path):
        """
        Scans a directory for Angular project files (package.json)
        and checks dependencies against OSV database.
        """
        self.logger.info(f"Scanning directory for Angular/Node projects: {directory_path}")
        results = {
            'vulnerabilities': [],
            'dependencies_scanned': 0,
            'files_analyzed': []
        }

        if not os.path.isdir(directory_path):
            self.logger.error(f"Invalid directory: {directory_path}")
            return results

        for root, dirs, files in os.walk(directory_path):
            if 'node_modules' in dirs:
                dirs.remove('node_modules') # Skip node_modules to avoid scanning installed packages directly if we just want manifest
            
            if 'package.json' in files:
                package_path = os.path.join(root, 'package.json')
                results['files_analyzed'].append(package_path)
                vulns = self.scan_package_json(package_path)
                results['vulnerabilities'].extend(vulns)

        results['dependencies_scanned'] = len(results['vulnerabilities']) # Placeholder
        return results

    def scan_package_json(self, package_path):
        """Parses package.json and checks dependencies."""
        self.logger.info(f"Analyzing package.json: {package_path}")
        vulnerabilities = []
        try:
            with open(package_path, 'r') as f:
                data = json.load(f)
            
            dependencies = data.get('dependencies', {})
            dev_dependencies = data.get('devDependencies', {})
            
            # Combine both
            all_deps = {**dependencies, **dev_dependencies}

            for name, version in all_deps.items():
                # Clean version string (remove ^, ~, etc.)
                clean_version = version.replace('^', '').replace('~', '')
                # Handle simplified cases only for now (valid semantic versions)
                
                vuln = self.check_osv(name, clean_version)
                if vuln:
                    vulnerabilities.append({
                        'file': package_path,
                        'dependency': f"{name}@{clean_version}",
                        'vulnerability': vuln
                    })
                    
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON in {package_path}")
        except Exception as e:
            self.logger.error(f"Error analyzing package.json: {str(e)}")
        
        return vulnerabilities

    def check_osv(self, name, version):
        """Query OSV API for vulnerabilities."""
        try:
            payload = {
                "package": {
                    "name": name,
                    "ecosystem": "npm"
                },
                "version": version
            }
            response = requests.post(self.osv_api_url, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'vulns' in data:
                    return data['vulns']
        except Exception as e:
            self.logger.warning(f"OSV API request failed for {name}@{version}: {str(e)}")
        return None
