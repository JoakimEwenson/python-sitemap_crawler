from bs4 import BeautifulSoup
import requests

# Initiate empty counter
url_ok = 0
url_broken = 0
url_redirect = 0

# Temporary set up URL to check
input_url = 'http://10.0.1.10/projekt/wpdemo/?tsf-sitemap=base'

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
    urlList = fetch_sitemap(input_url)
    print(
        f'Total number of urls in sitemap {len(urlList)}.')
