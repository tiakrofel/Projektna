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

def izbira(moznosti):
    for zaporedna_st, besedilo in enumerate(moznosti, 1):
        print(f'{zaporedna_st}) {besedilo}')
    while True:
        izbrana_moznost = stevilcni_vnos('> ')
        if 1 <= izbrana_moznost <= len(moznosti):
            return moznosti[izbrana_moznost - 1]
        else:
            print(f'Vneseno število mora biti število med 1 in {len(moznosti)}.')


def moznosti_uporabnika():
    while True: 
        print('''
        Izberi eno izmed možnosti za urejanje in ogled osebne knjižnice:
        1) ogled trenutnih branj
        2) posodobitev trenutnega branja
        3) urejanje neprebranih knjig
        4) urejanje prebranih knjig
        5) ogled knjig v osebni knjižnici
        6) izhod iz programa
        ''')
        izbrana_moznost = input('> ')
        if izbrana_moznost == '1':
            for trenutna in knjigozer.trenutne:
                print(trenutna)
        elif izbrana_moznost == '2':
            posodobi_branje()
        elif izbrana_moznost == '3':
            uredi_neprebrane()
        elif izbrana_moznost == '4':
            uredi_prebrane()
        elif izbrana_moznost == '5':
            ogled_knjig()
        elif izbrana_moznost == '6':
            print('Nasvidenje.')
            break
        else:
            print('Izbrana možnost ni na voljo.')

def posodobi_branje():
    while True:
        print('''
        Izberi eno izmed možnosti za posodobitev trenutnega branja:
        1) začetek branja ene izmed knjig s seznama neprebranih
        2) začetek branja knjige, ki ni zabeležena na nobenem seznamu knjižnice
        3) napredek v trenutnem branju
        4) dokončano trenutno branja
        5) opuščeno trenutno branje
        ''')
        izbrana_moznost = input('> ')
        if izbrana_moznost == '1':
            izberi_trenutno()
        elif izbrana_moznost == '2':
            dodaj_trenutno()
        elif izbrana_moznost == '3':
            posodobi_trenutno()
        elif izbrana_moznost == '4':
            dokoncana()
        elif izbrana_moznost == '5':
            opuscena_trenutna()
        else:
            print('Izbrana možnost ni na voljo.')


def izberi_trenutno():
    print('Izberi knjigo, ki bo šla med trenutna branja: ')
    neprebrana = izbira(knjigozer.neprebrane)
    strani = input('Vnesi število strani knjige: ')
    napredek = input('Vnesi število že prebranih strani: ')
    knjigozer.izberi_trenutno(neprebrana, strani, napredek)
    print('Knjiga je bila prenešena k trenutnim branjem.')

def dodaj_trenutno():
    avtor = input('Vnesi avtorja knjige: ')
    naslov = input('Vnesi naslov knjige: ')
    strani = input('Vnesi število strani knjige')
    napredek = input('Vnesi število že prebranih strani: ')
    knjigozer.dodaj_trenutno(avtor, naslov, strani, napredek)
    print('Knjiga je bila dodana med trenutna branja.')

def posodobi_trenutno():
    print('Izberi knjigo, v kateri bi rad zabeležil napredek: ')
    trenutna = izbira(knjigozer.trenutne)
    napredek = input('Vnesi novo število že prebranih strani: ')
    knjigozer.posodobi_trenutno(trenutna, napredek)
    print('Število prebranih strani je bilo posodobljeno.')

def dokoncana():
    datum = date.today()
    print('Izberi knjigo, ki si jo prebral do konca: ')
    trenutna = izbira(knjigozer.trenutne)
    ocena = input('Na kratko oceni knjigo: ')
    knjigozer.dokoncana(datum, trenutna, ocena)
    print('Knjiga je bila prenešena k prebranim knjigam.')

def opuscena_trenutna():
    print('Izberi knjigo, ki si jo opustil: ')
    trenutna = izbira(knjigozer.trenutne)
    knjigozer.opuscena_trenutna(trenutna)
    print('Knjiga je bila prenešena nazaj k neprebranim knjigam.')

def uredi_neprebrane():
    while True:
        print('''
        Izberi eno izmed možnosti za urejanje neprebranih knjig:
        1) dodaj novo knjigo na seznam neprebranih
        2) preveri, če je knjiga na seznamu neprebranih
        3) odstrani neprebrano knjigo iz knjižnice
        ''')
        izbrana_moznost = input('> ')
        if izbrana_moznost == '1':
            dodaj_neprebrano()
        elif izbrana_moznost == '2':
            najdi_neprebrano()
        elif izbrana_moznost == '3':
            odstrani_neprebrano()
        else:
            print('Izbrana možnost ni na voljo.')

def dodaj_neprebrano():
    avtor = input('Vnesi avtorja knjige: ')
    naslov = input('Vnesi naslov knjige: ')
    knjigozer.dodaj_neprebrano(avtor, naslov)
    print('Knjiga je bila dodana med neprebrane knjige.')

def najdi_neprebrano():
    avtor = input('Vnesi avtorja knjige: ')
    naslov = input('Vnesi naslov knjige: ')
    knjigozer.najdi_neprebrano(avtor, naslov)
    print('Ta knjiga je na seznamu neprebranih.')

def odstrani_neprebrano():
    print('Izberi neprebrano knjigo, ki jo želiš odstraniti iz knjižnice: ')
    neprebrana = izbira(knjigozer.neprebrane)
    knjigozer.odstrani_neprebrano(neprebrana)
    print('Knjiga je bila izbrisana iz knjižnice.')

def uredi_prebrane():
    while True:
        print('''
        Izberi eno izmed možnosti za urejanje neprebranih knjig:
        1) dodaj novo knjigo na seznam prebranih
        2) prenesi knjigo iz seznama neprebranih direktno k prebranim
        3) preveri, če je knjiga na seznamu prebranih
        4) odstrani prebrano knjigo iz knjižnice
        ''')
        izbrana_moznost = input('> ')
        if izbrana_moznost == '1':
            dodaj_prebrano()
        elif izbrana_moznost == '2':
            direktno_prebrana()
        elif izbrana_moznost == '3':
            najdi_prebrano()
        elif izbrana_moznost == '4':
            odstrani_prebrano()
        else:
            print('Izbrana možnost ni na voljo.')

def dodaj_prebrano():
    datum = date.today()
    avtor = input('Vnesi avtorja knjige: ')
    naslov = input('Vnesi naslov knjige: ')
    strani = input('Vnesi število strani knjige: ')
    ocena = input('Na kratko oceni knjigo: ')
    knjigozer.dodaj_prebrano(datum, avtor, naslov, strani, ocena)
    print('Knjiga je bila dodana med prebrane knjige.')

def direktno_prebrana():
    print('Izberi knjigo, ki si jo prebral: ')
    prebrana = izbira(knjigozer.neprebrane)
    datum = date.today()
    strani = input('Vnesi število strani knjige: ')
    ocena = input('Na kratko oceni knjigo')
    knjigozer.direktno_prebrana(datum, prebrana, strani, ocena)
    print('Knjiga je bila prenešena k prebranim knjigam.')

def najdi_prebrano():
    avtor = input('Vnesi avtorja knjige: ')
    naslov = input('Vnesi naslov knjige: ')
    knjigozer.najdi_prebrano(avtor, naslov)
    print('Ta knjiga je na seznamu prebranih.')

def odstrani_prebrano():
    print('Izberi prebrano knjigo, ki jo želiš odstraniti iz knjižnice: ')
    prebrana = izbira(knjigozer.prebrane)
    knjigozer.odstrani_prebrano(prebrana)
    print('Knjiga je bila izbrisana iz knjižnice.')

def ogled_knjig():
    knjigozer.ogled_knjig()


moznosti_uporabnika()







