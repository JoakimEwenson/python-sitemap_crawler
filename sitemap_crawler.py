import sys
from bs4 import BeautifulSoup
import requests
import validators

# Initiate empty counter
url_ok = 0
url_broken = 0
url_redirect = 0

""" Function for checking url and returning response """


def check_url(url):
    global url_ok, url_broken, url_redirect
    url_status = requests.head(url)

    if url_status.status_code == 200:
        url_ok += 1
    if url_status.status_code == 301 or url_status.status_code == 302:
        url_redirect += 1
    if url_status.status_code == 404:
        url_broken += 1

    print(f'{url_status.status_code}: {url}')

# Fetch sitemap.xml and parse it with BS4


def fetch_sitemap(url):
    req = requests.get(url)
    sitemap = req.text
    soup = BeautifulSoup(sitemap, features='xml')

    # Find all loc tags
    return soup.findAll('loc')


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Please supply a URL as input string on the next attempt.')
        exit()
    if validators.url(sys.argv[1]):
        base_url = sys.argv[1]
        urlList = fetch_sitemap(base_url)
        print(
            f'Total number of urls in sitemap {len(urlList)}.')
