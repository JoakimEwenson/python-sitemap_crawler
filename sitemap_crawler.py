from tracemalloc import start
from bs4 import BeautifulSoup
import asyncio
import requests
import time

# Initiate empty counter
url_ok = 0
url_broken = 0
url_redirect = 0

# Temporary set up URL to check
# url = 'https://www.dryden.se/category-sitemap.xml'
url = 'http://10.0.1.10/projekt/wpdemo/?tsf-sitemap=base'

""" Function for checking url and returning response """


async def check_url(url):
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
req = requests.get(url)
sitemap = req.text
soup = BeautifulSoup(sitemap, features='xml')

# Find all loc tags
urlList = soup.findAll('loc')

# Iterate result and print urls
start_time = time.time()
for url in urlList:
    asyncio.run(check_url(url.get_text()))

print(
    f'Total number of urls checked {len(urlList)} in {int(time.time() - start_time)} seconds and {url_ok} responded with HTTP 200.')
print(f'Number of redirects: {url_redirect}')
print(f'Number of broken urls: {url_broken}')
