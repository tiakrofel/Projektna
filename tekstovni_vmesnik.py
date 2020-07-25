from datetime import date
from model import Knjigozer

knjigozer = Knjigozer()

neprebrana1 = knjigozer.dodaj_neprebrano('Tartt, Donna', 'The Goldfinch')
trenutna1 = knjigozer.izberi_trenutno(neprebrana1, 771)
dokoncana1 = knjigozer.dokoncana(date(2019, 8, 20), trenutna1, '7/7')

neprebrana2 = knjigozer.dodaj_neprebrano('Gaiman, Neil', 'The Graveyard Book')

trenutna2 = knjigozer.dodaj_trenutno('Fry, Stephen', 'Mythos', 416, 82)

dokoncana2 = knjigozer.dodaj_prebrano(
    date(2019, 7, 1), 'Miller, Madeline', 'Circe', 393, '6/7')


def krepko(niz):
    return f'\033[1m{niz}\033[0m'


def modro(niz):
    return f'\033[1;94m{niz}\033[0m'


def rdeče(niz):
    return f'\033[1;91m{niz}\033[0m'



def osnovni_podatki_knjiznice():
    print(f'Število knjig, ki ste jih že prebrali: {len(knjigozer.prebrane)}')
    print(f'Število knjig, ki jih trenutno berete: {len(knjigozer.trenutne)}')
    print(f'Število knjig, ki si jih želite prebrati: {len(knjigozer.neprebrane)}')


def uporabnikova_izbira(slovar):
    for kljuc in slovar:
        print(f'{kljuc}. {slovar[kljuc][0]}')
    while True:
        izbral = vnos_stevila('Vnesite številko pred vašo izbiro: ')
        if len(slovar) == 1 and izbral != 1:
            print('Na tem mestu lahko izberete le 1')
        elif len(slovar) == 0:
            print('Na tem seznamu ni nobenega elementa, ki bi ga lahko izbrali.')
            zacetna_stran()
        elif 1 <= izbral <= len(slovar):
            return slovar[str(izbral)][1]
        else:
            print('Izbrati morate eno izmed ponujenih možnosti.')


def izbira(seznam):
    for zaporedna_st, besedilo in enumerate(seznam, 1):
        print(f'{zaporedna_st}. {besedilo}')
    while True:
        izbrana_moznost = vnos_stevila('> ')
        if 1 <= izbrana_moznost <= len(seznam):
            return seznam[izbrana_moznost - 1]
        else:
            if len(seznam) == 0:
                print('Na tem seznamu ni še nobene knjige, ki bi jo lahko izbrali.')
            elif len(seznam) == 1:
                print(f'Ker je na tem seznamu le ena knjiga, lahko na tem mestu vnesete le {len(seznam)}')
            print(f'Vnesti je treba število med 1 in {len(seznam)}.')


def vnos_avtorja():
    while True:
        priimek = input('Vnesite priimek avtorja knjige: ')
        ime = input('Vnesite ime avtorja knjige: ')
        avtor = priimek + ', ' + ime
        return avtor


def vnos_stevila(spodbuda):
    while True:
        stevilo = input(spodbuda)
        if stevilo.isdigit():
            return int(stevilo)
        else:
            print('Vnesti bo treba številko.')


def zacetna_stran():
    print()
    print(krepko('Pozdravljeni v programu knjigožer!'))
    while True:
        osnovne_moznosti()


def osnovne_moznosti():
    print('Vaša osebna knjižnica trenutno izgleda takole:')
    print()
    osnovni_podatki_knjiznice()
    print()
    ogled_knjig()
    print()
    print('Izberite seznam, ki si ga želite podrobneje ogledati ali posodobiti.')
    slovar = {
        '1': ('neprebrane knjige', urejanje_neprebranih),
        '2': ('trenutna branja', urejanje_trenutnih),
        '3': ('prebrane knjige', urejanje_prebranih),
    }
    naslednji_korak = uporabnikova_izbira(slovar)
    naslednji_korak()


def ogled_knjig():
    knjigozer.ogled_knjig()


def urejanje_neprebranih():
    print(krepko('Vse vaše neprebrane knjige:'))
    knjigozer.ogled_neprebranih()
    print()
    print()
    while True:
        print(krepko('Vaše možnosti urejanja neprebranih knjig:'))
        print()
        slovar = {
            '1': ('dodajte novo knjigo na seznam neprebranih', dodaj_neprebrano),
            '2': ('izbrišite neprebrano knjigo iz knjižnice', odstrani_neprebrano),
            '3': ('vrnitev nazaj na začetni meni osebne knjižnice', osnovne_moznosti),
        }
        izbira = uporabnikova_izbira(slovar)
        izbira()


def dodaj_neprebrano():
    avtor = vnos_avtorja()
    naslov = input('Vnesite naslov knjige: ')
    knjigozer.dodaj_neprebrano(avtor, naslov)
    print('Knjiga je bila dodana med neprebrane knjige.')


def odstrani_neprebrano():
    print('Izberi neprebrano knjigo, ki jo želiš odstraniti iz knjižnice: ')
    neprebrana = izbira(knjigozer.neprebrane)
    knjigozer.odstrani_neprebrano(neprebrana)
    print('Knjiga je bila izbrisana iz knjižnice.')


def urejanje_trenutnih():
    print(krepko('Vsa vaša trenutna branja:'))
    knjigozer.ogled_trenutnih()
    print()
    print()
    while True:
        print(krepko('Vaše možnosti urejanja trenutnih branj:'))
        print()
        slovar = {
            '1': ('med trenutna branja dodajte eno izmed vaših neprebranih knjig', izberi_trenutno),
            '2': ('med trenutna branja dodajte eno izmed knjig, ki še ni zabeležena v vaši knjižnici', dodaj_trenutno),
            '3': ('zabeležite napredek v enem izmed trenutnih branj', posodobi_trenutno),
            '4': ('premaknite eno izmed trenutnih branj med prebrane knjige', dokoncana),
            '5': ('premaknite eno izmed trenutnih branj nazaj med neprebrane knjige', opuscena_trenutna),
            '6': ('vrnitev nazaj na začetni meni osebne knjižnice', osnovne_moznosti),
        }
        izbira = uporabnikova_izbira(slovar)
        izbira()


def izberi_trenutno():
    print('Izberite knjigo, ki jo želite označiti kot trenutno brano: ')
    neprebrana = izbira(knjigozer.neprebrane)
    strani = vnos_stevila('Vnesite število strani knjige: ')
    napredek = vnos_stevila('Vnesite število že prebranih strani: ')
    knjigozer.izberi_trenutno(neprebrana, strani, napredek)
    print('Knjiga je bila prenešena k trenutnim branjem.')


def dodaj_trenutno():
    avtor = vnos_avtorja()
    naslov = input('Vnesite naslov knjige: ')
    strani = vnos_stevila('Vnesite število strani knjige: ')
    napredek = vnos_stevila('Vnesite število že prebranih strani: ')
    knjigozer.dodaj_trenutno(avtor, naslov, strani, napredek)
    print('Knjiga je bila dodana med trenutna branja.')


def posodobi_trenutno():
    print('Izberite knjigo, v kateri bi rad zabeležil napredek: ')
    trenutna = izbira(knjigozer.trenutne)
    napredek = vnos_stevila('Vnesite novo število že prebranih strani: ')
    knjigozer.posodobi_trenutno(trenutna, napredek)
    print('Število prebranih strani je bilo posodobljeno.')


def dokoncana():
    datum = date.today()
    print('Izberite knjigo, ki ste jo prebrali do konca: ')
    trenutna = izbira(knjigozer.trenutne)
    ocena = input('Na kratko ocenite knjigo: ')
    knjigozer.dokoncana(datum, trenutna, ocena)
    print('Knjiga je bila prenešena k prebranim knjigam.')


def opuscena_trenutna():
    print('Izberite knjigo, ki si jo opustil: ')
    trenutna = izbira(knjigozer.trenutne)
    knjigozer.opuscena_trenutna(trenutna)
    print('Knjiga je bila prenešena nazaj k neprebranim knjigam.')


def urejanje_prebranih():
    print(krepko('Vse vaše prebrane knjige:'))
    knjigozer.ogled_prebranih()
    print()
    print()
    while True:
        print(krepko('Vaše možnosti urejanja prebranih knjig:'))
        print()
        slovar = {
            '1': ('dodajte novo knjigo na seznam prebranih', dodaj_prebrano),
            '2': ('dodajte neprebrano knjigo na seznam prebranih', direktno_prebrana),
            '3': ('izbrišite prebrano knjigo iz knjižnice', odstrani_prebrano),
            '4': ('oglejte si vaše kategorije prebranih knjig in jih uredite', urejanje_kategorij),
            '5': ('vrnitev nazaj na začetni meni osebne knjižnice', osnovne_moznosti),
        }
        izbira = uporabnikova_izbira(slovar)
        izbira()


def dodaj_prebrano():
    datum = date.today()
    avtor = vnos_avtorja()
    naslov = input('Vnesite naslov knjige: ')
    strani = vnos_stevila('Vnesite število strani knjige: ')
    ocena = input('Na kratko ocenite knjigo: ')
    knjigozer.dodaj_prebrano(datum, avtor, naslov, strani, ocena)
    print('Knjiga je bila dodana med prebrane knjige.')


def direktno_prebrana():
    print('Izberite knjigo, ki ste jo prebrali: ')
    prebrana = izbira(knjigozer.neprebrane)
    datum = date.today()
    strani = vnos_stevila('Vnesite število strani knjige: ')
    ocena = input('Na kratko ocenite knjigo: ')
    knjigozer.direktno_prebrana(datum, prebrana, strani, ocena)
    print('Knjiga je bila prenešena k prebranim knjigam.')


def odstrani_prebrano():
    print('Izberite prebrano knjigo, ki jo želite izbrisati iz knjižnice: ')
    prebrana = izbira(knjigozer.prebrane)
    knjigozer.odstrani_prebrano(prebrana)
    print('Knjiga je bila izbrisana iz knjižnice.')


def urejanje_kategorij():
    while True:
        print(krepko('Vaše možnosti urejanja kategorij prebranih knjig:'))
        print()
        slovar = {
            '1': ('oglejte si vse vaše kategorije prebranih knjig', ogled_kategorij),
            '1': ('oglejte si prebrane knjige v določeni kategoriji', ogled_knjig_kategorije),
            '2': ('dodajte novo kategorijo prebranih knjig', nova_kategorija),
            '3': ('dodajte prebrano knjigo v eno izmed kategorij', v_kategorijo),
            '4': ('oglejte si vaše kategorije prebranih knjig in jih uredite', ogled_kategorij),
            '5': ('vrnitev nazaj na začetni meni osebne knjižnice', osnovne_moznosti),
        }
        izbira = uporabnikova_izbira(slovar)
        izbira()


def ogled_knjig_kategorije():
    kategorija = input('Vnesite ime kategorije, ki si jo želite ogledati: ')
    if len(knjigozer._kategorije_prebranih[kategorija]) < 1:
        print('V to kategorijo niste dodali še nobene knjige.')
    knjigozer.ogled_knjig_kategorije(kategorija)


def nova_kategorija():
    kategorija = input('Vnesite ime vaše nove kategorije: ')
    knjigozer.nova_kategorija(kategorija)


def v_kategorijo():
    kategorija = input('Vnesite ime kategorije, v katero želite dodati knjigo: ')
    prebrana = izbira(knjigozer.prebrane)
    knjigozer.v_kategorijo(kategorija, prebrana)
    print(f'Knjiga je bila dodana v kategorijo {kategorija}')


def ogled_kategorij():
    if len(knjigozer._kategorije_prebranih) < 1:
        print('Ustvarili niste še nobene kategorije prebranih knjig.')
    else:
        knjigozer.ogled_kategorij()


zacetna_stran()
