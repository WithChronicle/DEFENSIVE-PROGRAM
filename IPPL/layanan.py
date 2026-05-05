from abc import ABC, abstractmethod

class Layanan(ABC):
    @abstractmethod
    def hitungBiaya(self):
        pass
