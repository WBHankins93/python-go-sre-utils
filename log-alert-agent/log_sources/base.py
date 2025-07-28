from abc import ABC, abstractmethod
from typing import Iterator

class LogSource(ABC):
    @abstractmethod
    def read_lines(self) -> Iterator[str]:
        """Yield log lines one at a time"""
        pass
