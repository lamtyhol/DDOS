"""Configuration values for the DDoS project."""

from dataclasses import dataclass


@dataclass
class AppConfig:
    """Application settings."""

    threshold_requests_per_minute: int = 200
    alert_window_seconds: int = 60
    max_connection_count: int = 1000
    log_level: str = "INFO"


DEFAULT_CONFIG = AppConfig()
