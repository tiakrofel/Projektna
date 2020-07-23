from datetime import date
from model import Knjigozer

knjigozer = Knjigozer()

neprebrana = knjigozer.dodaj_neprebrano('Donna Tartt', 'The Goldfinch', 'DA')
trenutna = knjigozer.izberi_trenutno(neprebrana, 771)
dokoncana = knjigozer.dokoncana(date(2019, 8, 20), trenutna, '7/7') 

neprebrana1 = knjigozer.dodaj_neprebrano('Neil Gaiman', 'The Graveyard Book', "Children's Books")

trenutna1 = knjigozer.dodaj_trenutno('Stephen Fry', 'Mythos', 'myths', 416, 82)

dokoncana1 = knjigozer.dodaj_prebrano(date(2019, 7, 1), 'Madeline Miller', 'Circe', 'historical fiction', 393, '6/7')


print(knjigozer)