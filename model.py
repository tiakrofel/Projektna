class Knjigozer:

    def __init__(self):
        self.neprebrane = []
        self.trenutne = []
        self.prebrane = []
        self._moja_knjiznica = {}

    def dodaj_neprebrano(self, avtor, naslov, zanr):
        if (naslov, avtor) in self._moja_knjiznica:
            raise ValueError('Ta knjiga je že na enem izmed seznamov v knjižnici!')
        dodana = Neprebrana(naslov, avtor, zanr, self)
        self.neprebrane.append(dodana)
        self._moja_knjiznica[(avtor, naslov)] = 0
        return dodana
    
    def dodaj_trenutno(self, avtor, naslov, zanr, strani, napredek=1):
        prva = Neprebrana(naslov, avtor, zanr, self)
        spremenjena = Trenutna(prva, napredek, strani, self)
        self.trenutne.append(spremenjena)
        self._moja_knjiznica[(prva.avtor, prva.naslov)] = napredek / strani
        return spremenjena

    def izberi_trenutno(self, neprebrana, strani, napredek=1):
        izbrana = Trenutna(neprebrana, napredek, strani, self)
        self.trenutne.append(izbrana)
        self._moja_knjiznica[(neprebrana.avtor, neprebrana.naslov)] = napredek / strani 
        self.neprebrane.remove(neprebrana)
        return izbrana

    def posodobi_trenutno(self, trenutna, napredek):
        posodobljena = Trenutna(trenutna.neprebrana, napredek, trenutna.strani, self)
        self.trenutne.remove(trenutna)
        self.trenutne.append(posodobljena)
        self._moja_knjiznica[(trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)] = napredek / trenutna.strani
        return posodobljena

    def dokoncana(self, datum, trenutna, ocena):
        koncana = Prebrana(datum, trenutna, ocena, self)
        self.prebrane.append(koncana)
        self._moja_knjiznica[(trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)] = 1
        self.trenutne.remove(trenutna)
        return koncana

    def dodaj_prebrano(self, datum, avtor, naslov, zanr, strani, ocena):
        zacetna = Neprebrana(naslov, avtor, zanr, self)
        naslednja = Trenutna(zacetna, 1, strani, self)
        finalna = Prebrana(datum, naslednja, ocena, self)
        self.prebrane.append(finalna)
        self._moja_knjiznica[(zacetna.avtor, zacetna.naslov)] = strani
        return finalna    

    def __str__(self):
        return f'Knjige v knjižnici: {self.neprebrane}, {self.trenutne}, {self.prebrane}'

class Neprebrana:

    def __init__(self, naslov, avtor, zanr, knjigozer):
        self.naslov = naslov
        self.avtor = avtor
        self.zanr = zanr
        self.knjigozer = knjigozer
    
    def __repr__(self):
        return f'<Neprebrana: {self}>'
    
    def __str__(self):
        return f'{self.avtor}: {self.naslov}, {self.zanr}'


class Trenutna:

    def __init__(self, neprebrana, napredek, strani, knjigozer):
        self.neprebrana = neprebrana
        self.napredek = napredek
        self.strani = strani
        self.knjigozer = knjigozer
    
    def __repr__(self):
        return f'<Trenutno brana: {self}>'
    
    def __str__(self):
        return f'{self.neprebrana.avtor}: {self.neprebrana.naslov}, {self.neprebrana.zanr}, stran {self.napredek} od {self.strani}' 
    


class Prebrana:

    def __init__(self, datum, trenutna, ocena, knjigozer):
        self.datum = datum
        self.trenutna = trenutna
        self.ocena = ocena
        self.knjigozer = knjigozer
    
    def __repr__(self):
        return f'<Prebrana: {self}>'
    
    def __str__(self):
        return f'{self.trenutna.neprebrana.avtor}: {self.trenutna.neprebrana.naslov}, {self.trenutna.neprebrana.zanr}, {self.trenutna.strani} strani'