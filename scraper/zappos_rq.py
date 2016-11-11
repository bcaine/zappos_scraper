from __future__ import print_function, unicode_literals

import sys
import os
import argparse

from redis import Redis
from rq import Queue, Connection, Worker

from parse_zappos_products import parse_product_page


def start_worker():
    with Connection():
        w = Worker(['default'])
        w.work()


def enqueue_urls(url_file, output_directory):
    q = Queue(connection=Redis())
    with open(url_file, 'r') as f:
        for url in f.read().split("\n"):
            base_url = 'http://' + ''.join(url.split("/")[1:-1])
            product_url = url.split("/")[-1]
            job = q.enqueue(parse_product_page, output_directory, base_url, product_url)
            print(job)



if __name__ == "__main__":
    # parse_product_page("/homeben/Panda/scraper/test/", "http://www.zappos.com", "mark-nason-gillespie-cognac")

    parser = argparse.ArgumentParser("A parser for zappos")
    parser.add_argument('--mode', help="Mode of running (enqueue, worker)", required=True)
    parser.add_argument('-f', '--file', help="URL file", required=False)
    parser.add_argument('-o', '--output_dir', help="Base output directory", required=False)

    if len(sys.argv):
        args = parser.parse_args()
        if args.mode == "enqueue":
            enqueue_urls(args.file, args.output_dir)
        elif args.mode == "worker":
            start_worker()
    else:
        parser.print_help()
