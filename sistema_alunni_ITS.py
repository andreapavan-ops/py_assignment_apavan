# LIBRERIE
import json
import os
import re
from datetime import datetime

# FILE DI PERSISTENZA: LE MIE COSTANTI DOVE SALVO I DATI (IN MAIUSCOLO)
FILE_ALUNNI = "dati_alunni.json"
FILE_COMPITI = "lista_compiti.json"

# STRUTTURE DATI: VARIABILI GLOBALI (che cntengono dizionari vuoti)
lista_alunni = {}
lista_compiti = {}

# ============ FUNZIONI DI PERSISTENZA (di salvataggio) ===============

# FUNZIONE CARICA DATI (dai file jeson)
def carica_dati():
    """global: modifica queste variabili globali, non crearne di nuove locali"""
    global lista_alunni, lista_compiti

    """controllo esistenza file, catturo gli errori senza far creshare il programma"""
    if os.path.exists(FILE_ALUNNI):
        try:
            with open(FILE_ALUNNI, 'r', encoding='utf-8') as f:
                lista_alunni = json.load(f)
        except Exception as e:
            print(f"Errore caricamento alunni: {e}")

    if os.path.exists(FILE_COMPITI):
        try:
            with open(FILE_COMPITI, 'r', encoding='utf-8') as f:
                lista_compiti = json.load(f)
        except Exception as e:
            print(f"Errore caricamento compiti: {e}")

    print(f"Dati caricati: {len(lista_alunni)} alunni, {len(lista_compiti)} compiti")

# FUNZIONE SALVA ALUNNI (funzione opposta: Scrive il dizionario lista_alunni nel file json)
def salva_alunni():
    try:
        with open(FILE_ALUNNI, 'w', encoding='utf-8') as f:
            json.dump(lista_alunni, f, indent=4, ensure_ascii=False)
        print("Alunni salvati")
    except Exception as e:
        print(f"Errore salvataggio alunni: {e}")

# FUNZIONE SALVA COMPITI (Scrive il dizionario lista_compiti nel file json)
def salva_compiti():
    try:
        with open(FILE_COMPITI, 'w', encoding='utf-8') as f:
            json.dump(lista_compiti, f, indent=4, ensure_ascii=False)
        print("Compiti salvati")
    except Exception as e:
        print(f"Errore salvataggio compiti: {e}")

# ======== FUNZIONI DI VALIDAZIONE e GENERATORI ID ==========

def valida_email(email):
    """Verifica che l'email sia in un formato valido"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def genera_matricola():
    """Genera una nuova matricola incrementale MAT001, MAT002..."""
    numero = len(lista_alunni) + 1
    matricola = f"MAT{numero:03d}"
    # Se esiste già, incrementa finché non trova una libera
    while matricola in lista_alunni:
        numero += 1
        matricola = f"MAT{numero:03d}"
    return matricola


def genera_task_id():
    """Genera un nuovo ID compito incrementale TASK001, TASK002..."""
    numero = len(lista_compiti) + 1
    task_id = f"TASK{numero:03d}"
    # Se esiste già, incrementa finché non trova uno libero
    while task_id in lista_compiti:
        numero += 1
        task_id = f"TASK{numero:03d}"
    return task_id


# ==================== GESTIONE ALUNNI ====================
    """Dopo le funzioni di utilità (validazione e generazione ID). È una delle funzioni che l'utente può chiamare dal menu.Permette all'utente di aggiungere un nuovo studente al sistema, raccogliendo i dati da tastiera e salvandoli."""

def inserisci_alunno():
    """Inserisce un nuovo alunno"""
    print("\n--- INSERISCI NUOVO ALUNNO ---")

    nome = input("Nome: ").strip()
    cognome = input("Cognome: ").strip()
    if not nome or not cognome:
        print("Nome e cognome sono obbligatori!")
        return

    # Ciclo per inserimento email valida
    while True:
        email = input("Email: ").strip()
        if not email:
            print("L'email è obbligatoria!")
            continue
        if valida_email(email):
            break
        else:
            print("Email non valida! Formato corretto: esempio@dominio.com")
            print("Riprova oppure digita 'esci' per annullare.")
            if email.lower() == 'esci':
                print("Inserimento annullato.")
                return

    matricola = genera_matricola()
    data_corrente = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lista_alunni[matricola] = {
        "nome": nome,
        "cognome": cognome,
        "email": email,
        "matricola": matricola,
        "data_creazione": data_corrente,
        "data_modifica": data_corrente,
        "archiviato": False
    }

    salva_alunni()
    print(f"✅ Alunno {nome} {cognome} inserito con matricola: {matricola}")

# FUNZIONE di visualizzazione chiamabile dal menu.
"""Mostra a schermo l'elenco di tutti gli alunni non archiviati (cioè quelli "attivi") archiviato = False"""
def visualizza_alunni():
    """Visualizza tutti gli alunni attivi"""
    alunni_attivi = {}
    for k, v in lista_alunni.items():
        if not v.get('archiviato', False):
            alunni_attivi[k] = v

    if not alunni_attivi:
        print("\n⚠️  Nessun alunno attivo registrato")
        return

    print("\n--- 📋 ELENCO ALUNNI ATTIVI ---")
    for matricola, dati in alunni_attivi.items():
        print(f"\n📌 Matricola: {matricola}")
        print(f"  👤 Nome: {dati['nome']} {dati['cognome']}")
        print(f"  📧 Email: {dati['email']}")
        print(f"  📅 Creato: {dati['data_creazione']}")
        print(f"  🔄 Modificato: {dati['data_modifica']}")


def modifica_alunno():
    """Modifica i dati di un alunno esistente"""
    matricola = input("\nMatricola alunno da modificare: ").strip().upper()

    if matricola not in lista_alunni:
        print("Alunno non trovato!")
        return

    alunno = lista_alunni[matricola]
    print(f"\nDati attuali: {alunno['nome']} {alunno['cognome']} - {alunno['email']}")

    nome = input(f"Nuovo nome (invio per mantenere '{alunno['nome']}'): ").strip()
    cognome = input(f"Nuovo cognome (invio per mantenere '{alunno['cognome']}'): ").strip()
    email = input(f"Nuova email (invio per mantenere '{alunno['email']}'): ").strip()

    if nome:
        alunno['nome'] = nome
    if cognome:
        alunno['cognome'] = cognome
    if email:
        if not valida_email(email):
            print("Email non valida! Modifica annullata.")
            return
        alunno['email'] = email

    alunno['data_modifica'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    salva_alunni()
    print("Alunno modificato")

# FUNZIONE per aggiornare i dati di un alunno.
""" È una funzione CRUD (Create, Read, Update, Delete)"""
def elimina_alunno():
    """Archivia un alunno (cancellazione soft)"""
    matricola = input("\nMatricola alunno da archiviare: ").strip().upper()

    if matricola not in lista_alunni:
        print("❌ Alunno non trovato!")
        return

    alunno = lista_alunni[matricola]

    if alunno.get('archiviato', False):
        print("⚠️  Questo alunno è già archiviato!")
        return

    print(f"\n👤 Dati alunno: {alunno['nome']} {alunno['cognome']}")

    conferma = input("Sei sicuro di voler archiviare questo alunno? (s/n): ").lower()

    if conferma == 's':
        alunno['archiviato'] = True
        alunno['data_archiviazione'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        salva_alunni()
        print("📦 Alunno archiviato con successo!")
    else:
        print("🔙 Operazione annullata")

# FUNZIONE Mostra alunni archiviati (quelli "eliminati" con soft delete).
def visualizza_archiviati():
    """Visualizza gli alunni archiviati"""
    archiviati = {k: v for k, v in lista_alunni.items() if v.get('archiviato', False)}

    if not archiviati:
        print("\n📭 Nessun alunno archiviato")
        return

    print("\n--- 📦 ALUNNI ARCHIVIATI ---")
    for matricola, dati in archiviati.items():
        print(f"\n📌 Matricola: {matricola}")
        print(f"  👤 Nome: {dati['nome']} {dati['cognome']}")
        print(f"  📧 Email: {dati['email']}")
        print(f"  📅 Archiviato il: {dati.get('data_archiviazione', 'N/A')}")

# FUNZIONE recupera un alunno archiviato, rendendolo nuovamente attivo.
def ripristina_alunno():
    archiviati = {k: v for k, v in lista_alunni.items() if v.get('archiviato', False)}

    if not archiviati:
        print("\n📭 Nessun alunno archiviato da ripristinare")
        return

    print("\n--- 📦 ALUNNI ARCHIVIATI ---")
    for matricola, dati in archiviati.items():
        print(f"  {matricola} - {dati['nome']} {dati['cognome']}")

    matricola = input("\nMatricola alunno da ripristinare: ").strip().upper()

    if matricola not in archiviati:
        print("❌ Alunno non trovato tra gli archiviati!")
        return

    lista_alunni[matricola]['archiviato'] = False
    lista_alunni[matricola]['data_modifica'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    salva_alunni()
    print(f"✅ Alunno {lista_alunni[matricola]['nome']} {lista_alunni[matricola]['cognome']} ripristinato!")


# ==================== GESTIONE COMPITI ====================

def inserisci_compito():
    """Inserisce un nuovo compito e lo assegna a un alunno"""
    print("\n--- INSERISCI NUOVO COMPITO ---")

    if not lista_alunni:
        print("Nessun alunno registrato! Inserisci prima un alunno.")
        return

    descrizione = input("Descrizione compito: ").strip()

    if not descrizione:
        print("La descrizione e' obbligatoria!")
        return

    # Mostra solo alunni attivi (non archiviati)
    alunni_attivi = {k: v for k, v in lista_alunni.items() if not v.get('archiviato', False)}

    if not alunni_attivi:
        print("Nessun alunno attivo disponibile!")
        return

    print("\nAlunni disponibili:")
    for matricola, dati in alunni_attivi.items():
        print(f"  {matricola} - {dati['nome']} {dati['cognome']}")

    alunno_matricola = input("\nMatricola alunno a cui assegnare: ").strip().upper()

    if alunno_matricola not in alunni_attivi:
        print("Matricola non trovata o alunno archiviato!")
        return

    task_id = genera_task_id()

    lista_compiti[task_id] = {
        "id": task_id,
        "descrizione": descrizione,
        "alunno_matricola": alunno_matricola,
        "stato": "assegnato",
        "data_assegnazione": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "voto": None
    }

    salva_compiti()
    alunno = lista_alunni[alunno_matricola]
    print(f"Compito {task_id} assegnato a {alunno['nome']} {alunno['cognome']}")


def visualizza_compiti():
    """Visualizza tutti i compiti"""
    if not lista_compiti:
        print("\nNessun compito registrato")
        return

    print("\n--- ELENCO COMPITI ---")
    for task_id, dati in lista_compiti.items():
        alunno = lista_alunni.get(dati['alunno_matricola'], {})
        nome_alunno = f"{alunno.get('nome', '?')} {alunno.get('cognome', '?')}"

        print(f"\nID: {task_id}")
        print(f"  Descrizione: {dati['descrizione']}")
        print(f"  Alunno: {nome_alunno} ({dati['alunno_matricola']})")
        print(f"  Stato: {dati['stato']}")
        print(f"  Data assegnazione: {dati['data_assegnazione']}")
        print(f"  Voto: {dati['voto'] if dati['voto'] is not None else 'Non valutato'}")


def valuta_compito():
    """Assegna un voto a un compito"""
    print("\n--- VALUTA COMPITO ---")

    if not lista_compiti:
        print("Nessun compito registrato")
        return

    # Mostra compiti da valutare
    print("\nCompiti disponibili:")
    for task_id, dati in lista_compiti.items():
        alunno = lista_alunni.get(dati['alunno_matricola'], {})
        nome_alunno = f"{alunno.get('nome', '?')} {alunno.get('cognome', '?')}"
        stato_voto = f"Voto: {dati['voto']}" if dati['voto'] is not None else "Non valutato"
        print(f"  {task_id} - {dati['descrizione']} ({nome_alunno}) - {stato_voto}")

    task_id = input("\nID compito da valutare: ").strip().upper()

    if task_id not in lista_compiti:
        print("Compito non trovato!")
        return

    try:
        voto = int(input("Voto (0-10): ").strip())
        if voto < 0 or voto > 10:
            print("Il voto deve essere tra 0 e 10!")
            return
    except ValueError:
        print("Voto non valido! Inserisci un numero intero.")
        return

    lista_compiti[task_id]['voto'] = voto
    lista_compiti[task_id]['stato'] = "registrato"

    salva_compiti()
    print(f"Compito {task_id} valutato con voto: {voto}")


def visualizza_compiti_alunno():
    """Visualizza i compiti di un singolo alunno"""
    matricola = input("\nMatricola alunno: ").strip().upper()

    if matricola not in lista_alunni:
        print("Alunno non trovato!")
        return

    alunno = lista_alunni[matricola]
    print(f"\n--- COMPITI DI {alunno['nome']} {alunno['cognome']} ---")

    compiti_alunno = {k: v for k, v in lista_compiti.items() if v['alunno_matricola'] == matricola}

    if not compiti_alunno:
        print("Nessun compito assegnato")
        return

    for task_id, dati in compiti_alunno.items():
        print(f"\n{task_id}: {dati['descrizione']}")
        print(f"  Stato: {dati['stato']}")
        print(f"  Voto: {dati['voto'] if dati['voto'] is not None else 'Non valutato'}")


# ==================== STATISTICHE ====================

def statistiche():
    """Mostra statistiche generali"""
    print("\n--- STATISTICHE ---")
    print(f"\nTotale alunni: {len(lista_alunni)}")
    print(f"Totale compiti: {len(lista_compiti)}")

    if not lista_compiti:
        return

    # Compiti per stato
    stati = {}
    for compito in lista_compiti.values():
        stato = compito['stato']
        stati[stato] = stati.get(stato, 0) + 1

    print("\nCompiti per stato:")
    for stato, count in stati.items():
        print(f"  {stato}: {count}")

    # Media voti
    voti = [c['voto'] for c in lista_compiti.values() if c['voto'] is not None]
    if voti:
        media = sum(voti) / len(voti)
        print(f"\nMedia voti: {media:.2f}")
        print(f"Voto minimo: {min(voti)}")
        print(f"Voto massimo: {max(voti)}")


def statistiche_studente():
    """Mostra statistiche di un singolo studente"""
    matricola = input("\nMatricola studente: ").strip().upper()

    if matricola not in lista_alunni:
        print("Studente non trovato!")
        return

    alunno = lista_alunni[matricola]
    print(f"\n--- STATISTICHE DI {alunno['nome']} {alunno['cognome']} ---")

    compiti_alunno = [c for c in lista_compiti.values() if c['alunno_matricola'] == matricola]

    if not compiti_alunno:
        print("Nessun compito assegnato a questo studente")
        return

    print(f"\nTotale compiti assegnati: {len(compiti_alunno)}")

    completati = [c for c in compiti_alunno if c['stato'] == 'registrato']
    non_completati = [c for c in compiti_alunno if c['stato'] != 'registrato']

    print(f"Compiti completati: {len(completati)}")
    print(f"Compiti da completare: {len(non_completati)}")

    voti = [c['voto'] for c in compiti_alunno if c['voto'] is not None]
    if voti:
        media = sum(voti) / len(voti)
        print(f"\nMedia voti: {media:.2f}")
        print(f"Voto minimo: {min(voti)}")
        print(f"Voto massimo: {max(voti)}")

        # Progressione voti nel tempo
        compiti_con_voto = [c for c in compiti_alunno if c['voto'] is not None]
        compiti_con_voto.sort(key=lambda x: x['data_assegnazione'])

        print("\nProgressione voti nel tempo:")
        for c in compiti_con_voto:
            data = c['data_assegnazione'].split(" ")[0]  # Solo la data
            print(f"  {data} - {c['descrizione'][:30]}: {c['voto']}")
    else:
        print("\nNessun voto registrato")


def classifica_per_media():
    """Mostra la classifica degli studenti per media voti"""
    print("\n--- CLASSIFICA STUDENTI PER MEDIA VOTI ---")

    if not lista_alunni:
        print("Nessuno studente registrato")
        return

    classifica = []

    for matricola, alunno in lista_alunni.items():
        voti = [c['voto'] for c in lista_compiti.values()
                if c['alunno_matricola'] == matricola and c['voto'] is not None]

        if voti:
            media = sum(voti) / len(voti)
            classifica.append({
                'matricola': matricola,
                'nome': f"{alunno['nome']} {alunno['cognome']}",
                'media': media,
                'num_voti': len(voti)
            })
        else:
            classifica.append({
                'matricola': matricola,
                'nome': f"{alunno['nome']} {alunno['cognome']}",
                'media': None,
                'num_voti': 0
            })

    # Ordina per media (decrescente), studenti senza voti in fondo
    classifica.sort(key=lambda x: (x['media'] is not None, x['media'] or 0), reverse=True)

    print(f"\n{'Pos':<5}{'Nome':<25}{'Matricola':<12}{'Media':<10}{'N. Voti':<8}")
    print("-" * 60)

    for i, studente in enumerate(classifica, 1):
        media_str = f"{studente['media']:.2f}" if studente['media'] is not None else "N/A"
        print(f"{i:<5}{studente['nome']:<25}{studente['matricola']:<12}{media_str:<10}{studente['num_voti']:<8}")


def report_compiti_non_completati():
    """Mostra report dei compiti non completati"""
    print("\n--- REPORT COMPITI NON COMPLETATI ---")

    compiti_nc = {k: v for k, v in lista_compiti.items() if v['stato'] != 'registrato'}

    if not compiti_nc:
        print("Tutti i compiti sono stati completati!")
        return

    print(f"\nTotale compiti non completati: {len(compiti_nc)}")
    print()

    for task_id, dati in compiti_nc.items():
        alunno = lista_alunni.get(dati['alunno_matricola'], {})
        nome_alunno = f"{alunno.get('nome', '?')} {alunno.get('cognome', '?')}"

        print(f"{task_id}: {dati['descrizione']}")
        print(f"  Studente: {nome_alunno} ({dati['alunno_matricola']})")
        print(f"  Stato: {dati['stato']}")
        print(f"  Assegnato il: {dati['data_assegnazione']}")
        print()


def salva_backup():
    """Salva i dati in file di backup"""
    print("\n--- SALVA BACKUP ---")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    backup_alunni = f"backup_alunni_{timestamp}.json"
    backup_compiti = f"backup_compiti_{timestamp}.json"

    try:
        with open(backup_alunni, 'w', encoding='utf-8') as f:
            json.dump(lista_alunni, f, indent=4, ensure_ascii=False)
        print(f"Backup alunni salvato: {backup_alunni}")

        with open(backup_compiti, 'w', encoding='utf-8') as f:
            json.dump(lista_compiti, f, indent=4, ensure_ascii=False)
        print(f"Backup compiti salvato: {backup_compiti}")

        print("\nBackup completato con successo!")
    except Exception as e:
        print(f"Errore durante il backup: {e}")


def carica_backup():
    """Carica i dati da file di backup"""
    global lista_alunni, lista_compiti

    print("\n--- CARICA BACKUP ---")

    file_alunni = input("Nome file backup alunni (es: backup_alunni_20231201_120000.json): ").strip()
    file_compiti = input("Nome file backup compiti (es: backup_compiti_20231201_120000.json): ").strip()

    if not os.path.exists(file_alunni):
        print(f"File {file_alunni} non trovato!")
        return

    if not os.path.exists(file_compiti):
        print(f"File {file_compiti} non trovato!")
        return

    conferma = input("\nQuesta operazione sovrascrivera' i dati attuali. Continuare? (s/n): ").lower()

    if conferma != 's':
        print("Operazione annullata")
        return

    try:
        with open(file_alunni, 'r', encoding='utf-8') as f:
            lista_alunni = json.load(f)

        with open(file_compiti, 'r', encoding='utf-8') as f:
            lista_compiti = json.load(f)

        salva_alunni()
        salva_compiti()

        print(f"\nBackup caricato: {len(lista_alunni)} alunni, {len(lista_compiti)} compiti")
    except Exception as e:
        print(f"Errore durante il caricamento: {e}")


# ==================== FUNZIONI OPZIONALI ====================

def ricerca_studente():
    """Cerca studenti per nome, cognome o matricola"""
    print("\n--- RICERCA STUDENTE ---")

    if not lista_alunni:
        print("Nessuno studente registrato")
        return

    termine = input("Cerca per nome, cognome o matricola: ").strip().lower()

    if not termine:
        print("Inserisci un termine di ricerca!")
        return

    risultati = []
    for matricola, alunno in lista_alunni.items():
        if (termine in alunno['nome'].lower() or
            termine in alunno['cognome'].lower() or
            termine in matricola.lower()):
            risultati.append((matricola, alunno))

    if not risultati:
        print(f"Nessun risultato per '{termine}'")
        return

    print(f"\nTrovati {len(risultati)} risultati:\n")
    for matricola, alunno in risultati:
        print(f"  {matricola} - {alunno['nome']} {alunno['cognome']} ({alunno['email']})")


def esporta_csv():
    """Esporta i dati in formato CSV"""
    print("\n--- ESPORTAZIONE CSV ---")

    print("Cosa vuoi esportare?")
    print("1. Elenco studenti")
    print("2. Elenco compiti")
    print("3. Report completo (studenti + voti)")

    scelta = input("\nScelta: ").strip()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if scelta == "1":
        filename = f"export_studenti_{timestamp}.csv"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Matricola,Nome,Cognome,Email,Data Creazione,Data Modifica\n")
                for matricola, alunno in lista_alunni.items():
                    f.write(f"{matricola},{alunno['nome']},{alunno['cognome']},{alunno['email']},{alunno['data_creazione']},{alunno['data_modifica']}\n")
            print(f"Esportato: {filename}")
        except Exception as e:
            print(f"Errore esportazione: {e}")

    elif scelta == "2":
        filename = f"export_compiti_{timestamp}.csv"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("ID Compito,Descrizione,Matricola Studente,Stato,Data Assegnazione,Voto\n")
                for task_id, compito in lista_compiti.items():
                    voto = compito['voto'] if compito['voto'] is not None else ""
                    f.write(f"{task_id},{compito['descrizione']},{compito['alunno_matricola']},{compito['stato']},{compito['data_assegnazione']},{voto}\n")
            print(f"Esportato: {filename}")
        except Exception as e:
            print(f"Errore esportazione: {e}")

    elif scelta == "3":
        filename = f"export_report_{timestamp}.csv"
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("Matricola,Nome,Cognome,Email,Compiti Assegnati,Compiti Completati,Media Voti\n")
                for matricola, alunno in lista_alunni.items():
                    compiti = [c for c in lista_compiti.values() if c['alunno_matricola'] == matricola]
                    completati = len([c for c in compiti if c['stato'] == 'registrato'])
                    voti = [c['voto'] for c in compiti if c['voto'] is not None]
                    media = f"{sum(voti)/len(voti):.2f}" if voti else "N/A"
                    f.write(f"{matricola},{alunno['nome']},{alunno['cognome']},{alunno['email']},{len(compiti)},{completati},{media}\n")
            print(f"Esportato: {filename}")
        except Exception as e:
            print(f"Errore esportazione: {e}")

    else:
        print("❌ Opzione non valida!")


def importa_csv():
    """Importa studenti da un file CSV"""
    print("\n--- 📥 IMPORTAZIONE CSV ---")

    filename = input("Nome file CSV da importare (es: studenti.csv): ").strip()

    if not os.path.exists(filename):
        print(f"❌ File {filename} non trovato!")
        return

    try:
        with open(filename, 'r', encoding='utf-8') as f:
            linee = f.readlines()

        if len(linee) < 2:
            print("⚠️  File vuoto o senza dati!")
            return

        # Salta l'intestazione
        header = linee[0].strip().lower()
        print(f"📋 Intestazione trovata: {header}")

        importati = 0
        errori = 0

        for i, linea in enumerate(linee[1:], start=2):
            try:
                campi = linea.strip().split(',')
                if len(campi) < 3:
                    print(f"⚠️  Riga {i}: dati insufficienti, saltata")
                    errori += 1
                    continue

                nome = campi[0].strip()
                cognome = campi[1].strip()
                email = campi[2].strip()

                if not nome or not cognome or not email:
                    print(f"⚠️  Riga {i}: campi vuoti, saltata")
                    errori += 1
                    continue

                if not valida_email(email):
                    print(f"⚠️  Riga {i}: email non valida ({email}), saltata")
                    errori += 1
                    continue

                matricola = genera_matricola()
                data_corrente = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                lista_alunni[matricola] = {
                    "nome": nome,
                    "cognome": cognome,
                    "email": email,
                    "matricola": matricola,
                    "data_creazione": data_corrente,
                    "data_modifica": data_corrente,
                    "archiviato": False
                }
                importati += 1

            except Exception as e:
                print(f"⚠️  Riga {i}: errore ({e}), saltata")
                errori += 1

        salva_alunni()
        print(f"\n✅ Importazione completata!")
        print(f"   📊 Importati: {importati} studenti")
        if errori > 0:
            print(f"   ⚠️  Errori: {errori} righe")

    except Exception as e:
        print(f"❌ Errore durante l'importazione: {e}")


# ==================== MENU PRINCIPALE ====================

def visualizza_menu():
    """Visualizza il menu principale"""
    print("\n" + "=" * 50)
    print("🎓 SISTEMA GESTIONE STUDENTI E COMPITI 🎓".center(50))
    print("=" * 50)
    print("\n----- STUDENTI 👤 ------------------")
    print("1. ➕ Inserisci nuovo studente")
    print("2. 📋 Visualizza studenti")
    print("3. ✏️  Modifica dati studente")
    print("4. 📦 Archivia studente")
    print("5. 🔍 Cerca studente")
    print("6. 📭 Visualizza archiviati")
    print("7. ♻️  Ripristina studente")
    print("\n----- COMPITI 📝 -------------------")
    print("8.  ➕ Assegna compito a studente")
    print("9.  ✅ Registra valutazione")
    print("10. 📄 Visualizza compiti di uno studente")
    print("11. 📋 Visualizza tutti i compiti")
    print("\n----- STATISTICHE E REPORT 📊 ------")
    print("12. 📈 Statistiche generali")
    print("13. 📈 Visualizza statistiche studente")
    print("14. 🏆 Classifica studenti per media voti")
    print("15. ⚠️  Report compiti non completati")
    print("\n----- GESTIONE DATI 💾 -------------")
    print("16. 💾 Salva dati (backup)")
    print("17. 📂 Carica dati (ripristino)")
    print("18. 📤 Esporta CSV")
    print("19. 📥 Importa CSV")
    print("\n---- ALTRO 🔧 ----------------------")
    print("M. 📜 Visualizza menu")
    print("0. 🚪 Esci")


def menu():
    """Menu principale del programma"""
    carica_dati()
    visualizza_menu()

    while True:
        scelta = input("\nScegli un'opzione: ").strip().upper()

        if scelta == "1":
            inserisci_alunno()
        elif scelta == "2":
            visualizza_alunni()
        elif scelta == "3":
            modifica_alunno()
        elif scelta == "4":
            elimina_alunno()
        elif scelta == "5":
            ricerca_studente()
        elif scelta == "6":
            visualizza_archiviati()
        elif scelta == "7":
            ripristina_alunno()
        elif scelta == "8":
            inserisci_compito()
        elif scelta == "9":
            valuta_compito()
        elif scelta == "10":
            visualizza_compiti_alunno()
        elif scelta == "11":
            visualizza_compiti()
        elif scelta == "12":
            statistiche()
        elif scelta == "13":
            statistiche_studente()
        elif scelta == "14":
            classifica_per_media()
        elif scelta == "15":
            report_compiti_non_completati()
        elif scelta == "16":
            salva_backup()
        elif scelta == "17":
            carica_backup()
        elif scelta == "18":
            esporta_csv()
        elif scelta == "19":
            importa_csv()
        elif scelta == "M":
            visualizza_menu()
        elif scelta == "0":
            print("\n--- CONFERMA USCITA ---")
            print("1. Sì, esci dal gestionale")
            print("2. No, torna al menu principale")
            conferma_uscita = input("\nVuoi davvero uscire? (1/2): ").strip()
            if conferma_uscita == "1":
                print("\nArrivederci!")
                break
            else:
                print("\nTorno al menu principale...")
                visualizza_menu()
        else:
            print("\nOpzione non valida!")


if __name__ == "__main__":
    menu()
