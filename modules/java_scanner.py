import os
import re
import config
import requests
import xml.etree.ElementTree as ET
from utils.logger import setup_logger

class JavaScanner:
    def __init__(self):
        self.logger = setup_logger('JavaScanner')
        self.osv_api_url = config.OSV_API_URL

    def scan_directory(self, directory_path):
        """
        Scans a directory for Java project files (pom.xml, build.gradle)
        and checks dependencies against OSV database.
        """
        self.logger.info(f"Scanning directory for Java projects: {directory_path}")
        results = {
            'vulnerabilities': [],
            'dependencies_scanned': 0,
            'code_issues': [],
            'files_analyzed': []
        }

        if not os.path.isdir(directory_path):
            self.logger.error(f"Invalid directory: {directory_path}")
            return results

        for root, dirs, files in os.walk(directory_path):
            if 'pom.xml' in files:
                pom_path = os.path.join(root, 'pom.xml')
                results['files_analyzed'].append(pom_path)
                vulns = self.scan_maven(pom_path)
                results['vulnerabilities'].extend(vulns)
                
            if 'build.gradle' in files:
                gradle_path = os.path.join(root, 'build.gradle')
                results['files_analyzed'].append(gradle_path)
                vulns = self.scan_gradle(gradle_path)
                results['vulnerabilities'].extend(vulns)

            for file in files:
                if file.endswith('.java'):
                    java_file_path = os.path.join(root, file)
                    issues = self.scan_code(java_file_path)
                    results['code_issues'].extend(issues)

        results['dependencies_scanned'] = len(results['vulnerabilities'])
        return results

    def scan_code(self, file_path):
        """
        Scans Java source code for security patterns.
        """
        issues = []
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                
            for i, line in enumerate(lines):
                for rule_name, rule_data in config.JAVA_SAST_RULES.items():
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

    def scan_maven(self, pom_path):
        """Parses pom.xml and checks dependencies."""
        self.logger.info(f"Analyzing Maven file: {pom_path}")
        vulnerabilities = []
        try:
            tree = ET.parse(pom_path)
            root = tree.getroot()
            # Handle namespaces if present, usually xmlns="http://maven.apache.org/POM/4.0.0"
            ns = {'mvn': 'http://maven.apache.org/POM/4.0.0'}
            
            # Find dependencies
            dependencies = root.findall(".//mvn:dependency", ns)
            if not dependencies:
                 # Try without namespace if not found
                 dependencies = root.findall(".//dependency")

            for dep in dependencies:
                # Extract GroupId, ArtifactId, Version
                group_id_elem = dep.find("mvn:groupId", ns)
                if group_id_elem is None: group_id_elem = dep.find("groupId")
                
                artifact_id_elem = dep.find("mvn:artifactId", ns)
                if artifact_id_elem is None: artifact_id_elem = dep.find("artifactId")
                
                version_elem = dep.find("mvn:version", ns)
                if version_elem is None: version_elem = dep.find("version")

                if group_id_elem is not None and artifact_id_elem is not None and version_elem is not None:
                    g = group_id_elem.text
                    a = artifact_id_elem.text
                    v = version_elem.text
                    
                    # Resolve properties like ${project.version} - simplified
                    if v and v.startswith('${') and v.endswith('}'):
                        prop_name = v[2:-1]
                        # Try to find property in properties section
                        prop_val = root.find(f".//mvn:properties/mvn:{prop_name}", ns)
                        if prop_val is None: prop_val = root.find(f".//properties/{prop_name}")
                        if prop_val is not None:
                            v = prop_val.text

                    if v:
                        vuln = self.check_osv(g, a, v)
                        if vuln:
                            vulnerabilities.append({
                                'file': pom_path,
                                'dependency': f"{g}:{a}:{v}",
                                'vulnerability': vuln
                            })
        except Exception as e:
            self.logger.error(f"Error parsing pom.xml: {str(e)}")
        
        return vulnerabilities

    def scan_gradle(self, gradle_path):
        """Parses build.gradle and checks dependencies (Basic Regex Parsing)."""
        self.logger.info(f"Analyzing Gradle file: {gradle_path}")
        vulnerabilities = []
        try:
            with open(gradle_path, 'r') as f:
                content = f.read()
            
            # Regex for implementation 'group:artifact:version' or implementation group: '...', name: '...', version: '...'
            # Simplified regex for 'group:name:version'
            # implementation "com.google.guava:guava:30.1.1-jre"
            short_pattern = r"[\"']([a-zA-Z0-9\._-]+):([a-zA-Z0-9\._-]+):([a-zA-Z0-9\._-]+)[\"']"
            matches = re.findall(short_pattern, content)
            
            for g, a, v in matches:
                vuln = self.check_osv(g, a, v)
                if vuln:
                     vulnerabilities.append({
                        'file': gradle_path,
                        'dependency': f"{g}:{a}:{v}",
                        'vulnerability': vuln
                    })
                    
        except Exception as e:
            self.logger.error(f"Error reading build.gradle: {str(e)}")

        return vulnerabilities

    def check_osv(self, group_id, artifact_id, version):
        """Query OSV API for vulnerabilities."""
        try:
            payload = {
                "package": {
                    "name": f"{group_id}:{artifact_id}",
                    "ecosystem": "Maven"
                },
                "version": version
            }
            response = requests.post(self.osv_api_url, json=payload, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'vulns' in data:
                    return data['vulns']
        except Exception as e:
            self.logger.warning(f"OSV API request failed for {group_id}:{artifact_id}: {str(e)}")
        return None
