from __future__ import print_function, unicode_literals

import urllib
from bs4 import BeautifulSoup
import re
import os


def parse_product_page(base_dir, base_url, url):
    """
    A function to queue up to parse the product page and save the
    info somewhere
    """
    # Remove trailing slash if needed
    if base_dir[-1] == '/':
        base_dir = base_dir[:-1]

    page_url = "{}/{}".format(base_url, url)
    html = urllib.urlopen(page_url).read()
    soup = BeautifulSoup(html, 'lxml')


    product_dir = "{}/{}".format(base_dir, url)
    # If we already have that product, return.
    if os.path.exists(product_dir):
        return
    # Otherwise, create directory
    os.makedirs(product_dir)

    pattern = re.compile(".*PrImage.*")
    for img_tag in soup.find_all('a', class_=pattern):
        img_url = img_tag.get('href')
        id = img_tag.get('id')
        if not img_url:
            continue
        img_url = "{}{}".format(base_url, img_url)
        urllib.urlretrieve(img_url, "{}/{}.jpg".format(product_dir, id))

if __name__=="__main__":
    parse_product_page('/media/ben/HDD/zappos_images/', u'http://www.zappos.com', '/vans-sk8-hi-slim-bel-air-blue-true-white')