import bottle
import os
import random
import hashlib
from datetime import date
from model import Knjigozer, Uporabnik

# DATOTEKA_S_KNJIGAMI = 'knjiznica.json'

imenik_s_podatki = 'uporabniki'
uporabniki = {}
skrivnost = 'TO JE ENA HUDA SKRIVNOST'

if not os.path.isdir(imenik_s_podatki):
    os.mkdir(imenik_s_podatki)

for ime_datoteke in os.listdir(imenik_s_podatki):
    uporabnik = Uporabnik.nalozi_knjige(os.path.join(imenik_s_podatki, ime_datoteke))
    uporabniki[uporabnik.uporabnisko_ime] = uporabnik

# try:
#     knjigozer = Knjigozer.nalozi_knjige(DATOTEKA_S_KNJIGAMI)
# except FileNotFoundError:
#     knjigozer = Knjigozer()

def trenutni_uporabnik():
    uporabnisko_ime = bottle.request.get_cookie('uporabnisko_ime', secret=skrivnost)
    if uporabnisko_ime is None:
        bottle.redirect('/prijava/')
    return uporabniki[uporabnisko_ime]

def uporabnikov_knjigozer():
    return trenutni_uporabnik().knjigozer

def shrani_trenutnega_uporabnika():
    uporabnik = trenutni_uporabnik()
    uporabnik.shrani_knjige(os.path.join('uporabniki', f'{uporabnik.uporabnisko_ime}.json'))

@bottle.get('/')
def osnovna_stran():
    bottle.redirect('/knjigozer/')

@bottle.get('/knjigozer/')
def zacetna_stran():
    knjigozer = uporabnikov_knjigozer()
    return bottle.template('zacetna_stran.html', knjigozer=knjigozer)

@bottle.get('/prijava/')
def prijava_get():
    return bottle.template('prijava.html')

@bottle.post('/prijava/')
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode('uporabnisko_ime')
    geslo = bottle.request.forms.getunicode('geslo')
    h = hashlib.blake2b()
    h.update(geslo.encode(encoding='utf-8'))
    zasifrirano_geslo = h.hexdigest()
    if uporabnisko_ime not in uporabniki:
        uporabnik = Uporabnik(
            uporabnisko_ime,
            zasifrirano_geslo,
            Knjigozer()
        )
        uporabniki[uporabnisko_ime] = uporabnik
    else:
        uporabnik = uporabniki[uporabnisko_ime]
        uporabnik.preveri_geslo(zasifrirano_geslo)
    bottle.response.set_cookie('uporabnisko_ime', uporabnik.uporabnisko_ime, path='/', secret=skrivnost)
    bottle.redirect('/knjigozer/')

@bottle.post('/odjava/')
def odjava():
    bottle.response.delete_cookie('uporabnisko_ime', path='/')
    bottle.redirect('/prijava/')


@bottle.get('/pomoc/')
def pomoc():
    knjigozer = uporabnikov_knjigozer()
    return bottle.template('pomoc_uporabniku.html', knjigozer=knjigozer)

@bottle.get('/neprebrane/')
def stran_neprebranih():
    knjigozer = uporabnikov_knjigozer()
    return bottle.template('neprebrane.html', knjigozer=knjigozer)

@bottle.get('/trenutne/')
def stran_trenutnih():
    knjigozer = uporabnikov_knjigozer()
    return bottle.template('trenutne.html', knjigozer=knjigozer)

@bottle.get('/prebrane/')
def stran_prebranih():
    knjigozer = uporabnikov_knjigozer()
    return bottle.template('prebrane.html', knjigozer=knjigozer)

@bottle.post('/dodaj-neprebrano/')
def dodaj_neprebrano():
    knjigozer = uporabnikov_knjigozer()
    avtor = bottle.request.forms.getunicode('avtor')
    naslov = bottle.request.forms.getunicode('naslov')
    knjigozer.dodaj_neprebrano(avtor, naslov)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/neprebrane/')

@bottle.post('/dodaj-trenutno/')
def dodaj_trenutno():
    knjigozer = uporabnikov_knjigozer()
    avtor = bottle.request.forms.getunicode('avtor')
    naslov = bottle.request.forms.getunicode('naslov')
    strani = int(bottle.request.forms['strani'])
    napredek = int(bottle.request.forms['napredek'])
    knjigozer.dodaj_trenutno(avtor, naslov, strani, napredek)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/trenutne/')

@bottle.post('/dodaj-prebrano/')
def dodaj_prebrano():
    knjigozer = uporabnikov_knjigozer()
    datum = date.today().strftime('%Y-%m-%d')
    avtor = bottle.request.forms.getunicode('avtor')
    naslov = bottle.request.forms.getunicode('naslov')
    strani = bottle.request.forms['strani']
    ocena = bottle.request.forms.getunicode('ocena')
    knjigozer.dodaj_prebrano(datum, avtor, naslov, strani, ocena)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/prebrane/')

@bottle.post('/izberi-trenutno/')
def izberi_trenutno():
    knjigozer = uporabnikov_knjigozer()
    poklicana = bottle.request.forms['neprebrana']
    urejena = tuple(poklicana.split('; '))
    neprebrana = knjigozer.poisci_neprebrano(urejena)
    strani = bottle.request.forms.getunicode('strani')
    napredek = bottle.request.forms.getunicode('napredek')
    knjigozer.izberi_trenutno(neprebrana, strani, napredek)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/knjigozer/')

@bottle.post('/direktno-prebrana/')
def direktno_prebrana():
    knjigozer = uporabnikov_knjigozer()
    datum = date.today().strftime('%Y-%m-%d')
    poklicana = bottle.request.forms['neprebrana']
    urejena = tuple(poklicana.split('; '))
    neprebrana = knjigozer.poisci_neprebrano(urejena)
    strani = bottle.request.forms['strani']
    ocena = bottle.request.forms.getunicode('ocena')
    knjigozer.direktno_prebrana(datum, neprebrana, strani, ocena)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/neprebrane/')

@bottle.post('/dokoncana/')
def dokoncana():
    knjigozer = uporabnikov_knjigozer()
    datum = date.today().strftime('%Y-%m-%d')
    poklicana = bottle.request.forms['trenutna']
    urejena = tuple(poklicana.split('; '))
    trenutna = knjigozer.poisci_trenutno(urejena)
    ocena = bottle.request.forms.getunicode('ocena')
    knjigozer.dokoncana(datum, trenutna, ocena)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/knjigozer/')

@bottle.post('/odstrani-neprebrano/')
def odstrani_neprebrano():
    knjigozer = uporabnikov_knjigozer()
    poklicana = bottle.request.forms['neprebrana']
    urejena = tuple(poklicana.split('; '))
    neprebrana = knjigozer.poisci_neprebrano(urejena)
    knjigozer.odstrani_neprebrano(neprebrana)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/neprebrane/')

@bottle.post('/odstrani-trenutno/')
def odstrani_trenutno():
    knjigozer = uporabnikov_knjigozer()
    poklicana = bottle.request.forms['trenutna']
    urejena = tuple(poklicana.split('; '))
    trenutna = knjigozer.poisci_trenutno(urejena)
    knjigozer.odstrani_trenutno(trenutna)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/trenutne/')

@bottle.post('/odstrani-prebrano/')
def odstrani_prebrano():
    knjigozer = uporabnikov_knjigozer()
    poklicana = bottle.request.forms['prebrana']
    urejena = tuple(poklicana.split('; '))
    prebrana = knjigozer.poisci_prebrano(urejena)
    knjigozer.odstrani_prebrano(prebrana)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/prebrane/')

@bottle.post('/posodobi-trenutno/')
def posodobi_trenutno():
    knjigozer = uporabnikov_knjigozer()
    poklicana = bottle.request.forms['trenutna']
    urejena = tuple(poklicana.split('; '))
    trenutna = knjigozer.poisci_trenutno(urejena)
    napredek = bottle.request.forms.getunicode('napredek')
    knjigozer.posodobi_trenutno(trenutna, napredek)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/knjigozer/')

@bottle.post('/opuscena-trenutna/')
def opuscena_trenutna():
    knjigozer = uporabnikov_knjigozer()
    poklicana = bottle.request.forms['trenutna']
    urejena = tuple(poklicana.split('; '))
    trenutna = knjigozer.poisci_trenutno(urejena)
    knjigozer.opuscena_trenutna(trenutna)
    shrani_trenutnega_uporabnika()
    bottle.redirect('/trenutne/')

bottle.run(debug=True, reloader=True)