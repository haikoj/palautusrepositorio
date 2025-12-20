
class Tuomari:
    def __init__(self):
        self.ekan_pisteet = 0
        self.tokan_pisteet = 0
        self.tasapelit = 0

    def kirjaa_siirto(self, ekan_siirto, tokan_siirto):
        if self._tasapeli(ekan_siirto, tokan_siirto):
            self.tasapelit = self.tasapelit + 1
        elif self._eka_voittaa(ekan_siirto, tokan_siirto):
            self.ekan_pisteet = self.ekan_pisteet + 1
        else:
            self.tokan_pisteet = self.tokan_pisteet + 1

    def peli_ohi(self, max_pisteet=5):
        return self.ekan_pisteet >= max_pisteet or self.tokan_pisteet >= max_pisteet

    def __str__(self):
        return f"Pelitilanne: {self.ekan_pisteet} - {self.tokan_pisteet}\nTasapelit: {self.tasapelit}"

    def _tasapeli(self, eka, toka):
        if eka == toka:
            return True

        return False

    def _eka_voittaa(self, eka, toka):
        if eka == "k" and toka == "s":
            return True
        elif eka == "s" and toka == "p":
            return True
        elif eka == "p" and toka == "k":
            return True

        return False
