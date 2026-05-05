from akun import Akun

class Pelanggan(Akun):
    def __init__(self, idAkun, nama, noTelp, alamat):
        super().__init__(idAkun, nama, noTelp)
        self.alamat = alamat
