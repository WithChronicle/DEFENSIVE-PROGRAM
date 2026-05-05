class Transaksi:
    def __init__(self, noNota, pelanggan, motor, mekanik):
        self.noNota = noNota
        self.pelanggan = pelanggan
        self.motor = motor
        self.mekanik = mekanik
        self.totalBiaya = 0

    def hitungGrandTotal(self):
        return self.totalBiaya
