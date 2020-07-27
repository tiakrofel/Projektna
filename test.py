import json
from datetime import date
from model import Knjigozer

knjigozer = Knjigozer()

neprebrana1 = knjigozer.dodaj_neprebrano('Tartt, Donna', 'The Goldfinch')
trenutna1 = knjigozer.izberi_trenutno(neprebrana1, 771)
dokoncana1 = knjigozer.dokoncana(date(2019, 8, 20), trenutna1, '7/7') 

neprebrana2 = knjigozer.dodaj_neprebrano('Gaiman, Neil', 'The Graveyard Book')

trenutna2 = knjigozer.dodaj_trenutno('Fry, Stephen', 'Mythos', 416, 82)

dokoncana2 = knjigozer.dodaj_prebrano(date(2019, 7, 1), 'Miller, Madeline', 'Circe', 393, '6/7')

knjigozer.nova_kategorija('Najljubše')
knjigozer.v_kategorijo('Najljubše', dokoncana1)
knjigozer.v_kategorijo('Najljubše', dokoncana2)


knjiznica = knjigozer.slovar_knjig()
with open('knjiznica.json', 'w') as datoteka:
    json.dump(knjiznica, datoteka, ensure_ascii=False, indent=4)