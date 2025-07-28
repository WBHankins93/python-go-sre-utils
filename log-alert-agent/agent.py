import time
from log_sources.file_source import FileLogSource
from alerts.filter import classify_alerts

def run_agent(log_path, poll_interval=1.0, from_start=False):
    print(f"[✓] Starting log alert agent (watching: {log_path})...\n")
    source = FileLogSource(log_path)

    if from_start:
        for line in source.read_lines():
            results = classify_alerts([line])
            for result in results:
                print(f"[!] ALERT: {result['severity']} — {result['message']}")

    for line in source.follow(poll_interval=poll_interval):
        results = classify_alerts([line])
        for result in results:
            print(f"[!] ALERT: {result['severity']} — {result['message']}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Real-time Log Alert Agent")
    parser.add_argument("logfile", help="Path to log file")
    parser.add_argument("--from-start", action="store_true", help="Read existing lines first, then follow new ones")
    parser.add_argument("--interval", type=float, default=1.0, help="Polling interval in seconds")
    args = parser.parse_args()

    run_agent(args.logfile, poll_interval=args.interval, from_start=args.from_start)

