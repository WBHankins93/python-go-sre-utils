import json
import csv
from tabulate import tabulate

def write_csv(data, output_file):
    """Flatten grouped alerts and write to CSV."""
    flat_data = flatten_alerts(data)
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=flat_data[0].keys())
        writer.writeheader()
        writer.writerows(flat_data)

def write_json(data, output_file):
    """Write alerts grouped by severity to JSON."""
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

def flatten_alerts(data):
    """Flatten grouped alert dict into a single list of alerts."""
    flat = []
    for level, entries in data.items():
        for entry in entries:
            flat.append(entry)
    return flat