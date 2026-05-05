from akun import Akun

class Mekanik(Akun):
    def __init__(self, idAkun, nama, noTelp, spesialisasi, jumlahServis):
        super().__init__(idAkun, nama, noTelp)
        self.spesialisasi = spesialisasi
        self.jumlahServis = jumlahServis

    def ubahStatusServis(self):
        print("Status servis diubah")
