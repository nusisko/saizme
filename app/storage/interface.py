from abc import ABC, abstractmethod

class StorageInterface(ABC):
    @abstractmethod
    def save(self, file_data, filename):
        """Saves a file and returns its public URL or identifier."""
        pass

    @abstractmethod
    def read(self, filename):
        """Reads a file and returns its raw data."""
        pass
