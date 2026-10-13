from termios import CR1
from operator import attrgetter

class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self._nome = nome #privati (accesso sconsigliato)
        self._responsabile = responsabile
        self.strumenti = [] #creo una lista che memorizza gli strumenti
        self.prestiti = {} #dizionario con i prestiti

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nuovo_nome):
        self._nome = nuovo_nome

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self, nuovo_responsabile):
        self._responsabile = nuovo_responsabile

    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                file.readline() #salto la prima riga (intestazione)
                for line in file: #leggo le righe una per una e le memorizzo in un dizionario, poi ogni dizionario è aggiunto alla lista di strumenti
                    riga = line.strip().split(',')
                    strumento = {'C1': riga[0],
                                 'C2': riga[1],
                                 'C3': riga[2],
                                 'C4': int(riga[3]),
                                 'C5': float(riga[4])
                    }
                    self.strumenti.append(strumento)
        except FileNotFoundError:
            print("file non trovato")

    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        strumenti_aggiunti = []
        posizione = 10 + len(strumenti_aggiunti) + 1
        strumento = {'C1': f'S{posizione}',
                     'C2': tipo,
                     'C3': marca,
                     'C4': anno_acquisto,
                     'C5': valore
                    }
        strumenti_aggiunti.append(strumento)
        self.strumenti.append(strumento)
        return strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        return sorted(self.strumenti, key=lambda s: s['C3'])


    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        strumento_trovato = None
        for s in self.strumenti:
            if s.codice == id_strumento:
                strumento_trovato = s
                break

        if not strumento_trovato:
            raise Exception(f"Errore: Lo strumento con codice {id_strumento} non esiste.") #sto verificando che lo strumento esista nel deposito

        for prestito in self.prestiti.values(): #controllo che lo strumento non sia già in prestito
            if prestito['id_strumento'] == id_strumento:
                raise Exception(f"Errore: Lo strumento {id_strumento} è già in prestito.")

        self.contatore_prestiti += 1 #numero del prestito effettuato per id
        id_prestito = f"P{self.contatore_prestiti}"

        prestito = {
            'id_prestito':  id_prestito,
            'data': data,
            'id_strumento': id_strumento,
            'cognome_allievo': cognome_allievo
        } #dizionario con il prestito

        self.prestiti[id_prestito] = prestito
        return prestito

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        if id_prestito not in self.prestiti:
            raise Exception(f"Errore: Il prestito con ID {id_prestito} non esiste.")

        del self.prestiti[id_prestito] # Rimuove il dizionario del prestito dal sistema

