import json
import os
from datetime import datetime
from a_gestione_anagrafica_alunni import carica_alunni, salva_alunni  # import corretto

# --- Funzione per generare un nuovo TASK ID ---
def genera_task_id(lista_compiti):
    numero = len(lista_compiti) + 1
    return f"TASK{numero:03d}"

# --- Funzione per inserire un compito ---
def inserisci_compito(lista_compiti, alunni):
    print("\n--- Inserisci nuovo compito ---")
    descrizione = input("Descrizione del compito: ").strip()

    print("\nAlunni disponibili:")
    for m, info in alunni.items():
        print(f"{m} - {info['nome']} {info['cognome']}")

    matricola = input("\nMatricola alunno: ").strip().upper()

    if matricola not in alunni:
        print("❌ Matricola non trovata!")
        return

    task_id = genera_task_id(lista_compiti)

    lista_compiti[task_id] = {
        "id": task_id,
        "descrizione": descrizione,
        "alunno_matricola": matricola,
        "stato": "assegnato",
        "data_assegnazione": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "voto": None
    }

    print(f"✔ Compito inserito! Codice assegnato: {task_id}")

# --- Salvataggio e caricamento compiti ---
def salva_compiti(lista_compiti, filename="10registro_compiti.json"):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(lista_compiti, file, indent=4, ensure_ascii=False)
    print(f"💾 Compiti salvati nel file: {filename}")

def carica_compiti(filename="10registro_compiti.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    return {}

# --- Programma principale ---
alunni = carica_alunni()
lista_compiti = carica_compiti()

# inserisci nuovo compito
inserisci_compito(lista_compiti, alunni)

# salva dati
salva_alunni(alunni)
salva_compiti(lista_compiti)

# stampa riepilogo
print("\n📚 Compiti registrati:")
for t, info in lista_compiti.items():
    print(f"{t}: {info['descrizione']} → {info['alunno_matricola']} ({info['stato']})")


