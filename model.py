import json


class Knjigozer:

    def __init__(self):
        self.neprebrane = []
        self.trenutne = []
        self.prebrane = []
        self._slovar_neprebranih = {}
        self._slovar_trenutnih = {}
        self._slovar_prebranih = {}
        self._iskalnik_neprebranih = {}
        self._iskalnik_trenutnih = {}
        self._iskalnik_prebranih = {}
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
        elif self._kategorije_prebranih[kategorija] == 0:
            raise ValueError('V tej kategoriji ni še nobene knjige!')
        for prebrana in self.prebrane:
            if kategorija in prebrana.kategorija:
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

    def preveri_napredek(self, napredek, strani):
        if int(strani) < int(napredek):
            raise ValueError(
                'Prebranih strani ne more biti več, kot je vseh strani v knjigi!')
        elif int(strani) == int(napredek):
            raise ValueError(
                'Prebrali ste vse strani te knjige, zato jo raje vnesite kot prebrano knjigo!')

    def pri_napredku(self, avtor, naslov):
        if (avtor, naslov) in self._iskalnik_neprebranih:
            raise ValueError(
                'Ta knjiga je že med vašimi neprebranimi knjigami.')
        elif (avtor, naslov) in self._iskalnik_trenutnih:
            raise ValueError('Ta knjiga je že med vašimi trenutnimi branji.')
        elif (avtor, naslov) in self._iskalnik_prebranih:
            raise ValueError('Ta knjiga je že med vašimi prebranimi knjigami.')

    def dodaj_neprebrano(self, avtor, naslov):
        self.pri_dodajanju_neprebranih(avtor, naslov)
        neprebrana = Neprebrana(naslov, avtor, self)
        self.neprebrane.append(neprebrana)
        self._iskalnik_neprebranih[(avtor, naslov)] = neprebrana
        self.pri_dodajanju_neprebranih(avtor, naslov)
        return neprebrana

    def odstrani_neprebrano(self, neprebrana):
        if len(self.neprebrane) == 0:
            raise ValueError('V vaši knjižnici ni nobene neprebrane knjige!')
        self.neprebrane.remove(neprebrana)
        del self._iskalnik_neprebranih[(neprebrana.avtor, neprebrana.naslov)]
        self.pri_brisanju_neprebranih(neprebrana.avtor, neprebrana.naslov)

    def dodaj_trenutno(self, avtor, naslov, strani, napredek=1):
        self.pri_dodajanju_trenutnih(avtor, naslov)
        prva = Neprebrana(naslov, avtor, self)
        spremenjena = Trenutna(prva, napredek, strani, self)
        self.preveri_napredek(napredek, strani)
        self.trenutne.append(spremenjena)
        self._iskalnik_trenutnih[(prva.avtor, prva.naslov)] = spremenjena
        self.pri_dodajanju_trenutnih(avtor, naslov)
        return spremenjena

    def izberi_trenutno(self, neprebrana, strani, napredek=1):
        if len(self.neprebrane) == 0:
            raise ValueError('V vaši knjižnici ni nobene neprebrane knjige!')
        elif int(strani) < int(napredek):
            raise ValueError(
                'Prebranih strani ne more biti več, kot je vseh strani v knjigi!')
        elif int(strani) == int(napredek):
            raise ValueError(
                'Prebrali ste vse strani te knjige, vnašate pa jo kot trenutno branje!')
        izbrana = Trenutna(neprebrana, napredek, strani, self)
        self.preveri_napredek(napredek, strani)
        self.trenutne.append(izbrana)
        self.neprebrane.remove(neprebrana)
        self.pri_dodajanju_trenutnih(neprebrana.avtor, neprebrana.naslov)
        self.pri_brisanju_neprebranih(neprebrana.avtor, neprebrana.naslov)
        del self._iskalnik_neprebranih[(neprebrana.avtor, neprebrana.naslov)]
        self._iskalnik_trenutnih[(
            neprebrana.avtor, neprebrana.naslov)] = izbrana
        return izbrana

    def posodobi_trenutno(self, trenutna, napredek):
        if len(self.trenutne) == 0:
            raise ValueError('Trenutno ne berete nobene knjige!')
        posodobljena = Trenutna(trenutna.neprebrana,
                                napredek, trenutna.strani, self)
        self.preveri_napredek(napredek, trenutna.strani)
        self.trenutne.remove(trenutna)
        self.trenutne.append(posodobljena)
        return posodobljena

    def opuscena_trenutna(self, trenutna):
        if len(self.trenutne) == 0:
            raise ValueError('Trenutno ne berete nobene knjige!')
        opuscena = Trenutna(trenutna.neprebrana,
                            trenutna.napredek, trenutna.strani, self)
        vrnjena = Neprebrana(trenutna.neprebrana.naslov,
                             trenutna.neprebrana.avtor, self)
        self.neprebrane.append(vrnjena)
        self.trenutne.remove(trenutna)
        del self._iskalnik_trenutnih[(
            trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)]
        self._iskalnik_neprebranih[(
            trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)] = vrnjena
        self.pri_dodajanju_neprebranih(
            trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)
        self.pri_brisanju_trenutnih(
            trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)
        return opuscena

    def dokoncana(self, datum, trenutna, ocena, kategorija=[]):
        if len(self.trenutne) == 0:
            raise ValueError('Trenutno ne berete nobene knjige!')
        koncana = Prebrana(datum, trenutna, ocena, kategorija, self)
        self.prebrane.append(koncana)
        del self._iskalnik_trenutnih[(
            trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)]
        self._iskalnik_prebranih[(trenutna.neprebrana.avtor,
                                  trenutna.neprebrana.naslov)] = koncana
        self.trenutne.remove(trenutna)
        self.pri_dodajanju_prebranih(
            trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)
        self.pri_brisanju_trenutnih(
            trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)
        return koncana

    def odstrani_trenutno(self, trenutna):
        if len(self.trenutne) == 0:
            raise ValueError('Trenutno ne berete nobene knjige!')
        self.trenutne.remove(trenutna)
        del self._iskalnik_trenutnih[(
            trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)]
        self.pri_brisanju_trenutnih(
            trenutna.neprebrana.avtor, trenutna.neprebrana.naslov)

    def direktno_prebrana(self, datum, neprebrana, strani, ocena, kategorija=[]):
        if len(self.neprebrane) == 0:
            raise ValueError('V vaši knjižnici ni nobene neprebrane knjige!')
        vmesna = Trenutna(neprebrana, 1, strani, self)
        direktna = Prebrana(datum, vmesna, ocena, kategorija, self)
        self.prebrane.append(direktna)
        self.neprebrane.remove(neprebrana)
        self.pri_dodajanju_prebranih(neprebrana.avtor, neprebrana.naslov)
        self.pri_dodajanju_neprebranih(neprebrana.avtor, neprebrana.naslov)
        del self._iskalnik_neprebranih[(neprebrana.avtor, neprebrana.naslov)]
        self._iskalnik_prebranih[(
            neprebrana.avtor, neprebrana.naslov)] = direktna
        return direktna

    def dodaj_prebrano(self, datum, avtor, naslov, strani, ocena, kategorija=[]):
        self.pri_dodajanju_prebranih(avtor, naslov)
        zacetna = Neprebrana(naslov, avtor, self)
        naslednja = Trenutna(zacetna, 1, strani, self)
        finalna = Prebrana(datum, naslednja, ocena, kategorija, self)
        self.prebrane.append(finalna)
        self.pri_dodajanju_prebranih(avtor, naslov)
        self._iskalnik_prebranih[(avtor, naslov)] = finalna
        return finalna

    def odstrani_prebrano(self, prebrana):
        if len(self.prebrane) == 0:
            raise ValueError('V vaši knjižnici ni nobene prebrane knjige!')
        self.prebrane.remove(prebrana)
        for kategorija in prebrana.kategorija:
            self.iz_kategorije(kategorija, prebrana)
        del self._iskalnik_prebranih[(
            prebrana.trenutna.neprebrana.avtor, prebrana.trenutna.neprebrana.naslov)]
        self.pri_brisanju_prebranih(
            prebrana.trenutna.neprebrana.avtor, prebrana.trenutna.neprebrana.naslov)

    def posodobi_prebrano_nova(self, prebrana, nova_kategorija):
        seznam = prebrana.kategorija
        seznam.append(nova_kategorija)
        posodobljena = Prebrana(
            prebrana.datum, prebrana.trenutna, prebrana.ocena, seznam, self)
        self.prebrane.remove(prebrana)
        self.prebrane.append(posodobljena)
        return posodobljena

    def posodobi_prebrano_stara(self, prebrana, stara_kategorija):
        seznam = prebrana.kategorija
        seznam.remove(stara_kategorija)
        posodobljena = Prebrana(
            prebrana.datum, prebrana.trenutna, prebrana.ocena, seznam, self)
        self.prebrane.remove(prebrana)
        self.prebrane.append(posodobljena)
        return posodobljena

    def poisci_neprebrano(self, vrednost):
        return self._iskalnik_neprebranih[vrednost]

    def poisci_trenutno(self, vrednost):
        return self._iskalnik_trenutnih[vrednost]

    def poisci_prebrano(self, vrednost):
        return self._iskalnik_prebranih[vrednost]

    def nova_kategorija(self, kategorija):
        if kategorija in self._kategorije_prebranih:
            raise ValueError('Kategorija s tem imenom že obstaja!')
        self._kategorije_prebranih[kategorija] = 0
        return kategorija

    def v_kategorijo(self, kategorija, prebrana):
        if kategorija in prebrana.kategorija:
            return ValueError('Ta knjiga je že v tej kategoriji!')
        self._kategorije_prebranih[kategorija] += 1
        self.posodobi_prebrano_nova(prebrana, kategorija)
        return self._kategorije_prebranih[kategorija]

    def povecana_kategorija(self, kategorija):
        self._kategorije_prebranih[kategorija] += 1
        return self._kategorije_prebranih[kategorija]

    def iz_kategorije(self, kategorija, prebrana):
        if self._kategorije_prebranih[kategorija] == 0:
            raise ValueError(f'V kategoriji "{kategorija}" ni nobene knjige!')
        self._kategorije_prebranih[kategorija] -= 1
        self.posodobi_prebrano_stara(prebrana, kategorija)

    def odstrani_kategorijo(self, kategorija):
        if len(self._kategorije_prebranih) == 0:
            raise ValueError(
                'Ustvarili niste še nobene kategorije prebranih knjig!')
        for prebrana in self.prebrane:
            if kategorija in prebrana.kategorija:
                self.posodobi_prebrano_stara(prebrana, kategorija)
        del self._kategorije_prebranih[kategorija]

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
                'kategorije': prebrana.kategorija,
            } for prebrana in self.prebrane],
            'kategorije prebranih knjig': [{
                'ime': kategorija,
                'število knjig': self._kategorije_prebranih[kategorija],
            } for kategorija in self._kategorije_prebranih]
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
                prebrana['datum'], prebrana['avtor'], prebrana['naslov'], prebrana['strani'], prebrana['ocena'], prebrana['kategorije'])
        for kategorija in slovar_knjig['kategorije prebranih knjig']:
            nova_kategorija = knjigozer.nova_kategorija(kategorija['ime'])
            for prebrana in slovar_knjig['prebrane knjige']:
                if kategorija['ime'] in prebrana['kategorije']:
                    knjigozer.povecana_kategorija(kategorija['ime'])
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

    def __lt__(self, other):
        if self.avtor == other.avtor:
            return self.naslov < other.naslov
        else:
            return self.avtor < other.avtor

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
    
    def __lt__(self, other):
        return self.neprebrana < other.neprebrana


class Prebrana:

    def __init__(self, datum, trenutna, ocena, kategorija, knjigozer):
        self.datum = datum
        self.trenutna = trenutna
        self.ocena = ocena
        self.kategorija = kategorija
        self.knjigozer = knjigozer

    def __repr__(self):
        return f'{self}'

    def __str__(self):
        return f'{self.trenutna.neprebrana.avtor}: {self.trenutna.neprebrana.naslov}, {self.trenutna.strani} strani'

    def __lt__(self, other):
        return self.trenutna < other.trenutna