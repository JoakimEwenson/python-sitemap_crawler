import time
from bs4 import BeautifulSoup
from shared import crawler_headers
import sys
import requests
import validators

from parsers import parse_htmlpage, parse_sitemap, verify_hyperlinks


if __name__ == '__main__':
    if len(sys.argv) == 1:
        base_url = input('Please supply a URL: ')

    # if validators.url(sys.argv[1]):
    #     base_url = sys.argv[1]

    if validators.url(base_url):
        start_time = time.time()
        # Fetch content of base_url
        try:
            req = requests.get(base_url, headers=crawler_headers, timeout=15)
            sitemap = req.text
        except:
            print('Error parsing url')
        # Parse content into soup
        try:
            soup = BeautifulSoup(sitemap, features='xml')
            # Check if parsed content is sitemapindex or urlset
            if (soup.find('sitemapindex')):
                print('\nParsing sitemap index...')
                # TODO: Add some magic
                sitemap_list = parse_sitemap(soup)
                for sitemap in sitemap_list:
                    if validators.url(sitemap):
                        print(f'\nParsing {sitemap}:')
                        try:
                            sitemap_req = requests.get(sitemap, headers=crawler_headers, timeout=15)
                            sitemap_content = sitemap_req.text
                            sitemap_soup = BeautifulSoup(
                                sitemap_content, features='xml')
                        except:
                            print(f'Could not fetch {sitemap}')
                        try:
                            url_list = parse_sitemap(sitemap_soup)
                            # print(f'{sitemap} length {len(url_list)}')
                            crawl_result = verify_hyperlinks(
                                url_list=url_list, origin=sitemap)
                            print('Done')
                        except:
                            print(f'Could not parse {sitemap}')
            if (soup.find('urlset')):
                print(f'\nParsing URL set from {base_url}...')
                # TODO: Add some magic
                url_list = parse_sitemap(soup)
                for url in url_list:
                    links = parse_htmlpage(url=url)
                    crawl_result = verify_hyperlinks(url_list=links, origin=base_url)
                print('Done')
                
        except:
            print('Error parsing content')

        # Time well spent
        print(f'Time spent executing: {int(time.time() - start_time)}s')