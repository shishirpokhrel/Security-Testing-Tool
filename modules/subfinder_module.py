"""
Subfinder Module
Subdomain enumeration using subfinder tool
"""
import subprocess
import json
import os
from datetime import datetime
from utils.logger import setup_logger, success

logger = setup_logger('SubfinderModule')


class SubfinderScanner:
    """Subdomain enumeration using subfinder"""
    
    def __init__(self, subfinder_path='subfinder', timeout=120):
        """
        Initialize Subfinder scanner
        
        Args:
            subfinder_path: Path to subfinder binary
            timeout: Command timeout in seconds
        """
        self.subfinder_path = subfinder_path
        self.timeout = timeout
        self._check_subfinder()
    
    def _check_subfinder(self):
        """Check if subfinder is installed"""
        try:
            result = subprocess.run(
                [self.subfinder_path, '-version'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info(f"Subfinder found: {result.stdout.strip()}")
                return True
        except FileNotFoundError:
            logger.warning("Subfinder not found in PATH")
            logger.warning("Please install subfinder: https://github.com/projectdiscovery/subfinder")
            return False
        except Exception as e:
            logger.warning(f"Error checking subfinder: {str(e)}")
            return False
    
    def enumerate_subdomains(self, domain, output_file=None, silent=True, sources=None):
        """
        Enumerate subdomains for a given domain
        
        Args:
            domain: Target domain
            output_file: Output file path (optional)
            silent: Silent mode (show only subdomains)
            sources: Specific sources to use (comma-separated)
            
        Returns:
            dict: Enumeration results
        """
        logger.info(f"Enumerating subdomains for {domain}")
        
        try:
            # Build command
            cmd = [self.subfinder_path, '-d', domain]
            
            if silent:
                cmd.append('-silent')
            
            if sources:
                cmd.extend(['-sources', sources])
            
            # Add JSON output
            cmd.append('-json')
            
            logger.info(f"Running command: {' '.join(cmd)}")
            
            # Run subfinder
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout
            )
            
            if result.returncode != 0:
                logger.error(f"Subfinder error: {result.stderr}")
                return {
                    'domain': domain,
                    'error': result.stderr,
                    'subdomains': []
                }
            
            # Parse JSON output
            subdomains = []
            for line in result.stdout.strip().split('\n'):
                if line:
                    try:
                        data = json.loads(line)
                        subdomains.append({
                            'host': data.get('host', ''),
                            'source': data.get('source', ''),
                            'ip': data.get('ip', [])
                        })
                    except json.JSONDecodeError:
                        # Handle non-JSON output
                        subdomains.append({
                            'host': line.strip(),
                            'source': 'unknown',
                            'ip': []
                        })
            
            results = {
                'domain': domain,
                'scan_time': datetime.now().isoformat(),
                'subdomains_count': len(subdomains),
                'subdomains': subdomains
            }
            
            # Log results
            logger.info(f"Found {len(subdomains)} subdomains")
            for sub in subdomains[:10]:  # Show first 10
                logger.info(f"  - {sub['host']}")
            if len(subdomains) > 10:
                logger.info(f"  ... and {len(subdomains) - 10} more")
            
            # Save to file if specified
            if output_file:
                self.save_results(results, output_file)
            
            success(logger, f"Subdomain enumeration completed for {domain}")
            return results
            
        except subprocess.TimeoutExpired:
            logger.error(f"Subfinder timeout after {self.timeout} seconds")
            return {
                'domain': domain,
                'error': 'Timeout',
                'subdomains': []
            }
        except FileNotFoundError:
            logger.error("Subfinder not found. Please install it first.")
            logger.info("Install: go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest")
            return {
                'domain': domain,
                'error': 'Subfinder not installed',
                'subdomains': []
            }
        except Exception as e:
            logger.error(f"Error during enumeration: {str(e)}")
            return {
                'domain': domain,
                'error': str(e),
                'subdomains': []
            }
    
    def save_results(self, results, filename):
        """
        Save enumeration results to file
        
        Args:
            results: Enumeration results dictionary
            filename: Output filename
        """
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            success(logger, f"Results saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")
    
    def list_sources(self):
        """List available sources"""
        try:
            result = subprocess.run(
                [self.subfinder_path, '-ls'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                logger.info("Available sources:")
                print(result.stdout)
            return result.stdout
        except Exception as e:
            logger.error(f"Error listing sources: {str(e)}")
            return None


def main():
    """Test function"""
    scanner = SubfinderScanner()
    results = scanner.enumerate_subdomains('example.com')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
