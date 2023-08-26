
#la classe path è un'estensione della classe list già presente in Python
# quest'estensione si è resa necessaria in quanto un percorso di un agente è una lista di t vertici, dove il vertice
# t-esimo è il vertice occupato dall'agente all'istante t
# spesso però risulta necessario verificare la posizione dell'agente ad un istante T, con T > della lunghezza del
# percorso di un agente, per evitare di ottenere l'errore "indexerror list index out of range", il metodo getitem è
# stato sovrascritto in modo tale che:
    # se T <= lunghezza percorso
        # viene restituito il vertice occupato all'istante T
    # se T > lunghezza percorso
        # viene restituito l'ultimo vertice del percorso, ovvero il vertice sul quale l'agente si è fermato
# è stato inoltre sovrascritto anche il metodo add, in modo tale da consentire l'aggiunta simultanea di più vertici
# ad un percorso

class Path(list):
    def __getitem__(self, t):
        try:
            return super().__getitem__(t)
        except IndexError:
            return super().__getitem__(-1)

    def __add__(self, other):
        return Path([x for x in self] + [x for x in other])
