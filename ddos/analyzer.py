"""Core logic for traffic analysis and anomaly detection."""

from collections import defaultdict
from typing import Dict, List


class TrafficAnalyzer:
    """Analyze request patterns and flag suspicious behavior."""

    def __init__(self, threshold_requests_per_minute: int, alert_window_seconds: int):
        self.threshold_requests_per_minute = threshold_requests_per_minute
        self.alert_window_seconds = alert_window_seconds

    def analyze(self, traffic: List[Dict[str, float]]) -> Dict[str, object]:
        """Return a summary for a batch of requests.

        Each item in `traffic` can contain:
        - `timestamp`: numeric time value
        - `source_ip`: identifier of requester
        - `requests`: number of requests in the time window
        """
        if not traffic:
            return {"total_requests": 0, "suspicious_sources": [], "alert": False}

        counts_by_source = defaultdict(int)
        for item in traffic:
            counts_by_source[str(item.get("source_ip", "unknown"))] += int(item.get("requests", 0))

        suspicious_sources = [
            source for source, count in counts_by_source.items()
            if count >= self.threshold_requests_per_minute
        ]

        summary = {
            "total_requests": sum(item.get("requests", 0) for item in traffic),
            "suspicious_sources": suspicious_sources,
            "alert": bool(suspicious_sources),
        }
        return summary

    def classify(self, request_rate: int) -> str:
        """Classify traffic behavior based on request rate."""
        if request_rate >= self.threshold_requests_per_minute:
            return "high-risk"
        if request_rate >= self.threshold_requests_per_minute // 2:
            return "warning"
        return "normal"
