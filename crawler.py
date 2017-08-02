'''
A basic web crawler.
'''
import requests
import re
import logging
from urlparse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup, SoupStrainer
from fake_useragent import UserAgent

DEFAULT_TIMEOUT = 30
DEFAULT_UA = UserAgent().random
VALID_URL = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

LOG_REQUESTS = True
LOG_LEVEL = 'warn'


def validate_url(url):
    return VALID_URL.match(url)


class Spider(object):
    to_crawl = set()
    crawled = set()

    def __init__(self, seed, **options):
        self.seed = seed
        self.to_crawl = set([seed])
        self.crawled = set()
        # The spider is restricted to just one domain.
        # The domain of the seed.
        self.domain = urlparse(seed).netloc
        # Handle options.
        ua = UserAgent()
        # If a ua was not set use a random ua
        options.setdefault('user-agent', DEFAULT_UA)
        options.setdefault('verify_cert', True)
        options.setdefault('timeout', DEFAULT_TIMEOUT)
        options.setdefault('logging', True)
        options.setdefault('log_level', LOG_LEVEL)
        if options['logging']:
            level = options['log_level']
            if level == 'info':
                logging.basicConfig(level=logging.INFO)
            if level == 'warn':
                logging.basicConfig(level=logging.WARN)
            if level == 'debug':
                logging.basicConfig(level=logging.DEBUG)
        self.options = options

    def get_page(self, url):
        ''' Download a web page.
        If anything goes wrong with the download.
        get_page will return None
        '''
        headers = {'User-Agent': self.options.get('user-agent')}
        timeout = self.options.get('timeout')
        # Shuld we verify the ssl cert ?
        verify = self.options.get('verify_cert')

        if not validate_url(url):
            return

        try:
            response = requests.get(
                url,
                headers=headers,
                verify=verify,
                timeout=timeout)
            return response.text.encode('utf-8')
        except Exception:
            return None

    def extract_links(self, url):
        page = self.get_page(url)
        if not page:
            return None
        soup = BeautifulSoup(page, 'lxml')
        for a in soup.find_all('a', href=True):
            link = a['href'].rstrip('/')
            url = urlparse(link)
            domain = url.netloc

            if domain == self.domain and link not in self.crawled:
                self.to_crawl.add(link)

    def crawl(self):
        while self.to_crawl:
            link = self.to_crawl.pop()
            print link
            self.crawled.add(link)
            self.extract_links(link)


crawler = Spider('http://www.google.com')
crawler.crawl()
