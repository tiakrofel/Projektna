class Knjigozer:

    def __init__(self):
        self.neprebrane = []
        self.trenutne = []
        self.prebrane = []
        self._moja_knjiznica = {}
    
    def ogled_knjig(self):
        for (avtor, naslov) in self._moja_knjiznica:
            print(f'{avtor}: {naslov}')

    def dodaj_neprebrano(self, avtor, naslov):
        if (naslov, avtor) in self._moja_knjiznica:
            raise ValueError('Ta knjiga je že na enem izmed seznamov v tej knjižnici!')
        dodana = Neprebrana(naslov, avtor, self)
        self.neprebrane.append(dodana)
        self._moja_knjiznica[(avtor, naslov)] = 0
        return dodana
    
    def najdi_neprebrano(self, avtor, naslov):
        if (avtor, naslov) not in self._moja_knjiznica:
            raise ValueError('Te knjige ni v tvoji knjižnici.')
        elif Neprebrana(naslov, avtor, self) not in self.neprebrane:
            raise ValueError('Ta knjiga je v tvoji knjižnici, vendar ne med neprebranimi knjigami.')
        return True
    
    def odstrani_neprebrano(self, neprebrana):
        self.neprebrane.remove(neprebrana)
        del self._moja_knjiznica[(neprebrana.avtor, neprebrana.naslov)]
    
    def dodaj_trenutno(self, avtor, naslov, strani, napredek=1):
        if (naslov, avtor) in self._moja_knjiznica:
            raise ValueError('Ta knjiga je že na enem izmed seznamov v tej knjižnici!')
        prva = Neprebrana(naslov, avtor, self)
        spremenjena = Trenutna(prva, napredek, strani, self)
        self.trenutne.append(spremenjena)
        self._moja_knjiznica[(prva.avtor, prva.naslov)] = int(napredek) / int(strani)
        return spremenjena

    def izberi_trenutno(self, neprebrana, strani, napredek=1):
        izbrana = Trenutna(neprebrana, napredek, strani, self)
        self.trenutne.append(izbrana)
        self._moja_knjiznica[(neprebrana.avtor, neprebrana.naslov)] = int(napredek) / int(strani) 
        self.neprebrane.remove(neprebrana)
        return izbrana

    def posodobi_trenutno(self, trenutna, napredek):
        posodobljena = Trenutna(trenutna.neprebrana, napredek, trenutna.strani, self)
        self.trenutne.remove(trenutna)
        self.trenutne.append(posodobljena)
        self._moja_knjiznica[(trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)] = int(napredek) / int(trenutna.strani)
        return posodobljena
    
    def opuscena_trenutna(self, trenutna):
        opuscena = Trenutna(trenutna.neprebrana, trenutna.napredek, trenutna.strani, self)
        vrnjena = Neprebrana(opuscena.neprebrana.naslov, opuscena.neprebrana.avtor, self)
        self.neprebrane.append(vrnjena)
        self.trenutne.remove(trenutna)
        self._moja_knjiznica[(trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)] = 0
        return opuscena

    def dokoncana(self, datum, trenutna, ocena):
        koncana = Prebrana(datum, trenutna, ocena, self)
        self.prebrane.append(koncana)
        self._moja_knjiznica[(trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)] = 1
        self.trenutne.remove(trenutna)
        return koncana

    def direktno_prebrana(self, datum, neprebrana, strani, ocena):
        vmesna = Trenutna(neprebrana, 1, strani, self)
        direktna = Prebrana(datum, vmesna, ocena, self)
        self.prebrane.append(direktna)
        self._moja_knjiznica[(neprebrana.avtor, neprebrana.naslov)] = int(strani)
        self.neprebrane.remove(neprebrana)
        return direktna

    def dodaj_prebrano(self, datum, avtor, naslov, strani, ocena):
        if (naslov, avtor) in self._moja_knjiznica:
            raise ValueError('Ta knjiga je že na enem izmed seznamov v tej knjižnici!')
        zacetna = Neprebrana(naslov, avtor, self)
        naslednja = Trenutna(zacetna, 1, strani, self)
        finalna = Prebrana(datum, naslednja, ocena, self)
        self.prebrane.append(finalna)
        self._moja_knjiznica[(zacetna.avtor, zacetna.naslov)] = int(strani)
        return finalna   
    
    def najdi_prebrano(self, avtor, naslov):
        if (avtor, naslov) not in self._moja_knjiznica:
            raise ValueError('Te knjige še ni v tvoji knjižnici.')
        elif self._moja_knjiznica[(avtor, naslov)] == 0:
            raise ValueError('Ta knjiga je med neprebranimi knjigami.')
        elif self._moja_knjiznica[(avtor, naslov)] != 1:
            raise ValueError('Ta knjiga je med trenutnimi branji.')
        return True

    def odstrani_prebrano(self, prebrana):
        self.prebrane.remove(prebrana)
        del self._moja_knjiznica[(prebrana.trenutna.neprebrana.avtor, prebrana.trenutna.neprebrana.naslov)] 

    def __str__(self):
        return f'Neprebrane knjige: {self.neprebrane}, trenutna branja: {self.trenutne}, prebrane knjige: {self.prebrane}'


class Neprebrana:

    def __init__(self, naslov, avtor, knjigozer):
        self.naslov = naslov
        self.avtor = avtor
        self.knjigozer = knjigozer
    
    def __repr__(self):
        return f'{self}'
    
    def __str__(self):
        return f'{self.avtor}: {self.naslov}'


class Trenutna:

    def __init__(self, neprebrana, napredek, strani, knjigozer):
        self.neprebrana = neprebrana
        self.napredek = napredek
        self.strani = strani
        self.knjigozer = knjigozer
    
    def __repr__(self):
        return f'{self}'
    
    def __str__(self):
        return f'{self.neprebrana.avtor}: {self.neprebrana.naslov}, stran {self.napredek} od {self.strani}' 
    


class Prebrana:

    def __init__(self, datum, trenutna, ocena, knjigozer):
        self.datum = datum
        self.trenutna = trenutna
        self.ocena = ocena
        self.knjigozer = knjigozer
    
    def __repr__(self):
        return f'{self}'
    
    def __str__(self):
        return f'{self.trenutna.neprebrana.avtor}: {self.trenutna.neprebrana.naslov}, {self.trenutna.strani} strani'