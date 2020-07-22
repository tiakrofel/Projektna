class Knjigozer:

    def __init__(self):
        self.neprebrane = []
        self.trenutne = []
        self.prebrane = []
        self._moja_knjiznica = {}

    def dodaj_neprebrano(self, naslov, avtor, zanr):
        if (naslov, avtor) in self._moja_knjiznica:
            raise ValueError('Ta knjiga je že v tvoji knjižnici!')
        dodana = Neprebrana(naslov, avtor, zanr, self)
        self.neprebrane.append(dodana)
        self._moja_knjiznica[(naslov, avtor)] = 0
        return dodana
    
    def dodaj_trenutno(self, neprebrana, strani, napredek=0):
        izbrana = Trenutna(neprebrana, strani, napredek, self)
        self.trenutne.append(izbrana)
        self._moja_knjiznica[(neprebrana.naslov, neprebrana.avtor)] = napredek 
        self.neprebrane.remove(neprebrana)
        return izbrana

    def dokoncana(self, datum, trenutna, ocena):
        koncana = Prebrana(datum, trenutna, ocena, self)
        self.prebrane.append(koncana)
        self._moja_knjiznica[(trenutna.naslov, trenutna.avtor)] = trenutna.strani
        self.trenutne.remove(trenutna)
        return f'Bravo! Knjiga {trenutna} je sedaj med tvojimi prebranimi knjigami!'

    def slovarcek(self):
        return {
            'neprebrane': [{
                'naslov': neprebrana.naslov,
                'avtor': neprebrana.avtor,
                'zanr': neprebrana.zanr,
            } for neprebrana in self.neprebrane],
            'trenutne': [{
                'naslov': trenutna.neprebrana.naslov,
                'avtor': trenutna.neprebrana.avtor,
                'zanr': trenutna.neprebrana.zanr,
                'strani': trenutna.strani,
                'napredek': trenutna.napredek,
            } for trenutna in self.trenutne],
            'prebrane': [{
                'datum': str(prebrana.datum),
                'naslov': prebrana.trenutna.neprebrana.naslov,
                'avtor': prebrana.trenutna.neprebrana.avtor,
                'zanr': prebrana.trenutna.neprebrana.zanr,
                'strani': prebrana.trenutna.strani,
                'ocena': prebrana.ocena,
            } for prebrana in self.prebrane],
        }

class Neprebrana:

    def __init__(self, naslov, avtor, zanr, knjigozer):
        self.naslov = naslov
        self.avtor = avtor
        self.zanr = zanr
        self.knjigozer = knjigozer


class Trenutna:

    def __init__(self, neprebrana, strani, napredek, knjigozer):
        self.neprebrana = neprebrana
        self.strani = strani
        self.napredek = napredek
        self.knjigozer = knjigozer 
    


class Prebrana:

    def __init__(self, datum, trenutna, ocena, knjigozer):
        self.datum = datum
        self.neprebrana = trenutna
        self.ocena = ocena
        self.knjigozer = knjigozer