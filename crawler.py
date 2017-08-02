
'''
Scrape
'''

import requests
from urlparse import urlparse, urljoin, urldefrag
from bs4 import BeautifulSoup, SoupStrainer

class Spider(object):
    to_crawl = set()
    crawled = set()

    def __init__(self, seed):
        self.seed = seed
        self.to_crawl = set([seed])
        self.crawled = set()
        # The spider is restricted to just one domain.
        # The domain of the seed.
        self.domain = urlparse(seed).netloc

    def get_page(self, url):
        ''' Download a web page.
        If anything goes wrong with the download.
        get_page will return None
        '''
        try:
            return requests.get(url).text.encode('utf-8')
        except Exception as e:
            print e

    def extract_links(self, url):
        page = self.get_page(url)
        if not page:
            return None
        soup = BeautifulSoup(page, 'lxml')
        for a in soup.find_all('a', href=True):
            link = a['href'].rstrip('/')
            url = urlparse(link)
            domain = url.netloc
            the link has not been crawled.
            if domain == self.domain and link not in self.crawled:
                self.to_crawl.add(link)

    def crawl(self):
        while self.to_crawl:
            link = self.to_crawl.pop()
            self.crawled.add(link)
            self.extract_links(link)
            print link


crawler = Spider('http://www.google.com')
crawler.crawl()
