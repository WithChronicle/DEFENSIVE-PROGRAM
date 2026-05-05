from ikelola_stok import IKelolaStok

class Sparepart(IKelolaStok):
    def __init__(self, kodePart, namaPart, stok):
        self.kodePart = kodePart
        self.namaPart = namaPart
        self.stok = stok

    def kurangiStok(self, jml):
        if self.stok >= jml:
            self.stok -= jml
            return True
        return False

    def tambahStok(self, jml):
        self.stok += jml
