import sys
from bs4 import BeautifulSoup
import requests
import validators


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print('Please supply a URL as input string on the next attempt.')
        exit()
    if validators.url(sys.argv[1]):
        base_url = sys.argv[1]

        req = requests.get(base_url)
        sitemap = req.text
        soup = BeautifulSoup(sitemap, features='xml')

        if (soup.find('sitemapindex')):
            print('Found sitemap index!')
            # TODO: Add some magic
        if (soup.find('urlset')):
            print('Found url set!')
            # TODO: Add some magic
        