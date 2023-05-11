from abc import ABC, abstractmethod


class SerializableByMyEncoder(ABC):
    """Pure abstract class which provides interface to encoding"""

    @abstractmethod
    def get_data(self):
        """Return a data to json encoder"""
