#!/bin/bash -x

set -e

metric_name="$1"

cp /tmp/local_results.json ctpdata.json
python json2csv-tweaked.py ctpdata.json
python evaluate.py $metric_name && column -s, -t < verdicts.csv
mv verdicts.csv data-${metric_name}.csv

