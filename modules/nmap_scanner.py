"""
Nmap Scanner Module
Provides network scanning capabilities using python-nmap
"""
import nmap
import json
from datetime import datetime
from utils.logger import setup_logger, success

logger = setup_logger('NmapScanner')


class NmapScanner:
    """Network scanner using Nmap"""
    
    def __init__(self, timeout=300):
        """
        Initialize Nmap scanner
        
        Args:
            timeout: Scan timeout in seconds
        """
        self.timeout = timeout
        self.nm = nmap.PortScanner()
        
    def scan_ports(self, target, ports='common', arguments='-sV -sC'):
        """
        Scan ports on target
        
        Args:
            target: Target IP or hostname
            ports: Port specification ('common', 'all', or specific like '80,443,8080')
            arguments: Nmap arguments
            
        Returns:
            dict: Scan results
        """
        logger.info(f"Starting port scan on {target}")
        
        # Define port ranges
        if ports == 'common':
            port_range = '21,22,23,25,53,80,110,111,135,139,143,443,445,993,995,1723,3306,3389,5900,8080'
        elif ports == 'all':
            port_range = '1-65535'
        else:
            port_range = ports
            
        try:
            logger.info(f"Scanning ports: {port_range}")
            logger.info(f"Arguments: {arguments}")
            
            # Perform scan
            self.nm.scan(hosts=target, ports=port_range, arguments=arguments, timeout=self.timeout)
            
            results = {
                'target': target,
                'scan_time': datetime.now().isoformat(),
                'hosts': {}
            }
            
            # Parse results
            for host in self.nm.all_hosts():
                logger.info(f"Host: {host} ({self.nm[host].hostname()})")
                logger.info(f"State: {self.nm[host].state()}")
                
                host_info = {
                    'hostname': self.nm[host].hostname(),
                    'state': self.nm[host].state(),
                    'protocols': {}
                }
                
                # Get protocol information
                for proto in self.nm[host].all_protocols():
                    logger.info(f"Protocol: {proto}")
                    
                    ports_info = {}
                    lport = sorted(self.nm[host][proto].keys())
                    
                    for port in lport:
                        port_data = self.nm[host][proto][port]
                        state = port_data['state']
                        service = port_data.get('name', 'unknown')
                        product = port_data.get('product', '')
                        version = port_data.get('version', '')
                        
                        logger.info(f"Port: {port}\tState: {state}\tService: {service} {product} {version}")
                        
                        ports_info[port] = {
                            'state': state,
                            'service': service,
                            'product': product,
                            'version': version,
                            'extrainfo': port_data.get('extrainfo', ''),
                            'cpe': port_data.get('cpe', '')
                        }
                    
                    host_info['protocols'][proto] = ports_info
                
                # OS Detection
                if 'osmatch' in self.nm[host]:
                    os_matches = []
                    for osmatch in self.nm[host]['osmatch']:
                        os_matches.append({
                            'name': osmatch['name'],
                            'accuracy': osmatch['accuracy']
                        })
                    host_info['os_matches'] = os_matches
                    logger.info(f"OS Detection: {os_matches[0]['name'] if os_matches else 'Unknown'}")
                
                results['hosts'][host] = host_info
            
            success(logger, f"Scan completed successfully for {target}")
            return results
            
        except Exception as e:
            logger.error(f"Error during scan: {str(e)}")
            return {'error': str(e)}
    
    def vulnerability_scan(self, target, ports='common'):
        """
        Run vulnerability scan using NSE scripts
        
        Args:
            target: Target IP or hostname
            ports: Port specification
            
        Returns:
            dict: Vulnerability scan results
        """
        logger.info(f"Starting vulnerability scan on {target}")
        
        # Use vulnerability detection scripts
        arguments = '--script vuln'
        
        return self.scan_ports(target, ports, arguments)
    
    def save_results(self, results, filename):
        """
        Save scan results to file
        
        Args:
            results: Scan results dictionary
            filename: Output filename
        """
        try:
            with open(filename, 'w') as f:
                json.dump(results, f, indent=2)
            success(logger, f"Results saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving results: {str(e)}")


def main():
    """Test function"""
    scanner = NmapScanner()
    results = scanner.scan_ports('127.0.0.1', ports='80,443,8080', arguments='-sV')
    print(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()
