import time
from log_sources.file_source import FileLogSource
from alerts.filter import apply_alert_filters

def run_agent(log_path, poll_interval=1.0):
    print(f"[✓] Starting log alert agent (watching: {log_path})...\n")
    source = FileLogSource(log_path)

    for line in source.follow(poll_interval=poll_interval):
        result = apply_alert_filters(line)
        if result:
            print(f"[!] ALERT: {result['level']} — {result['message']}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Real-time Log Alert Agent")
    parser.add_argument("logfile", help="Path to log file")
    parser.add_argument("--interval", type=float, default=1.0, help="Polling interval in seconds")
    args = parser.parse_args()

    run_agent(args.logfile, poll_interval=args.interval)
