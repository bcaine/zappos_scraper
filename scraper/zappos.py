from __future__ import print_function, unicode_literals

from bs4 import BeautifulSoup
import urllib
import re

class ZapposScraper():

    def __init__(self, url, output_file):
        self.base_url = 'http://' + ''.join(url.split('/')[1:-1])
        self.url = url
        self.output_file = output_file

    def parse(self):
        r = urllib.urlopen(self.url).read()
        soup = BeautifulSoup(r)
        with open(self.output_file, 'w') as f:
            for cat_url in self._get_categories(soup, "Landing-Category"):
                for page_url in self._get_pages(cat_url):
                    for url in self._get_product_urls(page_url):
                        f.write(url + '\n')


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
        pattern = re.compile(".*secondary.*")
        page_url = url

        while True:
            # Parse page
            r = urllib.urlopen(page_url).read()
            soup = BeautifulSoup(r)

            # Find next page link (if there isn't one, exit)
            next_page = soup.find('a', class_=pattern)
            if not next_page:
                break

            # Save the next page to both parse and return
            page_url = "{}{}".format(self.base_url, next_page.get('href'))
            yield page_url


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
                urls.append("{}{}".format(self.base_url, product_url))
        return urls