import time
from log_sources.file_source import FileLogSource
from alerts.filter import classify_alerts

def run_agent(log_path, poll_interval=1.0, stream_mode=False):
    print(f"[✓] Starting log alert agent (reading: {log_path})...\n")
    source = FileLogSource(log_path)

    severity_counts = {"High": 0, "Medium": 0, "Low": 0}

    def handle_line(line):
        results = classify_alerts([line])
        for result in results:
            level = result['severity']
            message = result['message']

            if level in ("High", "Medium"):
                print(f"[!] ALERT: {level} — {message}")
            else:
                print(f"    {level} — {message}")  # No prefix, visually de-emphasized

            severity_counts[level] += 1

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
            print("\n[✋] Streaming stopped by user.")

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
    args = parser.parse_args()

    run_agent(args.logfile, poll_interval=args.interval, stream_mode=args.stream)
