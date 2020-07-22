class Knjigozer:

    def __init__(self):
        self.neprebrane = []
        self.trenutne = []
        self.prebrane = []
        self._moja_knjiznica = {}

    def dodaj_neprebrano(self, avtor, naslov, zanr):
        if (naslov, avtor) in self._moja_knjiznica:
            raise ValueError('Ta knjiga je že v tvoji knjižnici!')
        dodana = Neprebrana(naslov, avtor, zanr, self)
        self.neprebrane.append(dodana)
        self._moja_knjiznica[(avtor, naslov)] = 0
        return dodana
    
    def dodaj_trenutno(self, neprebrana, napredek=0):
        izbrana = Trenutna(neprebrana, napredek, self)
        self.trenutne.append(izbrana)
        self._moja_knjiznica[(neprebrana.avtor, neprebrana.naslov)] = napredek 
        self.neprebrane.remove(neprebrana)
        return izbrana

    def dokoncana(self, datum, trenutna, strani, ocena):
        koncana = Prebrana(datum, trenutna, strani, ocena, self)
        self.prebrane.append(koncana)
        self._moja_knjiznica[(trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)] = strani
        self.trenutne.remove(trenutna)
        return f'Bravo! Knjiga {trenutna} je sedaj med tvojimi prebranimi knjigami!'

    def __str__(self):
        return f'Neprebrane: {self.neprebrane}, trenutne: {self.trenutne}, prebrane: {self.prebrane}'

class Neprebrana:

    def __init__(self, naslov, avtor, zanr, knjigozer):
        self.naslov = naslov
        self.avtor = avtor
        self.zanr = zanr
        self.knjigozer = knjigozer
    
    def __repr__(self):
        return f'<Neprebrana: {self}>'
    
    def __str__(self):
        return f'{self.avtor}: {self.naslov}'


class Trenutna:

    def __init__(self, neprebrana, napredek, knjigozer):
        self.neprebrana = neprebrana
        self.napredek = napredek
        self.knjigozer = knjigozer
    
    def __repr__(self):
        return f'<Trenutno brana: {self}>'
    
    def __str__(self):
        return f'{self.neprebrana.avtor}: {self.neprebrana.naslov}, stran {self.napredek}' 
    


class Prebrana:

    def __init__(self, datum, trenutna, strani, ocena, knjigozer):
        self.datum = datum
        self.trenutna = trenutna
        self.strani = strani
        self.ocena = ocena
        self.knjigozer = knjigozer
    
    def __repr__(self):
        return f'<Prebrana: {self}>'
    
    def __str__(self):
        return f'{self.trenutna.neprebrana.avtor}: {self.trenutna.neprebrana.naslov}, {self.strani} strani'