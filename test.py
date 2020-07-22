from datetime import date
from model import Knjigozer

knjigozer = Knjigozer()

neprebrana = knjigozer.dodaj_neprebrano('Donna Tartt', 'The Goldfinch', 'DA')
trenutna = knjigozer.dodaj_trenutno(neprebrana, 110)
dokoncana = knjigozer.dokoncana(date(2019, 8, 20), trenutna, 771, '9') 

print(knjigozer)