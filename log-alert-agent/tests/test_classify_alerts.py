from alerts.filter import classify_alerts

def test_info_log_is_low():
    logs = ["2025-07-28 08:01:12 INFO Service started"]
    results = classify_alerts(logs)
    assert len(results) == 1
    assert results[0]["severity"] == "Low"
    assert results[0]["matched"] == "INFO"

def test_warn_log_is_medium():
    logs = ["2025-07-28 08:01:14 WARN Disk almost full"]
    results = classify_alerts(logs)
    assert results[0]["severity"] == "Medium"
    assert results[0]["matched"] == "WARN"

def test_critical_log_is_high():
    logs = ["2025-07-28 08:01:15 CRITICAL Kernel panic"]
    results = classify_alerts(logs)
    assert results[0]["severity"] == "High"
    assert results[0]["matched"] == "CRITICAL"

def test_debug_log_is_ignored():
    logs = ["2025-07-28 08:01:16 DEBUG Connection check"]
    results = classify_alerts(logs)
    assert results == []

def test_empty_input():
    assert classify_alerts([]) == []

def test_multiple_logs():
    logs = [
        "INFO Everything is good",
        "ERROR Database crashed",
        "WARNING CPU usage high"
    ]
    results = classify_alerts(logs)
    assert len(results) == 3
    assert results[0]["severity"] == "Low"
    assert results[1]["severity"] == "High"
    assert results[2]["severity"] == "Medium"