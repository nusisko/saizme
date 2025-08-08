from abc import ABC, abstractmethod
from typing import IO, Optional

class StorageInterface(ABC):
    """An interface defining the contract for all storage adapters."""
    @abstractmethod
    def save(self, file_stream: IO[bytes], filename: str, content_type: str) -> str:
        """Uploads a file and returns its public URL."""
        pass

    @abstractmethod
    def read(self, object_name: str) -> Optional[bytes]:
        """Reads a file's content into bytes or returns None if not found."""
        pass