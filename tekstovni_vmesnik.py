from datetime import date
from model import Knjigozer

LOGO = '''
88                      88  88                              88 88                                 
88                      ""  ""                               """                                                              
88                                                                                           
88   ,d8   8b,dPPYba,   88  88   ,adPPYb,d8   ,adPPYba,   888888888   ,adPPYba,  8b,dPPYba,  
88 ,a8"    88P'   `"8a  88  88  a8"    `Y88  a8"     "8a       a8P"  a8P_____88  88P'   "Y8  
8888[      88       88  88  88  8b       88  8b       d8    ,d8P'    8PP"""""""  88          
88`"Yba,   88       88  88  88  "8a,   ,d88  "8a,   ,a8"  ,d8"       "8b,   ,aa  88          
88   `Y8a  88       88  88  88   `"YbbdP"Y8   `"YbbdP"'   888888888   `"Ybbd8"'  88          
                       ,88       aa,    ,88                                                  
                     888P"        "Y8bbdP"                                                   
'''
DATOTEKA_S_KNJIGAMI = 'knjiznica.json'

try:
    knjigozer = Knjigozer.nalozi_knjige(DATOTEKA_S_KNJIGAMI)
except FileNotFoundError:
    knjigozer = Knjigozer()

def krepko(niz):
    return f'\033[1m{niz}\033[0m'


def modro(niz):
    return f'\033[1;94m{niz}\033[0m'


def rdeče(niz):
    return f'\033[1;91m{niz}\033[0m'


def osnovni_podatki_knjiznice():
    print(f'Število knjig, ki si jih želite prebrati: {len(knjigozer.neprebrane)}')
    print(f'Število knjig, ki jih trenutno berete: {len(knjigozer.trenutne)}')
    print(f'Število knjig, ki ste jih že prebrali: {len(knjigozer.prebrane)}')
    

def uporabnikova_izbira(slovar):
    for kljuc in slovar:
        print(f'{kljuc}. {slovar[kljuc][0]}')
    while True:
        izbral = vnos_stevila('Vnesite številko pred vašo izbiro: ')
        if len(slovar) == 1 and izbral != 1:
            print(rdeče('Na tem mestu lahko izberete le 1 \n'))
        elif len(slovar) == 0:
            print(
                rdeče('Na tem seznamu ni nobenega elementa, ki bi ga lahko izbrali. \n'))
            zacetna_stran()
        elif 1 <= izbral <= len(slovar):
            return slovar[str(izbral)][1]
        else:
            print(rdeče('Izbrati morate eno izmed ponujenih možnosti. \n'))


def izbira(seznam):
    for zaporedna_st, besedilo in enumerate(seznam, 1):
        print(f'{zaporedna_st}) {besedilo}')
    while True:
        izbrana_moznost = vnos_stevila('> ')
        if 1 <= izbrana_moznost <= len(seznam):
            return seznam[izbrana_moznost - 1]
        else:
            if len(seznam) == 0:
                print(rdeče('Na tem seznamu ni še nobenega objekta, ki bi ga lahko izbrali. \n'))
                break
            elif len(seznam) == 1:
                print(rdeče(
                    f'Ker je na tem seznamu le en objekt, lahko vnesete le število {len(seznam)}. \n'))
            else:
                print(rdeče(f'Vnesti je treba število med 1 in {len(seznam)}. \n'))


def vnos_avtorja():
    while True:
        priimek = input('Vnesite priimek avtorja knjige: ')
        ime = input('Vnesite ime avtorja knjige: ')
        avtor = priimek + ', ' + ime
        return avtor


def vnos_stevila(spodbuda):
    while True:
        print()
        stevilo = input(spodbuda)
        if stevilo.isdigit():
            return int(stevilo)
        else:
            print(rdeče('Vnesti bo treba številko.'))


def vnos_napredka(strani):
    print()
    while True:
        napredek = vnos_stevila('Vnesite število že prebranih strani: ')
        if int(napredek) > int(strani):
            print(rdeče('Število strani, ki ste jih že prebrali, ne more biti večje od števila vseh strani v knjigi. \n'))
        elif int(napredek) == int(strani):
            print(rdeče('Vaš napredek v knjigi je enak številu vseh strani knjige, vi pa trenutno vnašate trenutno branje in ne že prebrane knjige. \n'))
        else:
            return int(napredek)


def zacetna_stran():
    print()
    print(krepko(LOGO))
    print()
    print(modro(krepko('Pozdravljeni v programu knjigožer! \n')))
    print('Če želite iz programa, pritisnite Ctrl-C. \n')
    osnovne_moznosti()


def osnovne_moznosti():
    while True:
        try:
            print(krepko('Vaša osebna knjižnica trenutno izgleda takole: '))
            print()
            osnovni_podatki_knjiznice()
            print()
            ogled_knjig()
            print()
            print(krepko('Izberite seznam, ki si ga želite podrobneje ogledati ali posodobiti. \n'))
            slovar = {
                '1': ('neprebrane knjige', urejanje_neprebranih),
                '2': ('trenutna branja', urejanje_trenutnih),
                '3': ('prebrane knjige', urejanje_prebranih),
            }
            naslednji_korak = uporabnikova_izbira(slovar)
            print(80 * '-')
            naslednji_korak()
        except KeyboardInterrupt:
            print()
            print('Zapustili ste svojo osebno knjižnico.')
            break


def ogled_knjig():
    knjigozer.ogled_knjig()


def urejanje_neprebranih():
    print(krepko('Vse vaše neprebrane knjige:'))
    print()
    knjigozer.ogled_neprebranih()
    print()
    while True:
        try:
            print(krepko('Vaše možnosti urejanja neprebranih knjig:'))
            print()
            slovar = {
                '1': ('dodajte novo knjigo na seznam neprebranih', dodaj_neprebrano),
                '2': ('izbrišite neprebrano knjigo iz knjižnice', odstrani_neprebrano),
                '3': ('vrnitev nazaj na začetni meni osebne knjižnice', osnovne_moznosti),
            }
            izbira = uporabnikova_izbira(slovar)
            print(80 * '-')
            izbira()
            print()
            input('Pritisnite Enter za shranjevanje in vrnitev v osnovni meni...')
            knjigozer.shrani_knjige(DATOTEKA_S_KNJIGAMI)
        except ValueError as e:
            print(rdeče(e.args[0]))
            print()
        except KeyboardInterrupt:
            print()
            print('Zapustili ste svojo osebno knjižnico.')
            break


def dodaj_neprebrano():
    print()
    avtor = vnos_avtorja()
    naslov = input('Vnesite naslov knjige: ')
    knjigozer.dodaj_neprebrano(avtor, naslov)
    print(modro('Knjiga je bila dodana med neprebrane knjige. \n'))


def odstrani_neprebrano():
    print()
    print('Izberi neprebrano knjigo, ki jo želiš odstraniti iz knjižnice: ')
    neprebrana = izbira(knjigozer.neprebrane)
    knjigozer.odstrani_neprebrano(neprebrana)
    print(modro('Knjiga je bila izbrisana iz knjižnice. \n'))


def urejanje_trenutnih():
    print()
    print(krepko('Vsa vaša trenutna branja:'))
    print()
    knjigozer.ogled_trenutnih()
    print()
    while True:
        try:
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
            print(80 * '-')
            izbira()
            print()
            input('Pritisnite Enter za shranjevanje in vrnitev v osnovni meni...')
            knjigozer.shrani_knjige(DATOTEKA_S_KNJIGAMI)
        except ValueError as e:
            print(rdeče(e.args[0]))
            print()
        except KeyboardInterrupt:
            print()
            print('Zapustili ste svojo osebno knjižnico.')
            break


def izberi_trenutno():
    print()
    print('Izberite knjigo, ki jo želite označiti kot trenutno brano: ')
    neprebrana = izbira(knjigozer.neprebrane)
    strani = vnos_stevila('Vnesite število strani knjige: ')
    napredek = vnos_napredka(strani)
    knjigozer.izberi_trenutno(neprebrana, strani, napredek)
    print(modro('Knjiga je bila prenešena k trenutnim branjem. \n'))


def dodaj_trenutno():
    print()
    avtor = vnos_avtorja()
    naslov = input('Vnesite naslov knjige: ')
    strani = vnos_stevila('Vnesite število strani knjige: ')
    napredek = vnos_napredka(strani)
    knjigozer.dodaj_trenutno(avtor, naslov, strani, napredek)
    print(modro('Knjiga je bila dodana med trenutna branja. \n'))


def posodobi_trenutno():
    print()
    print('Izberite knjigo, v kateri bi rad zabeležil napredek: ')
    trenutna = izbira(knjigozer.trenutne)
    napredek = vnos_napredka(trenutna.strani)
    knjigozer.posodobi_trenutno(trenutna, napredek)
    print(modro('Število prebranih strani je bilo posodobljeno. \n'))


def dokoncana():
    print()
    datum = date.today()
    print('Izberite knjigo, ki ste jo prebrali do konca: ')
    trenutna = izbira(knjigozer.trenutne)
    ocena = input('Na kratko ocenite knjigo: ')
    knjigozer.dokoncana(datum, trenutna, ocena)
    print(modro('Knjiga je bila prenešena k prebranim knjigam. \n'))


def opuscena_trenutna():
    print()
    print('Izberite knjigo, ki ste jo opustili: ')
    trenutna = izbira(knjigozer.trenutne)
    knjigozer.opuscena_trenutna(trenutna)
    print(modro('Knjiga je bila prenešena nazaj k neprebranim knjigam. \n'))


def urejanje_prebranih():
    print()
    print(krepko('Vse vaše prebrane knjige: '))
    print()
    knjigozer.ogled_prebranih()
    print()
    while True:
        try:
            print(krepko('Vaše možnosti urejanja prebranih knjig: '))
            print()
            slovar = {
                '1': ('dodajte novo knjigo na seznam prebranih', dodaj_prebrano),
                '2': ('dodajte neprebrano knjigo na seznam prebranih', direktno_prebrana),
                '3': ('izbrišite prebrano knjigo iz knjižnice', odstrani_prebrano),
                '4': ('oglejte si vaše kategorije prebranih knjig in jih uredite', urejanje_kategorij),
                '5': ('vrnitev nazaj na začetni meni osebne knjižnice', osnovne_moznosti),
            }
            izbira = uporabnikova_izbira(slovar)
            print(80 * '-')
            izbira()
            print()
            input('Pritisnite Enter za shranjevanje in vrnitev v osnovni meni...')
            knjigozer.shrani_knjige(DATOTEKA_S_KNJIGAMI)
        except ValueError as e:
            print(rdeče(e.args[0]))
            print()
        except KeyboardInterrupt:
            print()
            print('Zapustili ste svojo osebno knjižnico.')
            break


def dodaj_prebrano():
    print()
    datum = date.today()
    avtor = vnos_avtorja()
    naslov = input('Vnesite naslov knjige: ')
    strani = vnos_stevila('Vnesite število strani knjige: ')
    ocena = input('Na kratko ocenite knjigo: ')
    knjigozer.dodaj_prebrano(datum, avtor, naslov, strani, ocena)
    print(modro('Knjiga je bila dodana med prebrane knjige. \n'))


def direktno_prebrana():
    print()
    print('Izberite knjigo, ki ste jo prebrali: ')
    prebrana = izbira(knjigozer.neprebrane)
    datum = date.today()
    strani = vnos_stevila('Vnesite število strani knjige: ')
    ocena = input('Na kratko ocenite knjigo: ')
    knjigozer.direktno_prebrana(datum, prebrana, strani, ocena)
    print(modro('Knjiga je bila prenešena k prebranim knjigam. \n'))


def odstrani_prebrano():
    print()
    print('Izberite prebrano knjigo, ki jo želite izbrisati iz knjižnice: ')
    prebrana = izbira(knjigozer.prebrane)
    knjigozer.odstrani_prebrano(prebrana)
    print(modro('Knjiga je bila izbrisana iz knjižnice. \n'))


def urejanje_kategorij():
    while True:
        try:
            print()
            print(krepko('Vaše možnosti urejanja kategorij prebranih knjig:'))
            print()
            slovar = {
                '1': ('oglejte si vse vaše kategorije prebranih knjig', ogled_kategorij),
                '2': ('oglejte si prebrane knjige v določeni kategoriji', ogled_knjig_kategorije),
                '3': ('dodajte novo kategorijo prebranih knjig', nova_kategorija),
                '4': ('dodajte prebrano knjigo v eno izmed kategorij', v_kategorijo),
                '5': ('odstranite prebrano knjigo iz ene izmed kategorij', iz_kategorije),
                '6': ('izbrišite eno izmed vaših kategorij', odstrani_kategorijo),
                '7': ('vrnitev nazaj na začetni meni osebne knjižnice', osnovne_moznosti),
            }
            izbira = uporabnikova_izbira(slovar)
            print(80 * '-')
            izbira()
            print()
            input('Pritisnite Enter za shranjevanje in vrnitev v osnovni meni...')
            knjigozer.shrani_knjige(DATOTEKA_S_KNJIGAMI)
        except ValueError as e:
            print(rdeče(e.args[0]))
            print()
        except KeyboardInterrupt:
            print()
            print('Zapustili ste svojo osebno knjižnico.')
            break


def ogled_knjig_kategorije():
    print()
    knjigozer.ogled_kategorij()
    print('Izberite kategorijo: ')
    kategorija = izbira(list(knjigozer._kategorije_prebranih.keys()))
    knjigozer.ogled_knjig_kategorije(kategorija)


def nova_kategorija():
    print()
    kategorija = input('Vnesite ime vaše nove kategorije: ')
    knjigozer.nova_kategorija(kategorija)
    print(modro(
        f'Kategorija "{kategorija}" je bila uspešno dodana med vaše kategorije prebranih knjig. \n'))


def v_kategorijo():
    print()
    print('Izberite kategorijo: ')
    kategorija = izbira(list(knjigozer._kategorije_prebranih.keys()))
    print(f'Izberite knjigo, ki jo želite dodati v kategorijo "{kategorija}": ')
    prebrana = izbira(knjigozer.prebrane)
    knjigozer.v_kategorijo(kategorija, prebrana)
    print(modro(f'Knjiga je bila dodana v kategorijo "{kategorija}". \n'))


def iz_kategorije():
    print()
    print('Izberite kategorijo: ')
    kategorija = izbira(list(knjigozer._kategorije_prebranih.keys()))
    if len(knjigozer._kategorije_prebranih[kategorija]) == 0:
        print(rdeče(f'V kategoriji "{kategorija}" ni nobene knjige!'))
    else:
        print(f'Izberite knjigo, ki jo želite izbrisati iz kategorije "{kategorija}": ')
        prebrana = izbira(knjigozer._kategorije_prebranih[kategorija])
        knjigozer.iz_kategorije(kategorija, prebrana)
        print(modro(f'Knjiga je bila izbrisana iz kategorije "{kategorija}". \n'))


def odstrani_kategorijo():
    print()
    print('Izberite kategorijo, ki jo želite izbrisati: ')
    kategorija = izbira(list(knjigozer._kategorije_prebranih.keys()))
    knjigozer.odstrani_kategorijo(kategorija)
    print(modro(f'Kategorija "{kategorija}" je bila izbrisana. \n'))


def ogled_kategorij():
    print()
    print('Vaše kategorije prebranih knjig: ')
    print()
    knjigozer.ogled_kategorij()


zacetna_stran()
