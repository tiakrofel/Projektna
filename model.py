import json


class Knjigozer:

    def __init__(self):
        self.neprebrane = []
        self.trenutne = []
        self.prebrane = []
        self._moja_knjiznica = {}
        self._slovar_neprebranih = {}
        self._slovar_trenutnih = {}
        self._slovar_prebranih = {}
        self._kategorije_prebranih = {}

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
        if len(self.neprebrane) == 0:
            raise ValueError('V vaši knjižnici ni nobene neprebrane knjige!')
        for avtor in sorted(self._slovar_neprebranih):
            for naslov in self._slovar_neprebranih[avtor]:
                print(f'{avtor}: {naslov}')

    def ogled_trenutnih(self):
        if len(self.trenutne) == 0:
            raise ValueError('Trenutno ne berete nobene knjige!')
        for avtor in sorted(self._slovar_trenutnih):
            for naslov in self._slovar_trenutnih[avtor]:
                print(f'{avtor}: {naslov}')

    def ogled_prebranih(self):
        if len(self.prebrane) == 0:
            raise ValueError('V vaši knjižnici ni nobene prebrane knjige!')
        for avtor in sorted(self._slovar_prebranih):
            for naslov in self._slovar_prebranih[avtor]:
                print(f'{avtor}: {naslov}')

    def ogled_kategorij(self):
        if len(self._kategorije_prebranih) == 0:
            raise ValueError(
                'Ustvarili niste še nobene kategorije prebranih knjig!')
        for kategorija in self._kategorije_prebranih:
            print(f'{kategorija}')

    def ogled_knjig_kategorije(self, kategorija):
        if len(self._kategorije_prebranih) == 0:
            raise ValueError('Najprej je potrebno kategorijo ustvariti!')
        elif len(self._kategorije_prebranih[kategorija]) == 0:
            raise ValueError('V tej kategoriji ni še nobene knjige!')
        for prebrana in self._kategorije_prebranih[kategorija]:
            print(
                f'{prebrana.trenutna.neprebrana.avtor}: {prebrana.trenutna.neprebrana.naslov}')

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
                raise ValueError(
                    'Ta knjiga je že med vašimi neprebranimi knjigami.')
            elif (naslov, avtor) in self._slovar_trenutnih:
                raise ValueError(
                    'Ta knjiga je že med vašimi trenutnimi branji.')
            elif (naslov, avtor) in self._slovar_prebranih:
                raise ValueError(
                    'Ta knjiga je že med vašimi prebranimi knjigami.')
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
            raise ValueError(
                'Ta knjiga je že na enem izmed seznamov v tej knjižnici!')
        prva = Neprebrana(naslov, avtor, self)
        spremenjena = Trenutna(prva, napredek, strani, self)
        self.trenutne.append(spremenjena)
        self._moja_knjiznica[(prva.avtor, prva.naslov)
                             ] = int(napredek) / int(strani)
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
        self.pri_dodajanju_neprebranih(
            trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)
        self.pri_brisanju_trenutnih(
            trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)
        return opuscena

    def dokoncana(self, datum, trenutna, ocena):
        koncana = Prebrana(datum, trenutna, ocena, self)
        self.prebrane.append(koncana)
        self._moja_knjiznica[(trenutna.neprebrana.avtor,
                              trenutna.neprebrana.naslov)] = int(trenutna.strani)
        self.trenutne.remove(trenutna)
        self.pri_dodajanju_prebranih(
            trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)
        self.pri_brisanju_trenutnih(
            trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)
        return koncana

    def direktno_prebrana(self, datum, neprebrana, strani, ocena):
        vmesna = Trenutna(neprebrana, 1, strani, self)
        direktna = Prebrana(datum, vmesna, ocena, self)
        self.prebrane.append(direktna)
        self.neprebrane.remove(neprebrana)
        self._moja_knjiznica[(
            neprebrana.avtor, neprebrana.naslov)] = int(strani)
        self.pri_dodajanju_prebranih(neprebrana.avtor, neprebrana.naslov)
        self.pri_dodajanju_neprebranih(neprebrana.avtor, neprebrana.naslov)
        return direktna

    def dodaj_prebrano(self, datum, avtor, naslov, strani, ocena):
        if (naslov, avtor) in self._moja_knjiznica:
            raise ValueError(
                'Ta knjiga je že na enem izmed seznamov v tej knjižnici!')
        zacetna = Neprebrana(naslov, avtor, self)
        naslednja = Trenutna(zacetna, 1, strani, self)
        finalna = Prebrana(datum, naslednja, ocena, self)
        self.prebrane.append(finalna)
        self._moja_knjiznica[(zacetna.avtor, zacetna.naslov)] = int(strani)
        self.pri_dodajanju_prebranih(avtor, naslov)
        return finalna

    def odstrani_prebrano(self, prebrana):
        self.prebrane.remove(prebrana)
        del self._moja_knjiznica[(
            prebrana.trenutna.neprebrana.avtor, prebrana.trenutna.neprebrana.naslov)]
        self.pri_brisanju_prebranih(
            prebrana.trenutna.neprebrana.avtor, prebrana.trenutna.neprebrana.naslov)

    def nova_kategorija(self, kategorija):
        if kategorija in self._kategorije_prebranih:
            raise ValueError('Kategorija s tem imenom že obstaja!')
        self._kategorije_prebranih[kategorija] = []
        return kategorija

    def v_kategorijo(self, kategorija, prebrana):
        if prebrana in self._kategorije_prebranih[kategorija]:
            raise ValueError(f'Ta knjiga je že v kategoriji "{kategorija}"!')
        self._kategorije_prebranih[kategorija].append(prebrana)

    def iz_kategorije(self, kategorija, prebrana):
        if len(self._kategorije_prebranih[kategorija]) == 0:
            raise ValueError(f'V kategoriji "{kategorija}" ni nobene knjige!')
        self._kategorije_prebranih[kategorija].remove(prebrana)

    def odstrani_kategorijo(self, kategorija):
        del self._kategorije_prebranih[kategorija]

    def poisci_kategorijo(self, prebrana):
        najdene = []
        for kategorija in self._kategorije_prebranih:
            if prebrana in self._kategorije_prebranih[kategorija]:
                najdene.append(kategorija)
        return najdene

    def __str__(self):
        return f'Neprebrane knjige: {self.neprebrane}, trenutna branja: {self.trenutne}, prebrane knjige: {self.prebrane}'

    def slovar_knjig(self):
        return {
            'neprebrane knjige': [{
                'avtor': neprebrana.avtor,
                'naslov': neprebrana.naslov,
            } for neprebrana in self.neprebrane],
            'trenutna branja': [{
                'avtor': trenutna.neprebrana.avtor,
                'naslov': trenutna.neprebrana.naslov,
                'napredek': trenutna.napredek,
                'strani': trenutna.strani,
            } for trenutna in self.trenutne],
            'prebrane knjige': [{
                'avtor': prebrana.trenutna.neprebrana.avtor,
                'naslov': prebrana.trenutna.neprebrana.naslov,
                'strani': prebrana.trenutna.strani,
                'datum': str(prebrana.datum),
                'ocena': prebrana.ocena,
            } for prebrana in self.prebrane],
        }

    @classmethod
    def nalozi_iz_slovarja_knjig(cls, slovar_knjig):
        knjigozer = cls()
        for neprebrana in slovar_knjig['neprebrane knjige']:
            dodaj_neprebrano = knjigozer.dodaj_neprebrano(
                neprebrana['avtor'], neprebrana['naslov'])
        for trenutna in slovar_knjig['trenutna branja']:
            dodaj_trenutno = knjigozer.dodaj_trenutno(
                trenutna['avtor'], trenutna['naslov'], trenutna['strani'], trenutna['napredek'])
        for prebrana in slovar_knjig['prebrane knjige']:
            dodaj_prebrano = knjigozer.dodaj_prebrano(
                prebrana['datum'], prebrana['avtor'], prebrana['naslov'], prebrana['strani'], prebrana['ocena'])
        return knjigozer

    def shrani_knjige(self, ime_datoteke):
        with open(ime_datoteke, 'w') as datoteka:
            json.dump(self.slovar_knjig(), datoteka,
                      ensure_ascii=False, indent=4)

    @classmethod
    def nalozi_knjige(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_knjig = json.load(datoteka)
        return cls.nalozi_iz_slovarja_knjig(slovar_knjig)


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
