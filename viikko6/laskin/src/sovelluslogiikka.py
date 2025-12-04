class Sovelluslogiikka:
    def __init__(self, arvo=0):
        self._arvo = arvo
        self._edellinen_arvo = [0]
    
    def _tallenna_edellinen(self):
        self._edellinen_arvo.append(self._arvo)

    def miinus(self, operandi):
        self._tallenna_edellinen()
        self._arvo = self._arvo - operandi

    def plus(self, operandi):
        self._tallenna_edellinen()
        self._arvo = self._arvo + operandi

    def nollaa(self):
        self._tallenna_edellinen()
        self._arvo = 0
    
    def kumoa(self):
        if self._edellinen_arvo:
            self._arvo = self._edellinen_arvo[-1]
            self._edellinen_arvo.pop()

    def aseta_arvo(self, arvo):
        self._arvo = arvo

    def arvo(self):
        return self._arvo
