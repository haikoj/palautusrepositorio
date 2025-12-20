
class TekoalyParannettu:
    def __init__(self, muistin_koko):
        self._muisti = [None] * muistin_koko
        self._vapaa_muisti_indeksi = 0

    def aseta_siirto(self, siirto):
        if self._vapaa_muisti_indeksi == len(self._muisti):
            self.vapauta_muistia()

        self._muisti[self._vapaa_muisti_indeksi] = siirto
        self._vapaa_muisti_indeksi += 1

    def vapauta_muistia(self):
        for i in range(1, len(self._muisti)):
            self._muisti[i - 1] = self._muisti[i]
            self._vapaa_muisti_indeksi -= 1

    def anna_siirto(self):
        if self._vapaa_muisti_indeksi in [0, 1]:
            return "k"

        viimeisin_siirto = self._muisti[self._vapaa_muisti_indeksi - 1]

        k, p, s = 0, 0, 0

        for i in range(0, self._vapaa_muisti_indeksi - 1):
            if viimeisin_siirto == self._muisti[i]:
                seuraava = self._muisti[i + 1]

                if seuraava == "k":
                    k += 1
                elif seuraava == "p":
                    p += 1
                else:
                    s += 1

        if k > p or k > s:
            return "p"
        elif p > k or p > s:
            return "s"
        else:
            return "k"
