# Really basic link crawler
This is a really simple link crawler for pages with sitemap.xml available. 

## What is it good for
Have you ever come across a 404 link on some blog? Maybee want to verify that all links on your blog is active and working? Well, then this is one way to go look for broken links.

## How to use it
1. Clone or download and unzip to your location of choice
2. Navigate to the folder and run `pip install -r requirements.txt`
3. Run `python3 hyperlink_crawler.py https://www.example.com/sitemap.xml` but with a correct link to the sitemap.xml file you want to crawl

## What it does
1. The file reads sitemap.xml and collect all `<loc>` elements and the link inside. 
2. Then it reads that file content, try to find all `<a href="">` tags and fetch the URL inside. 
3. After this, it will verify that it is a valid URL and make a HEAD-request for that URL. At the same time, it will also save that URL in memory to make sure that unique URLs don't get multiple requests.
4. It will then get the HTTP status code from that request and save those with a 3xx, 4xx or 5xx responses for displaying and log output later.