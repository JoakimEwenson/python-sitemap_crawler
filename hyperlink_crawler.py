from bs4 import BeautifulSoup
from sitemap_crawler import fetch_sitemap
import concurrent.futures
import requests
import sys
import time
import validators


class UrlObject:
    """ Set up a url object """
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

# Initiate empty counter for total amount of links checked
url_total = 0
# Initiate empty counter for OK
url_ok = 0
# Initiate empty set for storing URLs
url_list = set()
# Initiate empty arrays for results
url_broken = []
url_redirect = []
url_server_err = []
url_unknown_err = []


def check_url(url: str):
    """ Validate URL response status """
    origin = 'https://example.com'
    if validators.url(url):
        global url_list, url_ok, url_broken, url_redirect, url_total
        # Check list of already verified URLs first, only call if not found
        # Remove # from url
        url = url.rsplit('#')[0]
        # Remove & from url
        url = url.rsplit('&')[0]
        if url not in url_list:
            # Add url to set for later
            url_total += 1
            url_list.add(url)
            try:
                # Call for HEAD response with 15s timeout
                response = requests.head(url, headers=headers, timeout=15)

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
                url_unknown_err.append(
                    UrlObject(origin=origin, url=url, status=999))


def fetch_hyperlinks(url: str):
    """ Fetch hyperlinks from page """
    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            content = response.text
            soup = BeautifulSoup(content, 'html.parser')
            # Working solution without threads
            # for link in soup.find_all('a', href=True):
            #     # check_url(url, link['href'])
                # check_url(link['href'])
            # Threaded solution
            url_list = []
            for link in soup.find_all('a', href=True):
                url_list.append(link['href'])
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(check_url, url_list)
    except:
        pass


if __name__ == '__main__':
    """ Execute function if run as stand alone """
    if len(sys.argv) == 1:
        print('Please supply a URL as input string on the next attempt.')
        exit()
    if validators.url(sys.argv[1]):
        base_url = sys.argv[1]
        # Starting timer
        start_time = time.time()
        # Fetch sitemap
        sitemap = fetch_sitemap(f'{base_url}')
        print(f'Sitemap contains {len(sitemap)} urls to crawl')
        # Fetching links
        for index, link in enumerate(sitemap):
            print(
                f'\nCrawling links in {link.get_text()} (link {index + 1}/{len(sitemap)})')
            fetch_hyperlinks(link.get_text())

        # Check if there are any values in the broken and server_err arrays
        if len(url_broken) > 0 or len(url_server_err) > 0:
            print('Broken URLs:')
            # for item in url_redirect:
            #     print(f'HTTP {item.status}: {item.url} with origin {item.origin}')
            if len(url_broken) > 0:
                print('\n4xx responses\n')
                for item in url_broken:
                    print(
                        f'HTTP {item.status}: {item.url} with origin {item.origin}')
            if len(url_server_err) > 0:
                print('\n5xx responses\n')
                for item in url_server_err:
                    print(
                        f'HTTP {item.status}: {item.url} with origin {item.origin}')

        # Print to log file
        with open(f'url_test_{int(time.time())}.log', 'w') as file:
            file.write('Broken URLs:\n')
            if len(url_redirect) > 0:
                file.write('\n3xx responses\n')
                for item in url_redirect:
                    file.write(
                        f'HTTP {item.status}: {item.url} with origin {item.origin}\n')
            if len(url_broken) > 0:
                file.write('\n4xx responses\n')
                for item in url_broken:
                    file.write(
                        f'HTTP {item.status}: {item.url} with origin {item.origin}\n')
            if len(url_server_err) > 0:
                file.write('\n5xx responses:\n')
                for item in url_server_err:
                    file.write(
                        f'HTTP {item.status}: {item.url} with origin {item.origin}\n')
            # Time well spent
            file.write(
                f'\nTotal execution time was {int(time.time() - start_time)} seconds')
        # Time well spent
        print(
            f'\nTotal execution time was {int(time.time() - start_time)} seconds and a total of {url_total} links where checked.')
