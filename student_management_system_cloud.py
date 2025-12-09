import json
import os
from datetime import datetime

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
            json.dump(database, f, indent=2, ensure_ascii=False)
        print("💾 Dati salvati con successo")
    except Exception as e:
        print(f"❌ Errore nel salvataggio: {e}")


# ==================== GESTIONE STUDENTI ====================

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


# ==================== GESTIONE COMPITI ====================

def crea_compito():
    """Crea un nuovo compito"""
    print("\n--- CREA NUOVO COMPITO ---")
    
    id_compito = input("ID compito (es. C001): ").strip()
    
    if id_compito in database["compiti"]:
        print("❌ ID compito già esistente!")
        return
    
    titolo = input("Titolo compito: ").strip()
    descrizione = input("Descrizione: ").strip()
    
    if not titolo:
        print("❌ Il titolo è obbligatorio!")
        return
    
    database["compiti"][id_compito] = {
        "titolo": titolo,
        "descrizione": descrizione,
        "data_creazione": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    salva_dati()
    print(f"✅ Compito '{titolo}' creato con successo!")


def visualizza_compiti():
    """Visualizza tutti i compiti"""
    if not database["compiti"]:
        print("\nℹ️ Nessun compito presente")
        return
    
    print("\n--- ELENCO COMPITI ---")
    for id_compito, dati in database["compiti"].items():
        print(f"\n📝 ID: {id_compito}")
        print(f"   Titolo: {dati['titolo']}")
        print(f"   Descrizione: {dati['descrizione']}")
        print(f"   Creato il: {dati['data_creazione']}")


# ==================== GESTIONE VALUTAZIONI ====================

def registra_valutazione():
    """Registra una valutazione per uno studente"""
    print("\n--- REGISTRA VALUTAZIONE ---")
    
    matricola = input("Matricola studente: ").strip()
    
    if matricola not in database["studenti"]:
        print("❌ Studente non trovato!")
        return
    
    # Mostra compiti disponibili
    if database["compiti"]:
        print("\nCompiti disponibili:")
        for id_compito, dati in database["compiti"].items():
            print(f"  - {id_compito}: {dati['titolo']}")
    
    id_compito = input("ID compito: ").strip()
    
    if id_compito not in database["compiti"]:
        print("❌ Compito non trovato!")
        return
    
    try:
        voto = float(input("Voto (0-30): ").strip())
        if voto < 0 or voto > 30:
            print("❌ Il voto deve essere tra 0 e 30!")
            return
    except ValueError:
        print("❌ Voto non valido!")
        return
    
    note = input("Note (opzionale): ").strip()
    
    valutazione = {
        "id_compito": id_compito,
        "titolo_compito": database["compiti"][id_compito]["titolo"],
        "voto": voto,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "note": note
    }
    
    database["studenti"][matricola]["valutazioni"].append(valutazione)
    salva_dati()
    
    studente = database["studenti"][matricola]
    print(f"✅ Valutazione registrata per {studente['nome']} {studente['cognome']}")


def visualizza_valutazioni_studente():
    """Visualizza tutte le valutazioni di uno studente"""
    matricola = input("\nMatricola studente: ").strip()
    
    if matricola not in database["studenti"]:
        print("❌ Studente non trovato!")
        return
    
    studente = database["studenti"][matricola]
    valutazioni = studente["valutazioni"]
    
    print(f"\n--- VALUTAZIONI DI {studente['nome']} {studente['cognome']} ---")
    
    if not valutazioni:
        print("ℹ️ Nessuna valutazione presente")
        return
    
    for i, val in enumerate(valutazioni, 1):
        print(f"\n{i}. Compito: {val['titolo_compito']} (ID: {val['id_compito']})")
        print(f"   Voto: {val['voto']}")
        print(f"   Data: {val['data']}")
        if val['note']:
            print(f"   Note: {val['note']}")


# STATISTICHE
def statistiche_studenti():
    print("\n" + "="*60)
    print("VALUTAZIONE STATISTICA PER STUDENTE".center(60))
    print("="*60)

    if not database["studenti"]:
        print("\nNessuno studente presente")
        return

    # Calcolo numero totale compiti assegnati
    num_compiti_assegnati = len(database["compiti"])

    lista_media = []

    for matricola, studente in database["studenti"].items():
        valutazioni = studente["valutazioni"]

        print(f"\n{'─'*60}")
        print(f"📚 {studente['nome']} {studente['cognome']} (Matr. {matricola})")
        print(f"{'─'*60}")

        if not valutazioni:
            print("  ⚠️  Nessuna valutazione presente")
            print(f"  📋 Compiti assegnati: {num_compiti_assegnati}")
            print(f"  ✅ Compiti completati: 0")
            print(f"  📊 Tasso completamento: 0%")
            continue

        # 1. MEDIA VOTI PER ALUNNO
        voti = [v["voto"] for v in valutazioni]
        media = sum(voti) / len(voti)
        lista_media.append(media)

        # 2. NUMERO COMPITI COMPLETATI
        num_completati = len(valutazioni)

        # 3. VOTO MASSIMO E MINIMO
        voto_min = min(voti)
        voto_max = max(voti)

        # 4. PROGRESSIONE VOTI NEL TEMPO
        # Ordina le valutazioni per data
        valutazioni_ordinate = sorted(valutazioni, key=lambda x: x["data"])
        
        print(f"\n  📊 STATISTICHE GENERALI:")
        print(f"     • Media voti: {media:.2f}/30")
        print(f"     • Voto minimo: {voto_min}")
        print(f"     • Voto massimo: {voto_max}")
        print(f"     • Compiti assegnati: {num_compiti_assegnati}")
        print(f"     • Compiti completati: {num_completati}")
        
        if num_compiti_assegnati > 0:
            percentuale = (num_completati / num_compiti_assegnati) * 100
            print(f"     • Tasso completamento: {percentuale:.1f}%")

        # PROGRESSIONE VOTI NEL TEMPO
        print(f"\n  📈 PROGRESSIONE VOTI NEL TEMPO:")
        for i, val in enumerate(valutazioni_ordinate, 1):
            # Indicatore trend
            if i > 1:
                voto_precedente = valutazioni_ordinate[i-2]["voto"]
                if val["voto"] > voto_precedente:
                    trend = "📈 ↑"
                elif val["voto"] < voto_precedente:
                    trend = "📉 ↓"
                else:
                    trend = "➡️ ="
            else:
                trend = "🆕"

            print(f"     {i}. [{val['data'][:10]}] {val['titolo_compito']}: {val['voto']}/30 {trend}")

        # Analisi trend generale
        if len(voti) >= 2:
            primi_voti = voti[:len(voti)//2]
            ultimi_voti = voti[len(voti)//2:]
            media_inizio = sum(primi_voti) / len(primi_voti)
            media_fine = sum(ultimi_voti) / len(ultimi_voti)
            
            print(f"\n  🔍 ANALISI TREND:")
            print(f"     • Media prima metà: {media_inizio:.2f}")
            print(f"     • Media seconda metà: {media_fine:.2f}")
            
            differenza = media_fine - media_inizio
            if differenza > 0:
                print(f"     • Tendenza: ✅ MIGLIORAMENTO (+{differenza:.2f})")
            elif differenza < 0:
                print(f"     • Tendenza: ⚠️ PEGGIORAMENTO ({differenza:.2f})")
            else:
                print(f"     • Tendenza: ➡️ STABILE")

    # STATISTICHE GENERALI CLASSE
    if lista_media:
        print(f"\n{'='*60}")
        print("STATISTICHE GENERALI CLASSE".center(60))
        print(f"{'='*60}")
        print(f"\n  📊 Media generale di tutti gli studenti: {sum(lista_media) / len(lista_media):.2f}/30")
        print(f"  👥 Numero studenti con valutazioni: {len(lista_media)}/{len(database['studenti'])}")
        print(f"  🏆 Media più alta: {max(lista_media):.2f}")
        print(f"  📉 Media più bassa: {min(lista_media):.2f}")
        
        # Studenti sopra/sotto la media
        media_classe = sum(lista_media) / len(lista_media)
        sopra_media = sum(1 for m in lista_media if m >= media_classe)
        sotto_media = len(lista_media) - sopra_media
        
        print(f"  ✅ Studenti sopra la media: {sopra_media}")
        print(f"  ⚠️ Studenti sotto la media: {sotto_media}")
        
    print(f"\n{'='*60}\n")

# MENU PRINCIPALE
def menu():
    carica_dati()
    
    while True:
        print("\n" + "="*50)
        print("GESTIONALE STUDENTI".center(50))
        print("="*50)
        print("\n1. Aggiungi studente")
        print("2. Visualizza studenti")
        print("3. Elimina studente")
        print("4. Crea nuovo compito")
        print("5. Visualizza compiti")
        print("6. Registra valutazione")
        print("7. Visualizza valutazioni studente")
        print("8. Statistiche studenti")
        print("0. Esci")
        
        scelta = input("\nScegli un'opzione: ").strip()
        
        if scelta == "1":
            nuovo_studente()
        elif scelta == "2":
            visualizza_studenti()
        elif scelta == "3":
            elimina_studente()
        elif scelta == "4":
            nuovo_compito()
        elif scelta == "5":
            visualizza_compiti()
        elif scelta == "6":
            registra_valutazione()
        elif scelta == "7":
            visualizza_valutazioni_studente()
        elif scelta == "8":
            statistiche_studenti()
        elif scelta == "0":
            print("\nArrivederci!")
            break
        else:
            print("\nOpzione non valida!")

if __name__ == "__main__":
    menu()