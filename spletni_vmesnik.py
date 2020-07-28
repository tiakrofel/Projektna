import bottle
from datetime import date
from model import Knjigozer

DATOTEKA_S_KNJIGAMI = 'knjiznica.json'

try:
    knjigozer = Knjigozer.nalozi_knjige(DATOTEKA_S_KNJIGAMI)
except FileNotFoundError:
    knjigozer = Knjigozer()


@bottle.get('/')
def osnovna_stran():
    return bottle.template('zacetna_stran.html', knjigozer=knjigozer)

@bottle.post('/dodaj-neprebrano/')
def dodaj_neprebrano():
    avtor = bottle.request.forms.getunicode('avtor')
    naslov = bottle.request.forms.getunicode('naslov')
    knjigozer.dodaj_neprebrano(avtor, naslov)
    bottle.redirect('/')

@bottle.post('/dodaj-trenutno/')
def dodaj_trenutno():
    avtor = bottle.request.forms.getunicode('avtor')
    naslov = bottle.request.forms.getunicode('naslov')
    strani = bottle.request.forms['strani']
    napredek = bottle.request.forms['napredek']
    knjigozer.dodaj_trenutno(avtor, naslov, strani, napredek)
    bottle.redirect('/')

@bottle.post('/dodaj-prebrano/')
def dodaj_prebrano():
    datum = date.today().strftime('%Y-%m-%d')
    avtor = bottle.request.forms.getunicode('avtor')
    naslov = bottle.request.forms.getunicode('naslov')
    strani = bottle.request.forms['strani']
    ocena = bottle.request.forms.getunicode('ocena')
    knjigozer.dodaj_prebrano(datum, avtor, naslov, strani, ocena)
    bottle.redirect('/')

@bottle.post('/izberi-trenutno/')
def izberi_trenutno():
    poklicana = bottle.request.forms['neprebrana']
    urejena = tuple(poklicana.split('; '))
    neprebrana = knjigozer.poisci_neprebrano(urejena)
    strani = bottle.request.forms.getunicode('strani')
    napredek = bottle.request.forms.getunicode('napredek')
    knjigozer.izberi_trenutno(neprebrana, strani, napredek)
    bottle.redirect('/')

@bottle.post('/dokoncana/')
def dokoncana():
    datum = date.today().strftime('%Y-%m-%d')
    poklicana = bottle.request.forms['trenutna']
    urejena = tuple(poklicana.split('; '))
    trenutna = knjigozer.poisci_trenutno(urejena)
    ocena = bottle.request.forms.getunicode('ocena')
    knjigozer.dokoncana(datum, trenutna, ocena)
    bottle.redirect('/')

@bottle.post('/odstrani-prebrano/')
def odstrani_prebrano():
    poklicana = bottle.request.forms['prebrana']
    urejena = tuple(poklicana.split('; '))
    prebrana = knjigozer.poisci_prebrano(urejena)
    knjigozer.odstrani_prebrano(prebrana)
    bottle.redirect('/')

bottle.run(debug=True, reloader=True)