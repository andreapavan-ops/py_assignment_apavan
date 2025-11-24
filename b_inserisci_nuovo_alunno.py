from datetime import datetime
import json
import os

# --- GENERA MATRICOLA ---
def genera_matricola(alunni):
    """Genera una nuova matricola incrementale."""
    numero = len(alunni) + 1
    matricola = f"MATR{numero:03d}"
    return matricola

# --- INSERISCI ALUNNO ---
def inserisci_alunno(alunni):
    """Chiede i dati dell'alunno e lo inserisce nel dizionario 'alunni'."""
    nome = input("Inserisci il nome: ").strip()
    cognome = input("Inserisci il cognome: ").strip()
    email = input("Inserisci l'email: ").strip()

    matricola = genera_matricola(alunni)

    alunni[matricola] = {
        "nome": nome,
        "cognome": cognome,
        "email": email,
        "data_creazione": datetime.now().isoformat(),
        "voti": []
    }

    print(f"✔ Alunno inserito! Matricola assegnata: {matricola}")

# --- SALVA ALUNNI nello stesso file ---
def salva_alunni(alunni, filename="10registro_alunni.json"):
    """Salva il dizionario degli alunni nello stesso file JSON."""
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(alunni, file, indent=4, ensure_ascii=False)
    print(f"💾 Dati salvati nel file: {filename}")

# --- CARICA ALUNNI ---
def carica_alunni(filename="10registro_alunni.json"):
    """Carica gli alunni dal file JSON esistente, restituisce dizionario vuoto se il file non esiste."""
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

# --- PROGRAMMA PRINCIPALE ---
alunni = carica_alunni()       # Carica alunni esistenti dal file
inserisci_alunno(alunni)       # Inserisce un nuovo alunno
salva_alunni(alunni)           # Salva tutto nello stesso file
print("\n📋 Tutti gli alunni attuali:")
for m, info in alunni.items():
    print(f"{m}: {info['nome']} {info['cognome']}, email: {info['email']}")

