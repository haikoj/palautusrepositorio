from tekoaly_parannettu import TekoalyParannettu
from kivi_paperi_sakset import KiviPaperiSakset


class KPSParempiTekoaly(KiviPaperiSakset):

    def __init__(self):
        self.supertekoaly = TekoalyParannettu(10)

    def _toisen_siirto(self, ekan_siirto):
        tokan_siirto = self.supertekoaly.anna_siirto()
        print(f"Tietokone valitsi: {tokan_siirto}")
        self.supertekoaly.aseta_siirto(ekan_siirto)

        return tokan_siirto
