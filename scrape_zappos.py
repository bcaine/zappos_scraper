from __future__ import print_function, unicode_literals

import sys
import argparse
from scraper.zappos import ZapposScraper

def run_parser(url, output):
    scraper = ZapposScraper(url, output)
    scraper.parse()
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser("A parser for zappos")
    parser.add_argument('-o', '--output',
                        help="The output directory to place images in",
                        required=True)
    parser.add_argument('-u', '--url', help='URL to start with', required=True)

    if len(sys.argv):
        args = parser.parse_args()
        run_parser(args.url, args.output)
    else:
        parser.print_help()
