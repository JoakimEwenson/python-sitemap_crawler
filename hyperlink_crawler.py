from os import EX_CANTCREAT
from bs4 import BeautifulSoup
from sitemap_crawler import fetch_sitemap
import requests
import sys
import time
import validators

""" Set up a url object """


class UrlObject:
    origin: str
    url: str
    status: int

    def __init__(self, origin, url, status):
        self.origin = origin
        self.url = url
        self.status = status


# Set up user agent
headers = {
    'User-Agent': '404 crawler by Joakim Ewenson'
}

# Initiate empty counter
url_ok = 0
url_broken = []
url_redirect = []
url_server_err = []
url_unknown_err = []

""" Validate URL response status """


def check_url(origin: str, url: str):
    if validators.url(url):
        global url_ok, url_broken, url_redirect
        try:
            # TODO: Check list of already verified URLs first, only call if not found
            response = requests.head(url, headers=headers)

            print(f'HTTP {response.status_code} for {url}')

            if response.status_code >= 200 and response.status_code <= 299:
                url_ok += 1

            if response.status_code >= 300 and response.status_code <= 399:
                url_redirect.append(
                    UrlObject(origin=origin, url=url, status=response.status_code))

            if response.status_code >= 400 and response.status_code <= 499:
                url_broken.append(
                    UrlObject(origin=origin, url=url, status=response.status_code))

            if response.status_code >= 500 and response.status_code <= 599:
                url_server_err.append(
                    UrlObject(origin=origin, url=url, status=response.status_code))
        except:
            url_unknown_err.append(UrlObject(origin=origin, url=url, status=999))


""" Fetch hyperlinks from page """


def fetch_hyperlinks(url: str):
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        for link in soup.find_all('a', href=True):
            check_url(url, link['href'])


""" Execute function if run as stand alone """
if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Please supply a URL as input string on the next attempt.')
        exit()
    if validators.url(sys.argv[1]):
        base_url = sys.argv[1]
        # Starting timer
        start_time = time.time()
        # Fetch sitemap
        # sitemap = fetch_sitemap(f'{base_url}/sitemap.xml')
        sitemap = fetch_sitemap(f'http://10.0.1.10/projekt/wpdemo/?tsf-sitemap=base')
        print(f'Sitemap contains {len(sitemap)} urls to crawl')
        # Fetching links
        #fetch_hyperlinks(sys.argv[1])
        for link in sitemap:
            fetch_hyperlinks(link.get_text())
        # Time well spent
        print(
            f'Total execution time is {int(time.time() - start_time)} seconds')
        print('Broken URLs:')
        for item in url_redirect:
            print(f'HTTP {item.status}: {item.url} with origin {item.origin}')
        for item in url_broken:
            print(f'HTTP {item.status}: {item.url} with origin {item.origin}')
        for item in url_server_err:
            print(f'HTTP {item.status}: {item.url} with origin {item.origin}')
