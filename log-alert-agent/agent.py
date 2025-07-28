import time
from log_sources.file_source import FileLogSource
from alerts.filter import classify_alerts
from export.exporter import write_csv, write_json

def run_agent(log_path, poll_interval=1.0, stream_mode=False, export_format=None, export_file=None):
    print(f"[✓] Starting log alert agent (reading: {log_path})...\n")
    source = FileLogSource(log_path)

    severity_counts = {"High": 0, "Medium": 0, "Low": 0}

    export_data = {
        "high": [],
        "medium": [],
        "low": []
    }

    def handle_line(line):
        results = classify_alerts([line])
        for result in results:
            level = result['severity']
            message = result['message']

            parts = line.split()
            timestamp = " ".join(parts[:2]) if len(parts) >= 2 else "unknown"
            result["timestamp"] = timestamp

            if level in ("High", "Medium"):
                print(f"[!] ALERT: {level} — {message}")
            else:
                print(f"    {level} — {message}")  # No prefix, visually de-emphasized

            severity_counts[level] += 1
            export_data[level.lower()].append(result)

    # Step 1: Process full file first
    for line in source.read_lines():
        handle_line(line)

    # Step 2: Stream new logs if enabled
    if stream_mode:
        print("\n[~] Streaming new logs...\n")
        try:
            for line in source.follow(poll_interval=poll_interval):
                handle_line(line)
        except KeyboardInterrupt:
            print("\n Streaming stopped by user.")

    if export_format:
        print(f"\n Exporting results to {export_file}...")

        if export_format == "json":
            write_json(export_data, export_file)
        elif export_format == "csv":
            write_csv(export_data, export_file)

    print("[✓] Export complete.")

    # Step 3: Final summary
    print("\n🔎 Summary of alerts:")
    print(f"  High   → {severity_counts['High']}")
    print(f"  Medium → {severity_counts['Medium']}")
    print(f"  Low    → {severity_counts['Low']}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Log Alert Agent")
    parser.add_argument("logfile", help="Path to log file")
    parser.add_argument("--stream", action="store_true", help="Enable real-time tailing (like tail -f)")
    parser.add_argument("--interval", type=float, default=1.0, help="Polling interval in seconds (for streaming)")
    parser.add_argument("--export-format", help="Export format: csv or json")
    parser.add_argument("--export-file", help="Optional output filename")
    args = parser.parse_args()

    if not args.export_format:
        print("Select an output format:")
        print("  1. CSV (.csv)")
        print("  2. JSON (.json)")
        choice = input("Enter format [1–2]: ").strip()
        format_map = {"1": "csv", "2": "json"}
        args.export_format = format_map.get(choice)

if not args.export_file:
    args.export_file = f"alerts.{args.export_format}"

    run_agent(args.logfile, poll_interval=args.interval, stream_mode=args.stream, export_format=args.export_format, export_file=args.export_file)
