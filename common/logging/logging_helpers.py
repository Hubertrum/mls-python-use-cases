import time
from datetime import datetime


def log_message(
    message: str, timestamp: float | None = None, level: str = "INFO"
) -> None:

    if timestamp is None:
        timestamp = time.time()

    formatted_ts = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

    print(f"[{formatted_ts}] [{level}] {message}")
