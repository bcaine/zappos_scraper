#! /bin/bash

for run in {1..64}
do
  python scraper/zappos_rq.py --mode worker &
done
