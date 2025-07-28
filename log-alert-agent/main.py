import argparse
from parser import parse_log_file
from alert_formatter import classify_alerts
from export import export_summary

def main():
    parser = argparse.ArgumentParser(description="Log Alert Agent")
    parser.add_argument("logfile", help="Path to log file (text, JSON, or NDJSON)")
    parser.add_argument("--format", choices=["md", "csv", "json"], default="md", help="Output format")
    parser.add_argument("--output", help="Output file path (optional)")
    args = parser.parse_args()

    log_entries = parse_log_file(args.logfile)
    classified = classify_alerts(log_entries)
    export_summary(classified, output_format=args.format, output_path=args.output)

if __name__ == "__main__":
    main()
