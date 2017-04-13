import csv
import json
import sys

metric_names = [
    'firstInteractive-FMP',
    'firstInteractive-FMP-1s',
    'firstInteractive-FCP',
    'firstInteractive-FMP-ReverseSearch',
    'firstInteractive-FCP-ReverseSearch',
    'firstInteractive-FMP-Network',
    'firstInteractive-FMP-ReverseSearchFromNetworkFirstInteractive',
    'firstInteractiveForwardSlideInHighEQTWindow',
    'firstInteractiveNetRevLonelyTask',
    'firstInteractiveNetRevLonelyWindow',
    'firstInteractive-FMP-Proportional',
    'firstInteractive-MaxFmpDcl',
    'firstInteractive-Lighthouse',
    'firstInteractive-EventListeners',
    'firstInteractive-FMP-Proportional-w15-3000-lonely-ws-250-padding-1000psb-5000',
    'firstInteractive-FCP-Proportional-w15-3000-lonely-ws-250-padding-1000psb-5000',
    'firstInteractive-DCL-Proportional-w15-3000-lonely-ws-250-padding-1000psb-5000',
    'firstInteractive-FMP-ForwardLonely'
]

# metric_names += [
#     'firstInteractive-FMP-Proportional-w15-1250-lonely-ws-150-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1250-lonely-ws-150-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-1250-lonely-ws-200-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1250-lonely-ws-200-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-1250-lonely-ws-250-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1250-lonely-ws-250-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-1250-lonely-ws-150-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1250-lonely-ws-150-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-1250-lonely-ws-200-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1250-lonely-ws-200-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-1250-lonely-ws-250-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1250-lonely-ws-250-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-1500-lonely-ws-150-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1500-lonely-ws-150-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-1500-lonely-ws-200-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1500-lonely-ws-200-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-1500-lonely-ws-250-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1500-lonely-ws-250-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-1500-lonely-ws-150-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1500-lonely-ws-150-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-1500-lonely-ws-200-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1500-lonely-ws-200-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-1500-lonely-ws-250-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1500-lonely-ws-250-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-1750-lonely-ws-150-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1750-lonely-ws-150-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-1750-lonely-ws-200-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1750-lonely-ws-200-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-1750-lonely-ws-250-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1750-lonely-ws-250-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-1750-lonely-ws-150-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1750-lonely-ws-150-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-1750-lonely-ws-200-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1750-lonely-ws-200-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-1750-lonely-ws-250-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-1750-lonely-ws-250-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2000-lonely-ws-150-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2000-lonely-ws-150-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2000-lonely-ws-200-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2000-lonely-ws-200-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2000-lonely-ws-250-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2000-lonely-ws-250-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2000-lonely-ws-150-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2000-lonely-ws-150-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2000-lonely-ws-200-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2000-lonely-ws-200-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2000-lonely-ws-250-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2000-lonely-ws-250-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2250-lonely-ws-150-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2250-lonely-ws-150-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2250-lonely-ws-200-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2250-lonely-ws-200-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2250-lonely-ws-250-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2250-lonely-ws-250-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2250-lonely-ws-150-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2250-lonely-ws-150-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2250-lonely-ws-200-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2250-lonely-ws-200-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2250-lonely-ws-250-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2250-lonely-ws-250-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2500-lonely-ws-150-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2500-lonely-ws-150-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2500-lonely-ws-200-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2500-lonely-ws-200-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2500-lonely-ws-250-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2500-lonely-ws-250-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2500-lonely-ws-150-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2500-lonely-ws-150-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2500-lonely-ws-200-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2500-lonely-ws-200-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2500-lonely-ws-250-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2500-lonely-ws-250-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2750-lonely-ws-150-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2750-lonely-ws-150-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2750-lonely-ws-200-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2750-lonely-ws-200-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2750-lonely-ws-250-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2750-lonely-ws-250-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2750-lonely-ws-150-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2750-lonely-ws-150-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2750-lonely-ws-200-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2750-lonely-ws-200-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-2750-lonely-ws-250-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-2750-lonely-ws-250-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-3000-lonely-ws-150-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-3000-lonely-ws-150-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-3000-lonely-ws-200-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-3000-lonely-ws-200-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-3000-lonely-ws-250-padding-1000psb-0',
#     'firstInteractive-FMP-Proportional-w15-3000-lonely-ws-250-padding-1000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-3000-lonely-ws-150-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-3000-lonely-ws-150-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-3000-lonely-ws-200-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-3000-lonely-ws-200-padding-2000psb-5000',
#     'firstInteractive-FMP-Proportional-w15-3000-lonely-ws-250-padding-2000psb-0',
#     'firstInteractive-FMP-Proportional-w15-3000-lonely-ws-250-padding-2000psb-5000',
# ]

# print "Printing metrics names for test"
for window_size in xrange(1000, 5001, 1000):
    metric_name = 'firstInteractive-FMP-ws-' + str(window_size)
    metric_name_dcl = 'firstInteractive-FMP-ws-' + str(window_size) + '-DCL'
    metric_names.append(metric_name);
    metric_names.append(metric_name_dcl);

for w15 in xrange(1250, 3001, 250):
    metric_name = 'firstInteractive-FMP-Proportional-w15-' + str(w15)
    metric_names.append(metric_name);

# print "Done printing metric names"

# for window_size in xrange(350, 351, 50):
#     for eqt_threshold in xrange(8, 9):
#         metric_name = 'firstInteractiveNetRevHighEQTWindow-ws-{window_size}-et-{eqt_threshold}'.format(
#             window_size=window_size, eqt_threshold=eqt_threshold)
#         metric_names.append(metric_name)

reverse_search_metric_name = 'timeToFirstInteractive-FMP-based-ReverseSearch'

def load_results_from_file(filename):
    results = [];
    with open(filename) as f:
        for line in f:
            try:
                results.append(json.loads(line))
            except:
                print "Could not parse json: "
                print line
                print "######################"
    print "Loaded " + filename
    return results

def get_diagnostic_maps(bin):
    if len(bin) == 2:
        # This means we have a diagnostis map
        return bin[1]
    return []

def get_diagnostic_from_all_bins(histogram):
    all_diagnostics = []
    underflow_bin = histogram.get('underflow_bin', [])
    all_diagnostics.extend(get_diagnostic_maps(underflow_bin));
    for binIndex, bin in histogram.get('allBins', {}).items():
        all_diagnostics.extend(get_diagnostic_maps(bin))
    overflowBin = histogram.get('overflowBin', [])
    all_diagnostics.extend(get_diagnostic_maps(overflowBin));
    return all_diagnostics

def get_metric_histogram(ctp_result, metricName):
    histograms = ctp_result['pairs']['histograms']
    metric_histogram = [h for h in histograms if h.get('name', '') == metricName]
    if len(metric_histogram) == 0:
        return None
    if len(metric_histogram) > 1:
        raise Exception("The world is falling apart")
    return metric_histogram[0]

# The approach in this function looks fragile but I don't know a better way
def get_url(ctp_result):
    fcp_histogram = get_metric_histogram(ctp_result, 'timeToFirstContentfulPaint')
    diagnostics = get_diagnostic_from_all_bins(fcp_histogram)
    url = diagnostics[0]["url"]["value"]
    return url

# This function returns a string in the failure cases to make it more obvious in
# the csv what's going on.
def get_value(histogram):
    if histogram is None:
        return "Error: no histogram found"
    if 'running' in histogram:
        running_stats = histogram['running']
        running_max = running_stats[1]
        running_min = running_stats[4]
        if running_min == running_max:
            return running_min
        else:
            return "Error: Value not unique. Count: " + str(running_stats[0])
    return "Error: No value found"


# Returns a list of useful breakdown numbers
def get_breakdowns(result):
    histogram = get_metric_histogram(result, reverse_search_metric_name)
    diagnostics = get_diagnostic_from_all_bins(histogram)
    if len(diagnostics) == 0:
        return ["Error: No diagnostic found"]
    if len(diagnostics) != 1:
        print "Warning: Multiple diagnostics found: ", diagnostics
    return [json.dumps(diagnostics[-1]['Long task Breakdown of [forwardSearch, reverseSearch]']['value'])]

def get_url_to_sitename_map(map_file):
    with open(map_file) as f:
        r = csv.reader(f)
        url_to_sitename = {}
        for row in r:
            url_to_sitename[row[0].split(" ")[0].strip()] = row[1]
        return url_to_sitename


def main():
    if len(sys.argv) >= 2:
        ctp_result_filename = sys.argv[1]
    else:
        ctp_result_filename = "local_results.json"

    if len(sys.argv) >= 3:
        url_sitename_map_filename = sys.argv[2]
    else:
        url_sitename_map_filename = "tweakmap.csv"

    results = load_results_from_file(ctp_result_filename)
    url_to_sitename = get_url_to_sitename_map(url_sitename_map_filename)
    with open("results.csv", 'wb') as f:
        writer = csv.writer(f, delimiter='|')
        writer.writerow(['sitename', 'url'] + metric_names)
        rows = []
        for r in results:
            if len(r['failures']) != 0:
                print "Skipping result because of failures: ", r
                print "XXXXXXXXXXXXXXX"
                continue
            metrics = []
            for m in metric_names:
                h = get_metric_histogram(r, m)
                metrics.append(get_value(h))
            try:
                url = get_url(r)
            except:
                import IPython; IPython.embed()
                return 1
            rowData = [url_to_sitename[url], url] + metrics
            rows.append(rowData)

        rows = sorted(rows, key=lambda x: x[0].lower())
        for rowData in rows:
            writer.writerow(rowData)
    print "Total results processed:", len(results)


if __name__ == '__main__':
    main()

