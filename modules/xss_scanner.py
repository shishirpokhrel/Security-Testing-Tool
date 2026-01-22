"""
XSS Scanner Module
Cross-Site Scripting vulnerability scanner with multiple payload injection
"""
import requests
import re
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm
from utils.logger import setup_logger, success
import random

logger = setup_logger('XSSScanner')


class XSSScanner:
    """XSS vulnerability scanner"""
    
    def __init__(self, timeout=10, max_payloads=50):
        """
        Initialize XSS scanner
        
        Args:
            timeout: Request timeout in seconds
            max_payloads: Maximum number of payloads to test
        """
        self.timeout = timeout
        self.max_payloads = max_payloads
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0'
        ]
    
    def load_payloads(self, payload_file):
        """
        Load XSS payloads from file
        
        Args:
            payload_file: Path to payload file
            
        Returns:
            list: List of payloads
        """
        try:
            with open(payload_file, 'r', encoding='utf-8', errors='ignore') as f:
                payloads = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            
            # Limit payloads if too many
            if len(payloads) > self.max_payloads:
                payloads = random.sample(payloads, self.max_payloads)
            
            logger.info(f"Loaded {len(payloads)} XSS payloads")
            return payloads
        except FileNotFoundError:
            logger.error(f"Payload file not found: {payload_file}")
            return []
        except Exception as e:
            logger.error(f"Error loading payloads: {str(e)}")
            return []
    
    def extract_forms(self, url):
        """
        Extract all forms from a webpage
        
        Args:
            url: Target URL
            
        Returns:
            list: List of form dictionaries
        """
        try:
            response = self.session.get(url, timeout=self.timeout, verify=False)
            soup = BeautifulSoup(response.text, 'html.parser')
            forms = []
            
            for form in soup.find_all('form'):
                form_details = {
                    'action': form.get('action'),
                    'method': form.get('method', 'get').lower(),
                    'inputs': []
                }
                
                # Extract input fields
                for input_tag in form.find_all(['input', 'textarea', 'select']):
                    input_type = input_tag.get('type', 'text')
                    input_name = input_tag.get('name')
                    input_value = input_tag.get('value', '')
                    
                    if input_name:
                        form_details['inputs'].append({
                            'type': input_type,
                            'name': input_name,
                            'value': input_value
                        })
                
                forms.append(form_details)
            
            logger.info(f"Found {len(forms)} forms on {url}")
            return forms
            
        except Exception as e:
            logger.error(f"Error extracting forms: {str(e)}")
            return []
    
    def test_reflected_xss(self, url, payloads):
        """
        Test for reflected XSS vulnerabilities
        
        Args:
            url: Target URL
            payloads: List of XSS payloads
            
        Returns:
            dict: Test results
        """
        logger.info(f"Testing reflected XSS on {url}")
        
        results = {
            'url': url,
            'type': 'reflected_xss',
            'scan_time': datetime.now().isoformat(),
            'vulnerabilities': []
        }
        
        # Parse URL and extract parameters
        parsed_url = urlparse(url)
        params = parse_qs(parsed_url.query)
        
        if not params:
            logger.warning("No GET parameters found in URL")
            return results
        
        total_tests = len(params) * len(payloads)
        
        with tqdm(total=total_tests, desc="Reflected XSS") as pbar:
            for param_name in params.keys():
                for payload in payloads:
                    try:
                        # Inject payload into parameter
                        test_params = params.copy()
                        test_params[param_name] = [payload]
                        
                        # Rebuild URL with payload
                        test_url = urlunparse((
                            parsed_url.scheme,
                            parsed_url.netloc,
                            parsed_url.path,
                            parsed_url.params,
                            urlencode(test_params, doseq=True),
                            parsed_url.fragment
                        ))
                        
                        # Send request
                        headers = {'User-Agent': random.choice(self.user_agents)}
                        response = self.session.get(test_url, headers=headers, timeout=self.timeout, verify=False)
                        
                        # Check if payload is reflected in response
                        if payload in response.text:
                            # Check if it's in a potentially vulnerable context
                            if self._is_vulnerable_context(response.text, payload):
                                logger.warning(f"Possible XSS found in parameter '{param_name}'")
                                results['vulnerabilities'].append({
                                    'parameter': param_name,
                                    'payload': payload,
                                    'url': test_url,
                                    'evidence': self._extract_evidence(response.text, payload)
                                })
                        
                        pbar.update(1)
                        
                    except Exception as e:
                        logger.debug(f"Error testing payload: {str(e)}")
                        pbar.update(1)
                        continue
        
        if results['vulnerabilities']:
            success(logger, f"Found {len(results['vulnerabilities'])} potential XSS vulnerabilities")
        else:
            logger.info("No XSS vulnerabilities found")
        
        return results
    
    def test_form_xss(self, url, payloads, forms=None):
        """
        Test forms for XSS vulnerabilities
        
        Args:
            url: Target URL
            payloads: List of XSS payloads
            forms: Pre-extracted forms (optional)
            
        Returns:
            dict: Test results
        """
        logger.info(f"Testing form-based XSS on {url}")
        
        results = {
            'url': url,
            'type': 'form_xss',
            'scan_time': datetime.now().isoformat(),
            'vulnerabilities': []
        }
        
        # Extract forms if not provided
        if forms is None:
            forms = self.extract_forms(url)
        
        if not forms:
            logger.warning("No forms found on the page")
            return results
        
        for form_idx, form in enumerate(forms):
            logger.info(f"Testing form {form_idx + 1}/{len(forms)}")
            
            # Build form action URL
            action = form['action']
            if not action:
                action = url
            elif not action.startswith('http'):
                parsed_url = urlparse(url)
                if action.startswith('/'):
                    action = f"{parsed_url.scheme}://{parsed_url.netloc}{action}"
                else:
                    action = f"{url.rstrip('/')}/{action}"
            
            # Test each input field
            for input_field in form['inputs']:
                input_name = input_field['name']
                
                # Skip certain input types
                if input_field['type'] in ['submit', 'button', 'image', 'hidden']:
                    continue
                
                for payload in payloads[:20]:  # Limit payloads per form field
                    try:
                        # Build form data
                        form_data = {}
                        for inp in form['inputs']:
                            if inp['name'] == input_name:
                                form_data[inp['name']] = payload
                            else:
                                form_data[inp['name']] = inp['value']
                        
                        # Submit form
                        headers = {'User-Agent': random.choice(self.user_agents)}
                        if form['method'] == 'post':
                            response = self.session.post(action, data=form_data, headers=headers, 
                                                        timeout=self.timeout, verify=False)
                        else:
                            response = self.session.get(action, params=form_data, headers=headers, 
                                                       timeout=self.timeout, verify=False)
                        
                        # Check for payload in response
                        if payload in response.text:
                            if self._is_vulnerable_context(response.text, payload):
                                logger.warning(f"Possible XSS in form field '{input_name}'")
                                results['vulnerabilities'].append({
                                    'form_index': form_idx,
                                    'field': input_name,
                                    'payload': payload,
                                    'action': action,
                                    'method': form['method'],
                                    'evidence': self._extract_evidence(response.text, payload)
                                })
                        
                    except Exception as e:
                        logger.debug(f"Error testing form: {str(e)}")
                        continue
        
        if results['vulnerabilities']:
            success(logger, f"Found {len(results['vulnerabilities'])} potential form XSS vulnerabilities")
        else:
            logger.info("No form XSS vulnerabilities found")
        
        return results
    
    def scan_url(self, url, payload_file, test_forms=True):
        """
        Comprehensive XSS scan of a URL
        
        Args:
            url: Target URL
            payload_file: Path to XSS payload file
            test_forms: Whether to test forms
            
        Returns:
            dict: Combined scan results
        """
        logger.info(f"Starting comprehensive XSS scan on {url}")
        
        payloads = self.load_payloads(payload_file)
        if not payloads:
            logger.error("No payloads loaded, aborting scan")
            return None
        
        results = {
            'url': url,
            'scan_time': datetime.now().isoformat(),
            'reflected_xss': {},
            'form_xss': {},
            'total_vulnerabilities': 0
        }
        
        # Test reflected XSS
        if '?' in url:
            results['reflected_xss'] = self.test_reflected_xss(url, payloads)
            results['total_vulnerabilities'] += len(results['reflected_xss'].get('vulnerabilities', []))
        
        # Test form-based XSS
        if test_forms:
            results['form_xss'] = self.test_form_xss(url, payloads)
            results['total_vulnerabilities'] += len(results['form_xss'].get('vulnerabilities', []))
        
        success(logger, f"XSS scan completed. Found {results['total_vulnerabilities']} potential vulnerabilities")
        return results
    
    def _is_vulnerable_context(self, html, payload):
        """
        Check if payload appears in a vulnerable context
        
        Args:
            html: HTML response
            payload: Injected payload
            
        Returns:
            bool: True if potentially vulnerable
        """
        # Simple heuristic: check if payload is not properly encoded
        dangerous_patterns = [
            r'<script[^>]*>' + re.escape(payload),
            re.escape(payload) + r'</script>',
            r'onerror\s*=\s*["\']?' + re.escape(payload),
            r'onload\s*=\s*["\']?' + re.escape(payload),
            r'src\s*=\s*["\']?' + re.escape(payload)
        ]
        
        for pattern in dangerous_patterns:
            if re.search(pattern, html, re.IGNORECASE):
                return True
        
        # Check if payload contains script tags and they're not encoded
        if '<script' in payload.lower() and '&lt;script' not in html.lower():
            if payload in html:
                return True
        
        return False
    
    def _extract_evidence(self, html, payload, context_length=100):
        """
        Extract evidence of payload in HTML
        
        Args:
            html: HTML content
            payload: Injected payload
            context_length: Characters before/after to include
            
        Returns:
            str: Evidence snippet
        """
        try:
            idx = html.find(payload)
            if idx != -1:
                start = max(0, idx - context_length)
                end = min(len(html), idx + len(payload) + context_length)
                return html[start:end]
        except:
            pass
        return ""


def main():
    """Test function"""
    scanner = XSSScanner()
    # Example: scanner.scan_url('http://example.com?q=test', 'payloads/xss_payloads.txt')


if __name__ == '__main__':
    main()
