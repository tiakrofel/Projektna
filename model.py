class Knjigozer:

    def __init__(self):
        self.neprebrane = []
        self.trenutne = []
        self.prebrane = []
        self._moja_knjiznica = {}
        self._slovar_neprebranih = {}
        self._slovar_trenutnih = {}
        self._slovar_prebranih = {}
        self._kategorije_prebranih = {None: []}
        self._uspehi = {}

    def ogled_knjig(self):
        for avtor in sorted(self._slovar_neprebranih):
            for naslov in self._slovar_neprebranih[avtor]:
                print(f'{avtor}: {naslov}, neprebrana')
        for avtor in sorted(self._slovar_trenutnih):
            for naslov in self._slovar_trenutnih[avtor]:
                print(f'{avtor}: {naslov}, trenutno branje')
        for avtor in sorted(self._slovar_prebranih):
            for naslov in self._slovar_prebranih[avtor]:
                print(f'{avtor}: {naslov}, prebrana')


    def ogled_neprebranih(self):
        for avtor in sorted(self._slovar_neprebranih):
            for naslov in self._slovar_neprebranih[avtor]:
                print(f'{avtor}: {naslov}')
        
    
    def ogled_trenutnih(self):
        for avtor in sorted(self._slovar_trenutnih):
            for naslov in self._slovar_trenutnih[avtor]:
                print(f'{avtor}: {naslov}')
    

    def ogled_prebranih(self):
        for avtor in sorted(self._slovar_prebranih):
            for naslov in self._slovar_prebranih[avtor]:
                print(f'{avtor}: {naslov}')
    

    def ogled_kategorij(self):
        for kategorija in self._kategorije_prebranih:
            print(f'{kategorija}')


    def ogled_knjig_kategorije(self, kategorija):
        for (avtor, naslov) in self._kategorije_prebranih[kategorija]:
            print(f'{avtor}: {naslov}')


    def pri_dodajanju_neprebranih(self, avtor, naslov):
        if avtor not in self._slovar_neprebranih:
            self._slovar_neprebranih[avtor] = [naslov]
        elif avtor in self._slovar_neprebranih:
            self._slovar_neprebranih[avtor].append(naslov)
    

    def pri_brisanju_neprebranih(self, avtor, naslov):
        if len(self._slovar_neprebranih[avtor]) == 1:
            del self._slovar_neprebranih[avtor]
        else:
            self._slovar_neprebranih[avtor].remove(naslov)
    

    def pri_brisanju_trenutnih(self, avtor, naslov):
        if len(self._slovar_trenutnih[avtor]) == 1:
            del self._slovar_trenutnih[avtor]
        else:
            self._slovar_trenutnih[avtor].remove(naslov)
    

    def pri_brisanju_prebranih(self, avtor, naslov):
        if len(self._slovar_prebranih[avtor]) == 1:
            del self._slovar_prebranih[avtor]
        else:
            self._slovar_prebranih[avtor].remove(naslov)


    def pri_dodajanju_trenutnih(self, avtor, naslov):
        if avtor not in self._slovar_trenutnih:
            self._slovar_trenutnih[avtor] = [naslov]
        elif avtor in self._slovar_trenutnih:
            self._slovar_trenutnih[avtor].append(naslov)
    

    def pri_dodajanju_prebranih(self, avtor, naslov):
        if avtor not in self._slovar_prebranih:
            self._slovar_prebranih[avtor] = [naslov]
        elif avtor in self._slovar_prebranih:
            self._slovar_prebranih[avtor].append(naslov)


    def dodaj_neprebrano(self, avtor, naslov):
        if (avtor, naslov) in self._moja_knjiznica:
            if avtor in self._slovar_neprebranih:
                raise ValueError('Ta knjiga je že med vašimi neprebranimi knjigami.')
            elif (naslov, avtor) in self._slovar_trenutnih:
                raise ValueError('Ta knjiga je že med vašimi trenutnimi branji.')
            elif (naslov, avtor) in self._slovar_prebranih:
                raise ValueError('Ta knjiga je že med vašimi prebranimi knjigami.')
        neprebrana = Neprebrana(naslov, avtor, self)
        self.neprebrane.append(neprebrana)
        self._moja_knjiznica[(avtor, naslov)] = 0
        self.pri_dodajanju_neprebranih(avtor, naslov)
        return neprebrana


    def odstrani_neprebrano(self, neprebrana):
        self.neprebrane.remove(neprebrana)
        del self._moja_knjiznica[(neprebrana.avtor, neprebrana.naslov)]
        self.pri_brisanju_neprebranih(neprebrana.avtor, neprebrana.naslov)


    def dodaj_trenutno(self, avtor, naslov, strani, napredek=1):
        if (naslov, avtor) in self._moja_knjiznica:
            raise ValueError('Ta knjiga je že na enem izmed seznamov v tej knjižnici!')
        prva = Neprebrana(naslov, avtor, self)
        spremenjena = Trenutna(prva, napredek, strani, self)
        self.trenutne.append(spremenjena)
        self._moja_knjiznica[(prva.avtor, prva.naslov)] = int(napredek) / int(strani)
        self.pri_dodajanju_trenutnih(avtor, naslov)
        return spremenjena


    def izberi_trenutno(self, neprebrana, strani, napredek=1):
        izbrana = Trenutna(neprebrana, napredek, strani, self)
        self.trenutne.append(izbrana)
        self._moja_knjiznica[(neprebrana.avtor, neprebrana.naslov)] = int(
            napredek) / int(strani)
        self.neprebrane.remove(neprebrana)
        self.pri_dodajanju_trenutnih(neprebrana.avtor, neprebrana.naslov)
        self.pri_brisanju_neprebranih(neprebrana.avtor, neprebrana.naslov)
        return izbrana


    def posodobi_trenutno(self, trenutna, napredek):
        posodobljena = Trenutna(trenutna.neprebrana,
                                napredek, trenutna.strani, self)
        self.trenutne.remove(trenutna)
        self.trenutne.append(posodobljena)
        self._moja_knjiznica[(trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)] = int(
            napredek) / int(trenutna.strani)
        return posodobljena


    def opuscena_trenutna(self, trenutna):
        opuscena = Trenutna(trenutna.neprebrana,
                            trenutna.napredek, trenutna.strani, self)
        vrnjena = Neprebrana(opuscena.neprebrana.naslov,
                             opuscena.neprebrana.avtor, self)
        self.neprebrane.append(vrnjena)
        self.trenutne.remove(trenutna)
        self._moja_knjiznica[(trenutna.neprebrana.avtor,
                              trenutna.neprebrana.naslov)] = 0
        self.pri_dodajanju_neprebranih(trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)
        self.pri_brisanju_trenutnih(trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)
        return opuscena


    def dokoncana(self, datum, trenutna, ocena):
        koncana = Prebrana(datum, trenutna, ocena, self)
        self.prebrane.append(koncana)
        self._moja_knjiznica[(trenutna.neprebrana.avtor,
                              trenutna.neprebrana.naslov)] = int(trenutna.strani)
        self.trenutne.remove(trenutna)
        self._uspehi[(trenutna.neprebrana.avtor,
                      trenutna.neprebrana.naslov)] = datum
        self.pri_dodajanju_prebranih(trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)
        self.pri_brisanju_trenutnih(trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)
        return koncana


    def direktno_prebrana(self, datum, neprebrana, strani, ocena):
        vmesna = Trenutna(neprebrana, 1, strani, self)
        direktna = Prebrana(datum, vmesna, ocena, self)
        self.prebrane.append(direktna)
        self.neprebrane.remove(neprebrana)
        self._moja_knjiznica[(neprebrana.avtor, neprebrana.naslov)] = int(strani)
        self._uspehi[(neprebrana.avtor, neprebrana.naslov)] = datum
        self.pri_dodajanju_prebranih(neprebrana.avtor, neprebrana.naslov)
        self.pri_dodajanju_neprebranih(neprebrana.avtor, neprebrana.naslov)
        return direktna


    def dodaj_prebrano(self, datum, avtor, naslov, strani, ocena):
        if (naslov, avtor) in self._moja_knjiznica:
            raise ValueError('Ta knjiga je že na enem izmed seznamov v tej knjižnici!')
        zacetna = Neprebrana(naslov, avtor, self)
        naslednja = Trenutna(zacetna, 1, strani, self)
        finalna = Prebrana(datum, naslednja, ocena, self)
        self.prebrane.append(finalna)
        self._moja_knjiznica[(zacetna.avtor, zacetna.naslov)] = int(strani)
        self.pri_dodajanju_prebranih(avtor, naslov)
        self._uspehi[(avtor, naslov)] = datum
        return finalna


    def odstrani_prebrano(self, prebrana):
        self.prebrane.remove(prebrana)
        del self._moja_knjiznica[(prebrana.trenutna.neprebrana.avtor, prebrana.trenutna.neprebrana.naslov)]
        self.pri_brisanju_prebranih(prebrana.trenutna.neprebrana.avtor, prebrana.trenutna.neprebrana.naslov)


    def nova_kategorija(self, kategorija):
        if kategorija in self._kategorije_prebranih:
            ValueError('Ta kategorija že obstaja!')
        self._kategorije_prebranih[kategorija] = []
        return True
    

    def v_kategorijo(self, kategorija, prebrana):
        if kategorija not in self._kategorije_prebranih:
            ValueError('Ta kategorija še ne obstaja!')
        self._kategorije_prebranih[kategorija].append((prebrana.trenutna.neprebrana.avtor, prebrana.trenutna.neprebrana.naslov))
        return True
    

    def iz_kategorije(self, kategorija, prebrana):
        if kategorija not in self._kategorije_prebranih:
            ValueError('Ta kategorija ne obstaja!')
        elif prebrana not in self._kategorije_prebranih[kategorija]:
            ValueError('Te knjige ni v tej kategoriji!')
        self._kategorije_prebranih[kategorija].remove(prebrana)
    

    def odstrani_kategorijo(self, kategorija):
        if kategorija not in self._kategorije_prebranih:
            ValueError('Ta kategorija sploh ne obstaja!')
        del self._kategorije_prebranih[kategorija]
        

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