from __future__ import print_function, unicode_literals

from bs4 import BeautifulSoup
import urllib
import re

from redis import Redis
from rq import Queue

from parse_zappos_products import parse_product_page

class ZapposScraper():

    def __init__(self, url, output_dir):
        self.base_url = 'http://' + ''.join(url.split('/')[1:-1])
        self.url = url
        self.output_dir = output_dir

    def parse(self):
        # Set up an RQ connection
        q = Queue(connection=Redis())

        urls = set([])
        r = urllib.urlopen(self.url).read()
        soup = BeautifulSoup(r)
        for cat_url in self._get_categories(soup, "Landing-Category"):
            print(cat_url)
            for page_url in self._get_pages(cat_url):
                print("    ", page_url)
                for product_url in self._get_product_urls(page_url):
                    print("        ", product_url)
                    # Add to the queue if new
                    if product_url not in urls:
                        job = q.enqueue(parse_product_page, 
                                        self.output_dir, 
                                        self.base_url, 
                                        product_url)

    def _get_categories(self, soup, class_name):
        """Given a soup parsing, find the sub-categories we want to
        parse (shoe types for example).

        soup: BeautifulSoup
            A BeautifulSoup object to look in
        class_name: str
            A class name to make a regular expression out of

        returns:
            URL of each category page
        """
        for link in soup.find_all("a", class_=re.compile(".*{}.*".format(class_name))):
            url = link.get('href')
            yield "{}{}".format(self.base_url, url)
    
    def _get_pages(self, url):
        """For each category, go through each page and create a list
        of product pages
        """
        #pattern = re.compile(".*pager\w2.*")
        page_url = url
        idx = 1
        while True:
            # Parse page
            r = urllib.urlopen(page_url).read()
            soup = BeautifulSoup(r)

            # Find next page link (if there isn't one, exit)
            next_page = soup.find('a', class_="btn secondary arrow pager {}".format(idx))
            if not next_page:
                break

            # Save the next page to both parse and return
            page_url = "{}{}".format(self.base_url, next_page.get('href'))
            yield page_url
            idx += 1


    def _get_product_urls(self, url):
        """Given a url to a category landing page,
        get the url for each product displayed

        url: str
            URL of first page of a category landing page

        return: urls
            Urls of each page to parse
        """
        urls = []
        r = urllib.urlopen(url).read()
        soup = BeautifulSoup(r)
        for product in soup.find_all('a', class_=re.compile(".*product-.*")):
            product_url = product.get('href')
            if product_url:
                urls.append(product_url)
        return urls
