#<!----- Imports ----->
#pip install requests
from ipaddress import ip_address
import requests
from requests.adapters import HTTPAdapter, Retry
#pip install pandas
#pip install lxml
import pandas as pd

#pip install beautifulsoup4
from bs4 import BeautifulSoup as bs
import random, time

#<!----- Default Declarations ----->
DEFAULT_TIMEOUT = 5 #seconds

#<!----- Classes ----->
class TimeoutHTTPAdapter(HTTPAdapter):
    #Courtesy of https://findwork.dev/blog/advanced-usage-python-requests-timeouts-retries-hooks/
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)

class req:
    def __init__(self,MIN_TIME_BET_REQ=1):
        self.MIN_TIME_BET_REQ = MIN_TIME_BET_REQ #seconds
        self.DEFAULT_TIMEOUT = DEFAULT_TIMEOUT  #seconds
        self.last_request = time.time()
        self.user_agents = [ 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36', 
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36', 
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36', 
        'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148', 
        'Mozilla/5.0 (Linux; Android 11; SM-G960U) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'
        ] 

        self.headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Referer': 'https://www.google.com/',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1'
        }
        self.proxy_ips = []

    def randomize_header(self):
        """Randomize request headers by updating both referer and useragent
        """
        self.change_useragent()
        self.change_referer()

    def change_useragent(self):
        """Change request useragent to random one
        """
        self.headers['User-Agent'] = random.choice(self.user_agents)

    def change_referer(self):
        """Randomly set google.com as referer
        """
        self.headers['Referer'] = random.choice(['','https://www.google.com/'])
    
    def get_from_list(self, url_list, randomize_header=False):
        """Complete requests to a list of urls and return the list of responses

        Args:
            url_list (list): List of url
            randomize_header (bool, optional): Randomize header between url calls. Defaults to False.

        Returns:
            list: List of request responses
        """
        duplicate_list = url_list[:]
        random.shuffle(duplicate_list)

        req = {}
        for url in duplicate_list:
            req[url] = self.get(url, randomize_header=randomize_header)
        
        return [req[x] for x in url_list]
    
    def get(self, url, randomize_header=False, timeout=None, retry = 5, custom_headers=None, proxy=None):
        """URL request with header randomization, timeout, proxy and retries builtin

        Args:
            url (str): URL to request
            randomize_header (bool, optional): Randomize useragent and referer. Defaults to False.
            timeout (float, optional): request timeout. Defaults to None.
            retry(bool, optional): Number of times to retry on failure, Defaults to 5
            custom_headers(dict, optional): Custom headers, Defaults to None
            proxy(bool, optional): Do no use; Use `proxy_get` if you want to use proxy

        Returns:
            request object: request object
        """
        if randomize_header:
            self.randomize_header()

        if custom_headers:
            headers = custom_headers
        else:
            headers = self.headers
        
        if not timeout:
            timeout = self.DEFAULT_TIMEOUT

        time_elapsed = time.time() - self.last_request
        time.sleep(max(0, self.min_time_bet_req - time_elapsed))
        for i in range(retry):
            try:
                res = requests.get(url, headers=headers, timeout=timeout, proxies=proxy)
                res.raise_for_status()
                break
            except:
                time.sleep(0.5 * (2 ** (i)))
        return res

    def _get_free_proxy_list(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-CA,en-US;q=0.7,en;q=0.3',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.pluralsight.com/',
            'Connection': 'keep-alive',
            # Requests sorts cookies= alphabetically
            # 'Cookie': 'MicrosoftApplicationsTelemetryDeviceId=f173324b-4222-1ba5-2e2e-5b88b09082e5; MicrosoftApplicationsTelemetryFirstLaunchTime=1606934918262',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'cross-site'
            # Requests doesn't support trailers
            # 'TE': 'trailers',
        }
        res = self.get("https://free-proxy-list.net/", False, None, 5, custom_headers=headers)
        df = pd.read_html(res.text)
        self.proxy_ips = [f"{ip}:{port}" for ip, port in zip((df[0]['IP Address']),(df[0]['Port']))]
        return self.proxy_ips

    def proxy_get_from_list(self, url_list):
        """Complete requests to a list of urls and return the list of responses using proxy ips

        Args:
            url_list (list): List of url
            randomize_header (bool, optional): Randomize header between url calls. Defaults to False.

        Returns:
            list: List of request responses
        """
        duplicate_list = url_list[:]
        random.shuffle(duplicate_list)

        req = {}
        for url in duplicate_list:
            req[url] = self.proxy_get(url)
        
        return [req[x] for x in url_list]

    def proxy_get(self, url):
        if self.proxy_ips == []:
            self._get_free_proxy_list()
        while True:
            try:
                if self.proxy_ips == []:
                    print("All proxies exhausted.")
                    break
                proxy = random.randint(0, len(self.proxy_ips) - 1)
                proxies = {"http": self.proxy_ips(proxy), "https": self.proxy_ips(proxy)}
                self.proxy_ips.remove(self.proxy_ips(proxy))

                print(f"Proxy currently being used: {proxies['https']}", end='')
                response = self.get(url, randomize_header=True, timeout=self.DEFAULT_TIMEOUT, retry=2, proxy=proxies)
                print('Success.')
                break
            except:
                print(" - Error, looking for another proxy")
        return response
    
    def create_session(self, retry=5):
        """Generate sessions object with adequate headers and adapters

        Args:
            retry (int, optional): Number of times to retry on failed request. Defaults to 5.

        Returns:
            sessions obj: sessions object
        """
        s = requests.Session()
        s.headers = self.headers
        retries = Retry(total=retry,
                        backoff_factor=0.5,
                        status_forcelist=[429, 500, 502, 503, 504],
                        method_whitelist=["HEAD", "GET", "OPTIONS"]
                        )
        s.mount('http://', TimeoutHTTPAdapter(max_retries=retries))
        s.mount('https://', TimeoutHTTPAdapter(max_retries=retries))
        self.session = s
        return s

class soup_class:
    #<!----- Functions ----->
    def get_soup(text):
        return bs(text, "html.parser")