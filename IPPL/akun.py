from abc import ABC

class Akun(ABC):
    def __init__(self, idAkun, nama, noTelp):
        self.idAkun = idAkun
        self.nama = nama
        self.noTelp = noTelp

    def login(self):
        return True