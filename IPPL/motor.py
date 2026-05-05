from abc import ABC, abstractmethod

class Motor(ABC):
    def __init__(self, platNomor, merk):
        self.platNomor = platNomor
        self.merk = merk

    @abstractmethod
    def cekPengecekan(self):
        pass
