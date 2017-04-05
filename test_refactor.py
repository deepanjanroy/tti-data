import csv
import evaluate as ev
import numpy as np

metric_names = [
    'firstInteractive-FMP',
    'firstInteractive-FCP',
    'firstInteractive-FMP-ReverseSearch',
    'firstInteractive-FCP-ReverseSearch',
    'firstInteractive-FMP-Network',
    'firstInteractive-FMP-ReverseSearchFromNetworkFirstInteractive',
    'firstInteractiveNetRevHighEQTWindow-ws-350-et-8'
]

new_metrics = ev.get_site_to_metrics_map("results_new.csv")
old_metrics = ev.get_site_to_metrics_map("results_old.csv")

counter = 0
for m in metric_names:
    for site, mets in new_metrics.iteritems():
        new_value = float(mets[m])
        old_value = float(old_metrics[site][m])
        assert new_value == old_value
        print "passed: {0} - {1} - {2}".format(counter, site, m)
        counter += 1

