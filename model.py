class Knjigozer:

    def __init__(self):
        self.neprebrane = []
        self.posodobitve = []
        self.prebrane = []
        self.knjiznica = {}

    def dodaj_neprebrano(self, naslov, avtor, zanr):
        if (naslov, avtor) in self.knjiznica:
            raise ValueError('Ta knjiga je že v tvoji knjižnici!')
        dodana = Neprebrana(naslov, avtor, zanr, self)
        self.neprebrane.append(dodana)
        self.knjiznica[(naslov, avtor)] = 0
        return dodana


class Neprebrana:

    def __init__(self, naslov, avtor, zanr, knjigozer):
        self.naslov = naslov
        self.avtor = avtor
        self.zanr = zanr
        self.knjigozer = knjigozer


class Posodobitev:

    def __init__(self, datum, neprebrana, strani, knjigozer):
        self.datum = datum
        self.neprebrana = neprebrana
        self.strani = strani
        self.knjigozer = knjigozer 

class Prebrana:

    def __init__(self, datum, neprebrana, strani, ocena, knjigozer):
        self.datum = datum
        self.neprebrana = neprebrana
        self.strani = strani
        self.ocena = ocena
        self.knjigozer = knjigozer