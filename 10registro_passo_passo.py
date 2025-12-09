# 🎯 Ordine Consigliato di Scrittura
# Python deve sapere subito quali strumenti esterni useremo. Gli import vanno sempre all'inizio del file.
# 1️⃣ Prima: Import delle librerie

import json
import os
from datetime import datetime           #   datetime è sia il modulo che la classe

# 2️⃣ Secondo: Costanti e strutture dati globali
# Definire la struttura dati all'inizio è come preparare i contenitori prima di cucinare. 

# File di persistenza
DATA_FILE = "studenti_data.json"

# Struttura dati globale
database = {
    "studenti": {},  # {matricola: {nome, cognome, email, valutazioni: []}}
    "compiti": {}    # {id_compito: {titolo, descrizione, data_creazione}}
}


def carica_dati():
    """Carica i dati dal file JSON"""
    global database
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                database = json.load(f)
            print(f"✅ Dati caricati con successo ({len(database['studenti'])} studenti, {len(database['compiti'])} compiti)")
        except Exception as e:
            print(f"⚠️ Errore nel caricamento: {e}")
    else:
        print("ℹ️ Nessun file dati trovato, inizializzazione nuovo database")


def salva_dati():
    """Salva i dati nel file JSON"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=2, ensure_ascii=False)    # Scrive il dizionario nel file
        print("💾 Dati salvati con successo")
    except Exception as e:
        print(f"❌ Errore nel salvataggio: {e}")


# 3️⃣ Terzo: Le funzioni
# ==================== GESTIONE STUDENTI ====================
#Genera una nuova matricola incrementale

def aggiungi_studente():
    """Aggiunge un nuovo studente all'anagrafe"""
    print("\n--- AGGIUNGI NUOVO STUDENTE ---")
    
    matricola = input("Numero di matricola: ").strip()
    
    if matricola in database["studenti"]:
        print("❌ Matricola già esistente!")
        return
    
    nome = input("Nome: ").strip()
    cognome = input("Cognome: ").strip()
    email = input("Email: ").strip()
    
    if not nome or not cognome or not email:
        print("❌ Tutti i campi sono obbligatori!")
        return
    
    database["studenti"][matricola] = {
        "nome": nome,
        "cognome": cognome,
        "email": email,
        "valutazioni": []
    }
    
    salva_dati()
    print(f"✅ Studente {nome} {cognome} aggiunto con successo!")


def visualizza_studenti():
    """Visualizza tutti gli studenti"""
    if not database["studenti"]:
        print("\nℹ️ Nessuno studente registrato")
        return
    
    print("\n--- ELENCO STUDENTI ---")
    for matricola, dati in database["studenti"].items():
        print(f"\n📚 Matricola: {matricola}")
        print(f"   Nome: {dati['nome']} {dati['cognome']}")
        print(f"   Email: {dati['email']}")
        print(f"   Valutazioni registrate: {len(dati['valutazioni'])}")


def elimina_studente():
    """Elimina uno studente dal sistema"""
    matricola = input("\nInserisci matricola studente da eliminare: ").strip()
    
    if matricola not in database["studenti"]:
        print("❌ Studente non trovato!")
        return
    
    studente = database["studenti"][matricola]
    conferma = input(f"Confermi eliminazione di {studente['nome']} {studente['cognome']}? (s/n): ").lower()
    
    if conferma == 's':
        del database["studenti"][matricola]
        salva_dati()
        print("✅ Studente eliminato con successo")
    else:
        print("❌ Operazione annullata")















# 4️⃣ Quarto: Menu principale e avvio del programma

def menu_principale():
    """Menu principale del programma"""
    while True:
        print("\n" + "="*40)
        print("📚 SISTEMA GESTIONE STUDENTI")
        print("="*40)
        print("1. Aggiungi studente")
        print("2. Visualizza studenti")
        print("3. Elimina studente")
        print("4. Salva e esci")
        print("="*40)
        
        scelta = input("\nScegli un'opzione: ").strip()
        
        if scelta == "1":
            aggiungi_studente()
        elif scelta == "2":
            visualizza_studenti()
        elif scelta == "3":
            elimina_studente()
        elif scelta == "4":
            salva_dati()
            print("\n👋 Arrivederci!")
            break
        else:
            print("❌ Opzione non valida!")


# 5️⃣ Quinto: Punto di ingresso del programma
if __name__ == "__main__":
    carica_dati()           # Carica i dati all'avvio
    menu_principale()       # Avvia il menu