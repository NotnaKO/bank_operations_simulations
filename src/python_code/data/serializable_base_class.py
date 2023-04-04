from abc import ABC, abstractmethod


class SerializableByMyEncoder(ABC):
    @abstractmethod
    def get_data(self):
        pass
