from datetime import datetime
import json

def inserisci_alunno(alunni):
    """Chiede i dati dell'alunno e lo inserisce nella lista 'alunni'."""

    nome = input("Inserisci il nome: ").strip()
    cognome = input("Inserisci il cognome: ").strip()
    email = input("Inserisci l'email: ").strip()

    alunno = {
        "nome": nome,
        "cognome": cognome,
        "email": email,
        "data_creazione": datetime.now().isoformat(),
        "voti": []
    }

    alunni.append(alunno)
    print("✔ Alunno inserito correttamente!")


def salva_alunni(alunni, filename="registro_alunni.json"):
    with open(filename, "a") as file:
        json.dump(alunni, file, indent=4)
    print("💾 Dati salvati nel file:", filename)


#  FUNZIONI INSERIMENTO ALUNNI E SALVA ALUNNI

alunni = []  # lista vuota

inserisci_alunno(alunni)   # chiedi i dati e aggiungi l'alunno
salva_alunni(alunni)       # salva la lista nel file JSON
