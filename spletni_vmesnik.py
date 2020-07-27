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


bottle.run(debug=True, reloader=True)