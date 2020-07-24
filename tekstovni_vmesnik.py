from datetime import date
from model import Knjigozer

knjigozer = Knjigozer()

neprebrana1 = knjigozer.dodaj_neprebrano('Donna Tartt', 'The Goldfinch')
trenutna1 = knjigozer.izberi_trenutno(neprebrana1, 771)
dokoncana1 = knjigozer.dokoncana(date(2019, 8, 20), trenutna1, '7/7') 

neprebrana2 = knjigozer.dodaj_neprebrano('Neil Gaiman', 'The Graveyard Book')

trenutna2 = knjigozer.dodaj_trenutno('Stephen Fry', 'Mythos', 416, 82)

dokoncana2 = knjigozer.dodaj_prebrano(date(2019, 7, 1), 'Madeline Miller', 'Circe', 393, '6/7')

def stevilcni_vnos(pobuda):
    while True:
        stevilka = input(pobuda)
        if stevilka.isdigit():
            return int(stevilka)
        else:
            print(f'Na tem koraku je treba vnesti število.')

def izbira(seznam):
    for zaporedna_st, besedilo in enumerate(seznam, 1):
        print(f'{zaporedna_st}. {besedilo}')
    while True:
        izbrana_moznost = stevilcni_vnos('> ')
        if 1 <= izbrana_moznost <= len(seznam):
            return seznam[izbrana_moznost - 1]
        else:
            if len(seznam) == 0:
                print('Na tem seznamu ni še nobene knjige, ki bi jo lahko izbrali.')
            elif len(seznam) == 1:
                print(f'Ker je na tem seznamu le ena knjiga, lahko na tem mestu vnesete le {len(seznam)}')
            print(f'Vnesti je treba število med 1 in {len(seznam)}.')


def moznosti_uporabnika():
    while True: 
        print('Izberite eno izmed naslednjih možnosti za urejanje osebne knjižnice: ')
        moznosti = [
            'ogled vseh knjig v osebni knjižnici',
            'ogled trenutnih branj',
            'posodobitev trenutnih branja',
            'ogled neprebranih knjig',
            'urejanje neprebranih knjig',
            'ogled prebranih knjig',
            'urejanje prebranih knjig',
            'izhod iz programa',
        ]
        izbrana_moznost = izbira(moznosti)
        if izbrana_moznost == moznosti[0]:
            ogled_knjig()
        elif izbrana_moznost == moznosti[1]:
            for trenutna in knjigozer.trenutne:
                print(trenutna)
        elif izbrana_moznost == moznosti[2]:
            posodobi_branje()
        elif izbrana_moznost == moznosti[3]:
            for neprebrana in knjigozer.neprebrane:
                print(neprebrana)
        elif izbrana_moznost == moznosti[4]:
            uredi_neprebrane()
        elif izbrana_moznost == moznosti[5]:
            for prebrana in knjigozer.prebrane:
                print(prebrana)
        elif izbrana_moznost == moznosti[6]:
            uredi_prebrane()
        elif izbrana_moznost == moznosti[7]:
            print('Nasvidenje.')
            break
        else:
            print('Izbrana možnost ni na voljo.')

def posodobi_branje():
    while True:
        print('Izberite eno izmed naslednjih možnosti za urejanje osebne knjižnice: ')
        moznosti = [
            'začetek branja ene izmed knjig s seznama neprebranih',
            'začetek branja knjige, ki ni zabeležena na nobenem seznamu knjižnice',
            'napredek v trenutnem branju',
            'dokončano trenutno branja',
            'opuščeno trenutno branje',
            'vrnitev nazaj na možnosti urejanja osebne knjižnice',
        ]
        izbrana_moznost = izbira(moznosti)
        if izbrana_moznost == moznosti[0]:
            izberi_trenutno()
        elif izbrana_moznost == moznosti[1]:
            dodaj_trenutno()
        elif izbrana_moznost == moznosti[2]:
            posodobi_trenutno()
        elif izbrana_moznost == moznosti[3]:
            dokoncana()
        elif izbrana_moznost == moznosti[4]:
            opuscena_trenutna()
        elif izbrana_moznost == moznosti[5]:
            moznosti_uporabnika()
        else:
            print('Izbrana možnost ni na voljo.')


def izberi_trenutno():
    print('Izberite knjigo, ki jo želite označiti kot trenutno brano: ')
    neprebrana = izbira(knjigozer.neprebrane)
    strani = stevilcni_vnos('Vnesite število strani knjige: ')
    napredek = stevilcni_vnos('Vnesite število že prebranih strani: ')
    knjigozer.izberi_trenutno(neprebrana, strani, napredek)
    print('Knjiga je bila prenešena k trenutnim branjem.')

def dodaj_trenutno():
    avtor = input('Vnesite avtorja knjige: ')
    naslov = input('Vnesite naslov knjige: ')
    strani = stevilcni_vnos('Vnesite število strani knjige: ')
    napredek = stevilcni_vnos('Vnesite število že prebranih strani: ')
    knjigozer.dodaj_trenutno(avtor, naslov, strani, napredek)
    print('Knjiga je bila dodana med trenutna branja.')

def posodobi_trenutno():
    print('Izberite knjigo, v kateri bi rad zabeležil napredek: ')
    trenutna = izbira(knjigozer.trenutne)
    napredek = stevilcni_vnos('Vnesite novo število že prebranih strani: ')
    knjigozer.posodobi_trenutno(trenutna, napredek)
    print('Število prebranih strani je bilo posodobljeno.')

def dokoncana():
    datum = date.today()
    print('Izberite knjigo, ki si jo prebral do konca: ')
    trenutna = izbira(knjigozer.trenutne)
    ocena = input('Na kratko ocenite knjigo: ')
    knjigozer.dokoncana(datum, trenutna, ocena)
    print('Knjiga je bila prenešena k prebranim knjigam.')

def opuscena_trenutna():
    print('Izberite knjigo, ki si jo opustil: ')
    trenutna = izbira(knjigozer.trenutne)
    knjigozer.opuscena_trenutna(trenutna)
    print('Knjiga je bila prenešena nazaj k neprebranim knjigam.')

def uredi_neprebrane():
    while True:
        print('Izberite eno izmed naslednjih možnosti za urejanje vaših neprebranih knjig: ')
        moznosti = [
            'dodajte novo knjigo na seznam neprebranih',
            'preverite, če je neka knjiga na seznamu neprebranih knjig',
            'izbrišite neprebrano knjigo iz knjižnice',
            'vrnitev nazaj na osnovni seznam možnosti urejanja osebne knjižnice',
        ]
        izbrana_moznost = izbira(moznosti)
        if izbrana_moznost == moznosti[0]:
            dodaj_neprebrano()
        elif izbrana_moznost == moznosti[1]:
            najdi_neprebrano()
        elif izbrana_moznost == moznosti[2]:
            odstrani_neprebrano()
        elif izbrana_moznost == moznosti[3]:
            moznosti_uporabnika()
        else:
            print('Izbrana možnost ni na voljo.')

def dodaj_neprebrano():
    avtor = input('Vnesite avtorja knjige: ')
    naslov = input('Vnesite naslov knjige: ')
    knjigozer.dodaj_neprebrano(avtor, naslov)
    print('Knjiga je bila dodana med neprebrane knjige.')

def najdi_neprebrano():
    avtor = input('Vnesite avtorja knjige: ')
    naslov = input('Vnesite naslov knjige: ')
    knjigozer.najdi_neprebrano(avtor, naslov)
    print('Ta knjiga je res na seznamu neprebranih.')

def odstrani_neprebrano():
    print('Izberi neprebrano knjigo, ki jo želiš odstraniti iz knjižnice: ')
    neprebrana = izbira(knjigozer.neprebrane)
    knjigozer.odstrani_neprebrano(neprebrana)
    print('Knjiga je bila izbrisana iz knjižnice.')

def uredi_prebrane():
    while True:
        print('Izberite eno izmed naslednjih možnosti za urejanje vaših neprebranih knjig: ')
        moznosti = [
            'dodajte novo knjigo na seznam prebranih',
            'prenesite knjigo iz seznama neprebranih direktno k prebranim',
            'preverite, če je neka knjiga na seznamu prebranih knjig',
            'izbrišite prebrano knjigo iz knjižnice',
            'vrnitev nazaj na osnovni seznam možnosti urejanja osebne knjižnice',
        ]
        izbrana_moznost = izbira(moznosti)
        if izbrana_moznost == moznosti[0]:
            dodaj_prebrano()
        elif izbrana_moznost == moznosti[1]:
            direktno_prebrana()
        elif izbrana_moznost == moznosti[2]:
            najdi_prebrano()
        elif izbrana_moznost == moznosti[3]:
            odstrani_prebrano()
        elif izbrana_moznost == moznosti[4]:
            moznosti_uporabnika()
        else:
            print('Izbrana možnost ni na voljo.')

def dodaj_prebrano():
    datum = date.today()
    avtor = input('Vnesite avtorja knjige: ')
    naslov = input('Vnesite naslov knjige: ')
    strani = stevilcni_vnos('Vnesite število strani knjige: ')
    ocena = input('Na kratko ocenite knjigo: ')
    knjigozer.dodaj_prebrano(datum, avtor, naslov, strani, ocena)
    print('Knjiga je bila dodana med prebrane knjige.')

def direktno_prebrana():
    print('Izberite knjigo, ki ste jo prebrali: ')
    prebrana = izbira(knjigozer.neprebrane)
    datum = date.today()
    strani = stevilcni_vnos('Vnesite število strani knjige: ')
    ocena = input('Na kratko ocenite knjigo: ')
    knjigozer.direktno_prebrana(datum, prebrana, strani, ocena)
    print('Knjiga je bila prenešena k prebranim knjigam.')

def najdi_prebrano():
    avtor = input('Vnesite avtorja knjige: ')
    naslov = input('Vnesite naslov knjige: ')
    knjigozer.najdi_prebrano(avtor, naslov)
    print('Ta knjiga je res na seznamu prebranih.')

def odstrani_prebrano():
    print('Izberite prebrano knjigo, ki jo želite izbrisati iz knjižnice: ')
    prebrana = izbira(knjigozer.prebrane)
    knjigozer.odstrani_prebrano(prebrana)
    print('Knjiga je bila izbrisana iz knjižnice.')

def ogled_knjig():
    knjigozer.ogled_knjig()


moznosti_uporabnika()







