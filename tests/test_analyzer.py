"""Smoke test for the project skeleton."""

from ddos.analyzer import TrafficAnalyzer


def test_analyzer_detects_suspicious_source():
    analyzer = TrafficAnalyzer(200, 60)
    traffic = [
        {"source_ip": "192.168.1.10", "requests": 120},
        {"source_ip": "192.168.1.10", "requests": 95},
        {"source_ip": "192.168.1.11", "requests": 50},
    ]

    result = analyzer.analyze(traffic)

    assert result["alert"] is True
    assert "192.168.1.10" in result["suspicious_sources"]
    assert analyzer.classify(250) == "high-risk"
