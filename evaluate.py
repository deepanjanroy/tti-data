import csv
import sys

evaluation_fieldnames = ["sitename", "reasonable_start", "reasonable_end", "metric_value", "verdict", "distance"]
epsilon = 0.1  # For dealing with floating point errors
grace = 0  # Just to see if stretching the boundaries a little fixes things

def get_green_ranges(truthcsv):
    green_ranges = {}
    with open(truthcsv) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Site"] and row["Too early end"] and row["Reasonable end"]:
                left_boundary = float(row["Too early end"])
                right_boundary = float(row["Reasonable end"])
                assert left_boundary < right_boundary
                green_ranges[row["Site"]] = (left_boundary, right_boundary)
    return green_ranges

def get_metric_values(resultscsv, target_metric):
    metric_values = {}
    with open(resultscsv) as f:
        reader = csv.DictReader(f, delimiter="|")
        if target_metric not in reader.fieldnames:
            raise Exception('{0} metric not found in data'.format(target_metric))
        for row in reader:
            metric_values[row["sitename"]] = float(row[target_metric])
    return metric_values

def get_site_to_metrics_map(resultscsv):
    metric_values = {}
    with open(resultscsv) as f:
        reader = csv.DictReader(f, delimiter="|")
        for row in reader:
            metric_values[row["sitename"]] = row
    return metric_values

def get_evaluations(metric_values, green_ranges):
    evaluations = []
    for site, value in metric_values.iteritems():
        green_range = green_ranges[site]
        if value < green_range[0] - epsilon - grace:
            verdict = "Too early"
        elif value > green_range[1] + epsilon + grace:
            verdict = "Too late"
        else:
            verdict = "Reasonable"
        evaluations.append({
            "sitename": site,
            "metric_value": value,
            "reasonable_start": green_range[0] - epsilon,
            "reasonable_end": green_range[1] + epsilon,
            "verdict": verdict,
            "distance": green_range[1] + epsilon - value
        })
    return evaluations

def produce_evaluation_csv(evaluations, verdictscsv):
    # Sort so that it's in the same order as firstInteractive scorecard
    if len(evaluations) == 0:
        return

    evaluations = sorted(evaluations, key=lambda x: x["sitename"].lower())

    with open(verdictscsv, "w") as f:
        writer = csv.DictWriter(f, evaluation_fieldnames);
        writer.writeheader()
        for row in evaluations:
            writer.writerow(row)

def test_all_combinations(testoutputcsv, resultscsv, green_ranges):
    site_to_metrics = get_site_to_metrics_map(resultscsv)
    with open (testoutputcsv, 'w') as f:
        writer = csv.DictWriter(f,
                ['windowSize',
                 'eqtThreshold',
                 'reasonable',
                 'too early',
                 'too late',
                 'distance'])
        writer.writeheader()
        # Low values for testing rn
        for windowSize in xrange(50, 5001, 50):
            for eqtThreshold in xrange(1, 26):
                metric_name = 'firstInteractiveNetRevHighEQTWindow-ws-{windowSize}-et-{eqtThreshold}'.format(
                    windowSize=windowSize, eqtThreshold=eqtThreshold)
                metrics = {site: float(all_metrics[metric_name]) for site, all_metrics in site_to_metrics.iteritems()}
                evaluations = get_evaluations(metrics, green_ranges)
                writer.writerow({
                    'windowSize': windowSize,
                    'eqtThreshold': eqtThreshold,
                    'reasonable': sum(1 for e in evaluations if e["verdict"] == "Reasonable"),
                    'too early': sum(1 for e in evaluations if e["verdict"] == "Too early"),
                    'too late': sum(1 for e in evaluations if e["verdict"] == "Too late"),
                    'distance': sum(e["distance"] for e in evaluations)
                })


def main():
    green_ranges = get_green_ranges("truth.csv")
    if len(sys.argv) < 2:
        print "Error: You need to specify the target metric"
        print "Usage: python evaluate.py target_metric"
        return

    target_metric = sys.argv[1]
    if target_metric == "all-rev-eqt":
        test_all_combinations("test_output.csv", "results.csv", green_ranges)
        return 0

    metric_values = get_metric_values("results.csv", target_metric)
    evaluations = get_evaluations(metric_values, green_ranges)
    produce_evaluation_csv(evaluations, "verdicts.csv")
    print "Num Reasonable: {0}".format(sum(1 for e in evaluations if e["verdict"] == "Reasonable"))
    print "Num Too early: {0}".format(sum(1 for e in evaluations if e["verdict"] == "Too early"))
    print "Num Too late: {0}".format(sum(1 for e in evaluations if e["verdict"] == "Too late"))
    print "Total distance saved: {0}".format(sum(e['distance'] for e in evaluations))


if __name__ == "__main__":
    main()
