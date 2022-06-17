from bs4 import BeautifulSoup
from shared import CrawlerResult, UrlObject, crawler_headers
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


def parse_htmlpage(url:str):
    """ Function for parsing a HTML page looking for a hrefs and return a list of URLs """
    response = requests.get(url, headers=crawler_headers, timeout=15)

    if response.status_code == 200:
        content = response.text
        soup = BeautifulSoup(content, 'html.parser')
        url_list = []
        for link in soup.find_all('a', href=True):
            url_list.append(link['href'])
        return url_list


def verify_hyperlinks(url_list: list, origin: str):
    """ Take a list of URLs and verify them, returning a CrawlerResult """
    output = []
    for url in url_list:
        # Validate URL
        if validators.url(url):
            # Initiate empty counter for OK
            url_ok = 0
            # Initiate empty arrays for results
            url_broken = []
            url_redirect = []
            url_server_err = []
            url_unknown_err = []
            # Initiate empty set for storing URLs already verified
            url_verified = set()
            # Check list of already verified URLs first, only call if not found
            if url not in url_verified:
                # Add url to set for later
                url_verified.add(url)
                try:
                    # Call for HEAD response with 15s timeout
                    response = requests.head(
                        url, headers=crawler_headers, timeout=15)

                    # Output HTTP response code and URL to console
                    print(f'HTTP {response.status_code} for {url}')

                    # Check status code and sort accordingly
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
            output.append(CrawlerResult(origin=origin,ok=url_ok, broken=url_broken, redirect=url_redirect, server_err=url_server_err, unknown=url_unknown_err))
        else:
            pass

    # Return CrawlerResult with content
    return output
