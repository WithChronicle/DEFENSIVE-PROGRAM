from abc import ABC, abstractmethod

class KelolaStok(ABC):
    @abstractmethod
    def kurangiStok(self, jml):
        pass

    @abstractmethod
    def tambahStok(self, jml):
        pass
