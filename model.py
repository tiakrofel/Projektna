import json


class Uporabnik:
    def __init__(self, uporabnisko_ime, zasifrirano_geslo, knjigozer):
        self.uporabnisko_ime = uporabnisko_ime
        self.zasifrirano_geslo = zasifrirano_geslo
        self.knjigozer = knjigozer

    def preveri_geslo(self, zasifrirano_geslo):
        if self.zasifrirano_geslo != zasifrirano_geslo:
            raise ValueError('Geslo je napačno!')

    def shrani_knjige(self, ime_datoteke):
        slovar_knjig = {
            'uporabnisko_ime': self.uporabnisko_ime,
            'zasifrirano_geslo': self.zasifrirano_geslo,
            'knjigozer': self.knjigozer.slovar_knjig()
        }
        with open(ime_datoteke, 'w') as datoteka:
            json.dump(slovar_knjig, datoteka, ensure_ascii=False, indent=4)

    @classmethod
    def nalozi_knjige(cls, ime_datoteke):
        with open(ime_datoteke) as datoteka:
            slovar_knjig = json.load(datoteka)
        uporabnisko_ime = slovar_knjig['uporabnisko_ime']
        zasifrirano_geslo = slovar_knjig['zasifrirano_geslo']
        knjigozer = Knjigozer.nalozi_iz_slovarja_knjig(
            slovar_knjig['knjigozer'])
        return cls(uporabnisko_ime, zasifrirano_geslo, knjigozer)


class Knjigozer:

    def __init__(self):
        self.neprebrane = []
        self.trenutne = []
        self.prebrane = []
        self.kategorije = []
        self._iskalnik_neprebranih = {}
        self._iskalnik_trenutnih = {}
        self._iskalnik_prebranih = {}
        self._iskalnik_kategorij = {}
        self._kategorije_prebranih = {}

    def preveri_obstoj(self, avtor, naslov):
        if (avtor, naslov) in self._iskalnik_neprebranih:
            raise ValueError(
                'Ta knjiga je že med vašimi neprebranimi knjigami!')
        elif (avtor, naslov) in self._iskalnik_trenutnih:
            raise ValueError('Ta knjiga je že med vašimi trenutnimi branji!')
        elif (avtor, naslov) in self._iskalnik_prebranih:
            raise ValueError('Ta knjiga je že med vašimi prebranimi knjigami!')

    def ogled_knjig(self):
        for (avtor, naslov) in sorted(self._iskalnik_neprebranih):
            print(f'{avtor}: {naslov}, neprebrana')
        for (avtor, naslov) in sorted(self._iskalnik_trenutnih):
            print(f'{avtor}: {naslov}, trenutno branje')
        for (avtor, naslov) in sorted(self._iskalnik_prebranih):
            print(f'{avtor}: {naslov}, prebrana')

    def ogled_neprebranih(self):
        if len(self.neprebrane) == 0:
            print('V vaši knjižnici ni nobene neprebrane knjige!')
        for (avtor, naslov) in sorted(self._iskalnik_neprebranih):
            print(f'{avtor}: {naslov}')

    def ogled_trenutnih(self):
        if len(self.trenutne) == 0:
            print('V vaši knjižnici ni nobenega trenutnega branja!')
        for (avtor, naslov) in sorted(self._iskalnik_trenutnih):
            print(f'{avtor}: {naslov}')

    def ogled_prebranih(self):
        if len(self.prebrane) == 0:
            print('V vaši knjižnici ni nobene prebrane knjige!')
        for (avtor, naslov) in sorted(self._iskalnik_prebranih):
            print(f'{avtor}: {naslov}')

    def ogled_kategorij(self):
        if len(self.kategorije) == 0:
            raise ValueError(
                'Ustvarili niste še nobene kategorije prebranih knjig!')
        for ime in self._iskalnik_kategorij:
            print(f'{ime}')

    def ogled_knjig_kategorije(self, kategorija):
        if len(self.kategorije) == 0:
            raise ValueError('Najprej je potrebno kategorijo ustvariti!')
        elif len(kategorija.knjige) == 0:
            raise ValueError('V tej kategoriji ni še nobene knjige!')
        for knjiga in kategorija.knjige:
            print(
                f'{knjiga.avtor}: {knjiga.naslov}')

    def pri_brisanju_neprebranih(self, avtor, naslov):
        del self._iskalnik_neprebranih[(avtor, naslov)]

    def pri_brisanju_trenutnih(self, avtor, naslov):
        del self._iskalnik_trenutnih[(avtor, naslov)]

    def pri_brisanju_prebranih(self, avtor, naslov):
        del self._iskalnik_prebranih[(avtor, naslov)]

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
        if avtor == '' or avtor == ', ' or naslov == '':
            raise ValueError('Niste vnesli vseh zahtevanih podatkov!')
        neprebrana = Neprebrana(avtor, naslov, self)
        self.preveri_obstoj(avtor, naslov)
        self.neprebrane.append(neprebrana)
        self._iskalnik_neprebranih[(avtor, naslov)] = neprebrana
        return neprebrana

    def odstrani_neprebrano(self, neprebrana):
        if len(self.neprebrane) == 0:
            raise ValueError('V vaši knjižnici ni nobene neprebrane knjige!')
        self.neprebrane.remove(neprebrana)
        self.pri_brisanju_neprebranih(neprebrana.avtor, neprebrana.naslov)

    def dodaj_trenutno(self, avtor, naslov, strani, napredek=1):
        if avtor == '' or avtor == ', ' or naslov == '' or strani == '':
            raise ValueError('Niste vnesli vseh zahtevanih podatkov!')
        knjiga = Trenutna(avtor, naslov, napredek, strani, self)
        self.preveri_obstoj(avtor, naslov)
        self.preveri_napredek(napredek, strani)
        self.trenutne.append(knjiga)
        self._iskalnik_trenutnih[(knjiga.avtor, knjiga.naslov)] = knjiga
        return knjiga

    def izberi_trenutno(self, neprebrana, strani, napredek=1):
        if len(self.neprebrane) == 0:
            raise ValueError('V vaši knjižnici ni nobene neprebrane knjige!')
        elif int(strani) < int(napredek):
            raise ValueError(
                'Prebranih strani ne more biti več, kot je vseh strani v knjigi!')
        elif int(strani) == int(napredek):
            raise ValueError(
                'Prebrali ste vse strani te knjige, vnašate pa jo kot trenutno branje!')
        elif strani == '':
            raise ValueError('Niste vnesli vseh zahtevanih podatkov!')
        izbrana = Trenutna(
            neprebrana.avtor, neprebrana.naslov, napredek, strani, self)
        self.preveri_napredek(napredek, strani)
        self.trenutne.append(izbrana)
        self.odstrani_neprebrano(neprebrana)
        self._iskalnik_trenutnih[(
            neprebrana.avtor, neprebrana.naslov)] = izbrana
        return izbrana

    def posodobi_trenutno(self, trenutna, napredek):
        if len(self.trenutne) == 0:
            raise ValueError('Trenutno ne berete nobene knjige!')
        elif napredek == '':
            raise ValueError('Niste vnesli vseh zahtevanih podatkov!')
        posodobljena = Trenutna(
            trenutna.avtor, trenutna.naslov, napredek, trenutna.strani, self)
        self.preveri_napredek(napredek, trenutna.strani)
        self.trenutne.remove(trenutna)
        self.trenutne.append(posodobljena)
        self._iskalnik_trenutnih[(
            trenutna.avtor, trenutna.naslov)] = posodobljena
        return posodobljena

    def opuscena_trenutna(self, trenutna):
        if len(self.trenutne) == 0:
            raise ValueError('Trenutno ne berete nobene knjige!')
        opuscena = Trenutna(trenutna.avtor, trenutna.naslov,
                            trenutna.napredek, trenutna.strani, self)
        vrnjena = Neprebrana(trenutna.avtor, trenutna.naslov, self)
        self.neprebrane.append(vrnjena)
        self.trenutne.remove(trenutna)
        self.pri_brisanju_trenutnih(trenutna.avtor, trenutna.naslov)
        self._iskalnik_neprebranih[(trenutna.avtor, trenutna.naslov)] = vrnjena
        return opuscena

    def prebran_del(self, trenutna):
        return int(trenutna.napredek) / int(trenutna.strani)

    def dokoncana(self, datum, trenutna, ocena):
        if len(self.trenutne) == 0:
            raise ValueError('Trenutno ne berete nobene knjige!')
        elif ocena == '':
            raise ValueError('Niste vnesli vseh zahtevanih podatkov!')
        koncana = Prebrana(datum, trenutna.avtor,
                           trenutna.naslov, ocena, self)
        self.prebrane.append(koncana)
        self._kategorije_prebranih[koncana] = []
        self.odstrani_trenutno(trenutna)
        self._iskalnik_prebranih[(trenutna.avtor, trenutna.naslov)] = koncana
        return koncana

    def ponovno_brana(self, prebrana, strani, napredek=1):
        if len(self.prebrane) == 0:
            raise ValueError('V vaši knjižnici ni nobene prebrane knjige!')
        elif strani == '':
            raise ValueError('Niste vnesli vseh zahtevanih podatkov!')
        ponovna = Trenutna(prebrana.avtor, prebrana.naslov,
                           napredek, strani, self)
        self.odstrani_prebrano(prebrana)
        self.trenutne.append(ponovna)
        self._iskalnik_trenutnih[(prebrana.avtor, prebrana.naslov)] = ponovna

    def odstrani_trenutno(self, trenutna):
        if len(self.trenutne) == 0:
            raise ValueError('Trenutno ne berete nobene knjige!')
        self.trenutne.remove(trenutna)
        self.pri_brisanju_trenutnih(trenutna.avtor, trenutna.naslov)

    def direktno_prebrana(self, datum, neprebrana, ocena):
        if len(self.neprebrane) == 0:
            raise ValueError('V vaši knjižnici ni nobene neprebrane knjige!')
        elif ocena == '':
            raise ValueError('Niste vnesli vseh zahtevanih podatkov!')
        direktna = Prebrana(datum, neprebrana.avtor,
                            neprebrana.naslov, ocena, self)
        self.prebrane.append(direktna)
        self._kategorije_prebranih[direktna] = []
        self.odstrani_neprebrano(neprebrana)
        self._iskalnik_prebranih[(
            neprebrana.avtor, neprebrana.naslov)] = direktna
        return direktna

    def dodaj_prebrano(self, datum, avtor, naslov, ocena):
        if avtor == '' or avtor == ', ' or naslov == '' or ocena == '':
            raise ValueError('Niste vnesli vseh zahtevanih podatkov!')
        dodana = Prebrana(datum, avtor, naslov, ocena, self)
        self.preveri_obstoj(avtor, naslov)
        self.prebrane.append(dodana)
        self._iskalnik_prebranih[(avtor, naslov)] = dodana
        self._kategorije_prebranih[dodana] = []
        return dodana

    def odstrani_prebrano(self, prebrana):
        if len(self.prebrane) == 0:
            raise ValueError('V vaši knjižnici ni nobene prebrane knjige!')
        seznam = []
        for kategorija in self._kategorije_prebranih[prebrana]:
            seznam.append(kategorija)
        for kategorija in seznam:
            self.iz_kategorije(kategorija, prebrana)
        del self._kategorije_prebranih[prebrana]
        self.pri_brisanju_prebranih(prebrana.avtor, prebrana.naslov)
        self.prebrane.remove(prebrana)

    def poisci_neprebrano(self, vrednost):
        return self._iskalnik_neprebranih[vrednost]

    def poisci_trenutno(self, vrednost):
        return self._iskalnik_trenutnih[vrednost]

    def poisci_prebrano(self, vrednost):
        return self._iskalnik_prebranih[vrednost]

    def poisci_kategorijo(self, ime):
        return self._iskalnik_kategorij[ime]

    def kategorije_prebrane(self, prebrana):
        yield from self._kategorije_prebranih[prebrana]

    def nova_kategorija(self, ime):
        if ime in self._iskalnik_kategorij:
            raise ValueError('Kategorija s tem imenom že obstaja!')
        elif ime == '':
            raise ValueError('Niste vnesli vseh zahtevanih podatkov!')
        knjige = []
        kategorija = Kategorija(ime, knjige, self)
        self.kategorije.append(kategorija)
        self._iskalnik_kategorij[ime] = kategorija
        return kategorija

    def v_kategorijo(self, kategorija, prebrana):
        if prebrana in kategorija.knjige:
            raise ValueError('Ta knjiga je že v tej kategoriji!')
        seznam = []
        for knjiga in kategorija.knjige:
            seznam.append(knjiga)
        seznam.append(prebrana)
        nova = Kategorija(kategorija.ime, seznam, self)
        self.odstrani_kategorijo(kategorija)
        self.kategorije.append(nova)
        self._iskalnik_kategorij[nova.ime] = nova
        for knjiga in nova.knjige:
            self._kategorije_prebranih[knjiga].append(nova)
        return nova

    def iz_kategorije(self, kategorija, prebrana):
        if self.kategorije == 0:
            raise ValueError(f'V kategoriji "{kategorija}" ni nobene knjige!')
        if prebrana not in kategorija.knjige:
            raise ValueError(f'Te knjige ni v kategoriji "{kategorija}"!')
        seznam = []
        for knjiga in kategorija.knjige:
            if knjiga != prebrana:
                seznam.append(knjiga)
        nova = Kategorija(kategorija.ime, seznam, self)
        self.odstrani_kategorijo(kategorija)
        self.kategorije.append(nova)
        self._iskalnik_kategorij[kategorija.ime] = nova
        for knjiga in nova.knjige:
            self._kategorije_prebranih[knjiga].append(nova)
        return nova

    def odstrani_kategorijo(self, kategorija):
        if len(self.kategorije) == 0:
            raise ValueError(
                'Ustvarili niste še nobene kategorije prebranih knjig!')
        for knjiga in kategorija.knjige:
            self._kategorije_prebranih[knjiga].remove(kategorija)
        self.kategorije.remove(kategorija)
        del self._iskalnik_kategorij[kategorija.ime]

    def __str__(self):
        return f'Neprebrane knjige: {self.neprebrane}, trenutna branja: {self.trenutne}, prebrane knjige: {self.prebrane}, kategorije: {self.kategorije}'

    def slovar_knjig(self):
        return {
            'neprebrane knjige': [{
                'avtor': neprebrana.avtor,
                'naslov': neprebrana.naslov,
            } for neprebrana in self.neprebrane],
            'trenutna branja': [{
                'avtor': trenutna.avtor,
                'naslov': trenutna.naslov,
                'napredek': trenutna.napredek,
                'strani': trenutna.strani,
            } for trenutna in self.trenutne],
            'prebrane knjige': [{
                'datum': str(prebrana.datum),
                'avtor': prebrana.avtor,
                'naslov': prebrana.naslov,
                'ocena': prebrana.ocena,
            } for prebrana in self.prebrane],
            'kategorije': [{
                'ime': kategorija.ime,
                'knjige': [{
                    'avtor': knjiga.avtor,
                    'naslov': knjiga.naslov,
                } for knjiga in kategorija.knjige],
            } for kategorija in self.kategorije]
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
                prebrana['datum'], prebrana['avtor'], prebrana['naslov'], prebrana['ocena'])
        for kategorija in slovar_knjig['kategorije']:
            nova_kategorija = knjigozer.nova_kategorija(kategorija['ime'])
            for knjiga in kategorija['knjige']:
                prava = knjigozer._iskalnik_prebranih[(
                    knjiga['avtor'], knjiga['naslov'])]
                knjigozer.v_kategorijo(nova_kategorija, prava)
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

    def __init__(self, avtor, naslov, knjigozer):
        self.avtor = avtor
        self.naslov = naslov
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

    def __init__(self, avtor, naslov, napredek, strani, knjigozer):
        self.avtor = avtor
        self.naslov = naslov
        self.napredek = napredek
        self.strani = strani
        self.knjigozer = knjigozer

    def __repr__(self):
        return f'{self}'

    def __str__(self):
        return f'{self.avtor}: {self.naslov}, stran {self.napredek} od {self.strani}'

    def __lt__(self, other):
        if self.avtor == other.avtor:
            return self.naslov < other.naslov
        else:
            return self.avtor < other.avtor


class Prebrana:

    def __init__(self, datum, avtor, naslov, ocena, knjigozer):
        self.datum = datum
        self.avtor = avtor
        self.naslov = naslov
        self.ocena = ocena
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

    def kategorije(self):
        yield from self.knjigozer.kategorije_prebrane(self)


class Kategorija:

    def __init__(self, ime, knjige, knjigozer):
        self.ime = ime
        self.knjige = knjige
        self.knjigozer = knjigozer

    def __repr__(self):
        return f'{self}'

    def __str__(self):
        return f'{self.ime}'

    def __lt__(self, other):
        return self.ime < other.ime
