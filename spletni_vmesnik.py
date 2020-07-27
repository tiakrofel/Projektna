import bottle
from model import Knjigozer

DATOTEKA_S_KNJIGAMI = 'knjiznica.json'

try:
    knjigozer = Knjigozer.nalozi_knjige(DATOTEKA_S_KNJIGAMI)
except FileNotFoundError:
    knjigozer = Knjigozer()


@bottle.get('/')
def osnovna_stran():
    return bottle.template('zacetna_stran.html', knjigozer=knjigozer)

@bottle.post('/dodaj/')
def dodaj_neprebrano():
    knjigozer.dodaj_neprebrano(bottle.request.forms.getunicode('avtor'), bottle.request.forms.getunicode('naslov'))
    bottle.redirect('/')

bottle.run(debug=True, reloader=True)