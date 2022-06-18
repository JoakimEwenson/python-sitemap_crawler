from bs4 import BeautifulSoup
from shared import CrawlerResult, UrlObject, crawler_headers
import concurrent.futures
import requests
import validators


def parse_sitemap(content: BeautifulSoup):
    """ Function for parsing sitemap index and return list of URLs """
    # TODO: Add magic
    url_list = []
    for loc in content.findAll('loc'):
        if validators.url(loc.get_text()):
            url_list.append(loc.get_text())

    return url_list


def parse_htmlpage(url: str):
    """ Function for parsing a HTML page looking for a hrefs and return a list of URLs """
    response = requests.get(url, headers=crawler_headers, timeout=15)

    if response.status_code == 200:
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        url_list = []
        for link in soup.find_all('a', href=True):
            url_list.append(link['href'])
        return url_list


def check_url(url: str):
    """ Make a HEAD request for url and check response status """
    # Initiate empty counter for OK
    url_ok = False
    # Initiate empty arrays for results
    url_broken = []
    url_redirect = []
    url_server_err = []
    url_unknown_err = []
    # Try HEAD request for URL to get status code
    try:
        # Call for HEAD response with 15s timeout
        response = requests.head(
            url, headers=crawler_headers, timeout=10)

        # Output HTTP response code and URL to console
        print(f'HTTP {response.status_code} for {url}')

        # Check status code and sort accordingly
        if response.status_code >= 200 and response.status_code <= 299:
            url_ok = True

        if response.status_code >= 300 and response.status_code <= 399:
            url_redirect.append(
                UrlObject(origin=None, url=url, status=response.status_code))

        if response.status_code >= 400 and response.status_code <= 499:
            url_broken.append(
                UrlObject(origin=None, url=url, status=response.status_code))

        if response.status_code >= 500 and response.status_code <= 599:
            url_server_err.append(
                UrlObject(origin=None, url=url, status=response.status_code))
    except:
        url_unknown_err.append(
            UrlObject(origin=None, url=url, status=999))
    
    return CrawlerResult(origin=None, ok=url_ok, broken=url_broken, redirect=url_redirect, server_err=url_server_err, unknown=url_unknown_err)


def verify_hyperlinks(url_list: list, origin: str):
    """ Take a list of URLs and verify them, returning a CrawlerResult """
    # Initiate empty array for storing results
    output = []
    # Initiate empty set for storing URLs already verified
    url_verified = set()
    # Iterate url_list, verify and clean url and add to set
    for url in url_list:
        # Validate URL
        if validators.url(url):
            # Remove # from url
            url = url.rsplit('#')[0]
            # Remove & from url
            url = url.rsplit('&')[0]

            # Check list of already verified URLs first, only call if not found
            if url not in url_verified:
                # Add url to set for later
                url_verified.add(url)
        else:
            pass
    # Iterate verified urls and check them concurrently
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for result in executor.map(check_url, url_verified):
            output.append(result)
    # Return result
    return output
