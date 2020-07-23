from datetime import date
from model import Knjigozer

knjigozer = Knjigozer()

neprebrana1 = knjigozer.dodaj_neprebrano('Donna Tartt', 'The Goldfinch')
trenutna1 = knjigozer.izberi_trenutno(neprebrana1, 771)
dokoncana1 = knjigozer.dokoncana(date(2019, 8, 20), trenutna1, '7/7') 

neprebrana2 = knjigozer.dodaj_neprebrano('Neil Gaiman', 'The Graveyard Book')

trenutna2 = knjigozer.dodaj_trenutno('Stephen Fry', 'Mythos', 416, 82)

dokoncana2 = knjigozer.dodaj_prebrano(date(2019, 7, 1), 'Madeline Miller', 'Circe', 393, '6/7')


print(knjigozer)