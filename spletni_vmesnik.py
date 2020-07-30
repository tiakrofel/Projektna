import bottle
from datetime import date
from model import Knjigozer, Uporabnik

DATOTEKA_S_KNJIGAMI = 'knjiznica.json'

try:
    knjigozer = Knjigozer.nalozi_knjige(DATOTEKA_S_KNJIGAMI)
except FileNotFoundError:
    knjigozer = Knjigozer()


@bottle.get('/')
def osnovna_stran():
    bottle.redirect('/knjigozer/')

@bottle.get('/knjigozer/')
def zacetna_stran():
    return bottle.template('zacetna_stran.html', knjigozer=knjigozer)

@bottle.get('/prijava/')
def prijava_get():
    return bottle.template('prijava.html')

@bottle.get('/neprebrane/')
def stran_neprebranih():
    return bottle.template('neprebrane.html', knjigozer=knjigozer)

@bottle.get('/trenutne/')
def stran_trenutnih():
    return bottle.template('trenutne.html', knjigozer=knjigozer)

@bottle.get('/prebrane/')
def stran_prebranih():
    return bottle.template('prebrane.html', knjigozer=knjigozer)

@bottle.post('/dodaj-neprebrano/')
def dodaj_neprebrano():
    avtor = bottle.request.forms.getunicode('avtor')
    naslov = bottle.request.forms.getunicode('naslov')
    knjigozer.dodaj_neprebrano(avtor, naslov)
    knjigozer.shrani_knjige(DATOTEKA_S_KNJIGAMI)
    bottle.redirect('/neprebrane/')

@bottle.post('/dodaj-trenutno/')
def dodaj_trenutno():
    avtor = bottle.request.forms.getunicode('avtor')
    naslov = bottle.request.forms.getunicode('naslov')
    strani = int(bottle.request.forms['strani'])
    napredek = int(bottle.request.forms['napredek'])
    knjigozer.dodaj_trenutno(avtor, naslov, strani, napredek)
    knjigozer.shrani_knjige(DATOTEKA_S_KNJIGAMI)
    bottle.redirect('/trenutne/')

@bottle.post('/dodaj-prebrano/')
def dodaj_prebrano():
    datum = date.today().strftime('%Y-%m-%d')
    avtor = bottle.request.forms.getunicode('avtor')
    naslov = bottle.request.forms.getunicode('naslov')
    strani = bottle.request.forms['strani']
    ocena = bottle.request.forms.getunicode('ocena')
    knjigozer.dodaj_prebrano(datum, avtor, naslov, strani, ocena)
    knjigozer.shrani_knjige(DATOTEKA_S_KNJIGAMI)
    bottle.redirect('/prebrane/')

@bottle.post('/izberi-trenutno/')
def izberi_trenutno():
    poklicana = bottle.request.forms['neprebrana']
    urejena = tuple(poklicana.split('; '))
    neprebrana = knjigozer.poisci_neprebrano(urejena)
    strani = bottle.request.forms.getunicode('strani')
    napredek = bottle.request.forms.getunicode('napredek')
    knjigozer.izberi_trenutno(neprebrana, strani, napredek)
    knjigozer.shrani_knjige(DATOTEKA_S_KNJIGAMI)
    bottle.redirect('/trenutne/')

@bottle.post('/direktno-prebrana/')
def direktno_prebrana():
    datum = date.today().strftime('%Y-%m-%d')
    poklicana = bottle.request.forms['neprebrana']
    urejena = tuple(poklicana.split('; '))
    neprebrana = knjigozer.poisci_neprebrano(urejena)
    strani = bottle.request.forms['strani']
    ocena = bottle.request.forms.getunicode('ocena')
    knjigozer.direktno_prebrana(datum, neprebrana, strani, ocena)
    knjigozer.shrani_knjige(DATOTEKA_S_KNJIGAMI)
    bottle.redirect('/neprebrane/')

@bottle.post('/dokoncana/')
def dokoncana():
    datum = date.today().strftime('%Y-%m-%d')
    poklicana = bottle.request.forms['trenutna']
    urejena = tuple(poklicana.split('; '))
    trenutna = knjigozer.poisci_trenutno(urejena)
    ocena = bottle.request.forms.getunicode('ocena')
    knjigozer.dokoncana(datum, trenutna, ocena)
    knjigozer.shrani_knjige(DATOTEKA_S_KNJIGAMI)
    bottle.redirect('/trenutne/')

@bottle.post('/odstrani-neprebrano/')
def odstrani_neprebrano():
    poklicana = bottle.request.forms['neprebrana']
    urejena = tuple(poklicana.split('; '))
    neprebrana = knjigozer.poisci_neprebrano(urejena)
    knjigozer.odstrani_neprebrano(neprebrana)
    knjigozer.shrani_knjige(DATOTEKA_S_KNJIGAMI)
    bottle.redirect('/neprebrane/')

@bottle.post('/odstrani-trenutno/')
def odstrani_trenutno():
    poklicana = bottle.request.forms['trenutna']
    urejena = tuple(poklicana.split('; '))
    trenutna = knjigozer.poisci_trenutno(urejena)
    knjigozer.odstrani_trenutno(trenutna)
    knjigozer.shrani_knjige(DATOTEKA_S_KNJIGAMI)
    bottle.redirect('/trenutne/')

@bottle.post('/odstrani-prebrano/')
def odstrani_prebrano():
    poklicana = bottle.request.forms['prebrana']
    urejena = tuple(poklicana.split('; '))
    prebrana = knjigozer.poisci_prebrano(urejena)
    knjigozer.odstrani_prebrano(prebrana)
    knjigozer.shrani_knjige(DATOTEKA_S_KNJIGAMI)
    bottle.redirect('/prebrane/')

@bottle.post('/posodobi-trenutno/')
def posodobi_trenutno():
    poklicana = bottle.request.forms['trenutna']
    urejena = tuple(poklicana.split('; '))
    trenutna = knjigozer.poisci_trenutno(urejena)
    napredek = bottle.request.forms.getunicode('napredek')
    knjigozer.posodobi_trenutno(trenutna, napredek)
    knjigozer.shrani_knjige(DATOTEKA_S_KNJIGAMI)
    bottle.redirect('/trenutne/')

@bottle.post('/opuscena-trenutna/')
def opuscena_trenutna():
    poklicana = bottle.request.forms['trenutna']
    urejena = tuple(poklicana.split('; '))
    trenutna = knjigozer.poisci_trenutno(urejena)
    knjigozer.opuscena_trenutna(trenutna)
    knjigozer.shrani_knjige(DATOTEKA_S_KNJIGAMI)
    bottle.redirect('/trenutne/')

bottle.run(debug=True, reloader=True)