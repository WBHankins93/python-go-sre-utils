import time
from typing import Iterator
from .base import LogSource

class FileLogSource(LogSource):
    def __init__(self, file_path: str, delay: float = 0.0):
        """
        file_path: Path to the log file to read
        delay: Optional delay (in seconds) between yielding lines (simulates real-time streaming)
        """
        self.file_path = file_path
        self.delay = delay

    def read_lines(self) -> Iterator[str]:
        with open(self.file_path, "r") as f:
            for line in f:
                yield line.strip()
                if self.delay > 0:
                    time.sleep(self.delay)
