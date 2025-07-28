from typing import List, Dict

ALERT_KEYWORDS = {
    "ERROR": "High",
    "CRITICAL": "High",
    "WARN": "Medium",
    "WARNING": "Medium",
    "INFO": "Low"
}

def classify_alerts(log_lines: List[str]) -> List[Dict]:
    alerts = []
    for line in log_lines:
        for keyword, severity in ALERT_KEYWORDS.items():
            if keyword in line:
                alerts.append({
                    "message": line,
                    "severity": severity,
                    "matched": keyword
                })
                break
    return alerts
