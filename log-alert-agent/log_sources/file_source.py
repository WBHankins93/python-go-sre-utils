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

    def follow(self, poll_interval: float = 1.0) -> Iterator[str]:
        """
        Like tail -f: Yields new lines as they are written to the file.
        """
        with open(self.file_path, "r") as f:
            # Move to end of file
            f.seek(0, 2)
            while True:
                line = f.readline()
                if not line:
                    time.sleep(poll_interval)
                    continue
                yield line.strip()