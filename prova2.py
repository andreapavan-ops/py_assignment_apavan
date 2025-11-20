from datetime import datetime
import json
import os

def inserisci_alunno(filename="registro_alunni.json"):
    """Chiede i dati dell'alunno e lo inserisce nel registro JSON."""

    # Carico la lista esistente dal file, se esiste
    if os.path.exists(filename):
        with open(filename, "r") as file:
            alunni = json.load(file)
    else:
        alunni = []

    # Chiedo i dati
    nome = input("Inserisci il nome: ").strip()
    cognome = input("Inserisci il cognome: ").strip()
    email = input("Inserisci l'email: ").strip()

    # Creo il dizionario dell'alunno
    alunno = {
        "nome": nome,
        "cognome": cognome,
        "email": email,
        "data_creazione": datetime.now().isoformat(),
        "voti": []
    }

    # Aggiungo il nuovo alunno
    alunni.append(alunno)

    # Salvo la lista aggiornata nel file
    with open(filename, "w") as file:
        json.dump(alunni, file, indent=4)

    print("✔ Alunno aggiunto correttamente nel registro!")

# ---- USO ----
inserisci_alunno()  # aggiunge un nuovo alunno senza cancellare i precedenti
