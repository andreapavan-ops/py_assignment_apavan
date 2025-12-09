import json
import os
from datetime import datetime

#FILE DI PERSISTENZA
DATA_JSON="data_studenti.json"

#STRUTTURA GLOBALE
database = {
    "studenti": {},
    "compiti": {}
}

#FUNZIONI
def carica_dati():
    global database
    if os.path.exists(DATA_JSON):
        try:
            with open(DATA_JSON, "r", encoding='utf-8') as f:
                database = json.load(f)
                print(f"dati caricati ({len(database ['studenti'])} studenti, {len(database['compiti'])} compiti)")
        except Exception as e:
            print(f"Caricamento erroneo: {e}")
    else:
        print("Non è stato trovato nessun file")        

def salva_dati():
    try:
        with open(DATA_JSON, 'w', encoding='utf-8') as f:
            json.dump(database, f, indent=2, ensure_ascii=False)
            print("I dati sono stati salvati")
    except Exception as e:
            print(f"Errore di salvataggio: {e}")

#GESTIONALE STUDENTI
def nuovo_studente():
    print("\n --AGGIUNGI STUDENTE--")

    matricola = input("Numero di matricola: ").strip()

    if matricola in database["studenti"]:
        print("Numero Matricola Esistente")
        return

    nome = input("Nome: ").strip()
    cognome = input("Cognome: ").strip()
    email = input("Email: ").strip()

    if not nome or not cognome or not email:
        print("Completa tutti i campi")
        return

    database["studenti"][matricola] = {
        "nome": nome,
        "cognome": cognome,
        "email": email,
        "valutazioni": []

    }

    salva_dati()
    print(f"studente {nome} {cognome} {matricola} aggiunto con successo")

def visualizza_studenti():
    if not database["studenti"]:
        print("\n Il Registro studenti è vuoto")
        return

print("\n --REGISTRO STUDENTI--")
for chiave, valore in database["studenti"].items():
    print(f"\n Matricola: {chiave}")
    print(f"   Nome: {valore['nome']} {valore['cognome']}")
    print(f".  Email: {valore['email']}")
    print(f".   Valutazioni registrate: {len(valore['valutazioni'])}")

#FUNZIONE ELIMINA STUDENTE
def elimina_studente():
    matricola = input("\n Inserisci N° matricola da eliminare").strip()

    if matricola not in database ["studenti"]:
        print("studente inesistente")
        return

# MOSTRO LE INFORMAZIONI DEL STUDENTE CHE STO ELIMINANDO
    studente = database["studenti"][matricola]
    
    print(f"\n DATI STUDENTE DA ELIMINARE:")
    print(f"   Matricola: {matricola}")
    print(f"   Nome: {studente['nome']} {studente['cognome']}")
    print(f"   Email: {studente['email']}")
    print(f"   Valutazioni: {len(studente['valutazioni'])}")
    
    conferma = input(f"\n  Sei sicuro? (s/n): ").lower()
    
    if conferma == 's':
        del database["studenti"][matricola]
        salva_dati()
        print("Eliminato!")

#GESTIONE COMPITI
def nuovo_compito():
    print("\n -- CREA NUOVO COMPITO --")

    id_compito = input("ID compito (es. 001): ").strip()

    if id_compito in database["compiti"]:
        print("Compito già esistente")
        return

    titolo = input("Titolo compito: ").strip()
    descrizione = input("Descrizione: ").strip()

    if not titolo:
        print("Devi inserire un Titolo!")
        return

    database["compiti"][id_compito] = {
        "titolo": titolo,
        "descrizione": descrizione,
        "data_creazione": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }    

    salva_dati()
    print(f"Hai creato il seguente compito: {titolo}")

def visualizza_compiti():
    if not database["compiti"]:
        print("\n Non è presente nessun compito")
        return
    
    print("\n -- ELENCO COMPITI --")
    for chiave, valore in database["compiti"].items():
        print(f"\n ID: {chiave}")
        print(f"   Titolo: {valore['titolo']}")
        print(f"   Descrizione: {valore['descrizione']}")
        print(f"   Creato il: {valore['data_creazione']}")

#GESTIONE VALUTAZIONI
def registra_valutazione():
    print("\n -- REGISTRA VALUTAZIONE --")

    matricola = input("Matricola studente: ").strip()
    if matricola not in database["studenti"]:
        print("Studente inesistente!")
        return

#Mostra compiti
    if database["compiti"]:
        print("\n Compiti presenti:")
        for chiave, valore in database["compiti"].items():
            print(f"  - {chiave}: {valore['titolo']}")
    else:
        print("\n Nessun compito inserito!")        

    id_compito = input("ID compito: ").strip()

    if id_compito not in database["compiti"]:
        print("Compito inesistente")
        return

    try:
        voto = float(input("Voto (0-30)").strip())
        if voto  < 0 or voto > 30:
            print("il voto deve essere tra 0 e 30!")
            return
    except ValueError:
        print("Voto non valido!")
        return        

    valutazione = {
        "id_compito": id_compito,
        "titolo_compito": database["compiti"][id_compito]["titolo"],
        "voto": voto,
        "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }

    database["studenti"][matricola]["valutazioni"].append(valutazione)
    salva_dati()

    studente = database["studenti"][matricola]
    print(f"Valutazione registrata del {studente['nome']} {studente['cognome']}")

#MOSTRA LE VALUTAZIONI DI UNO STUDENTE
def visualizza_valutazioni_studente():
    matricola = input("\nMatricola studente: ").strip()

    if matricola not in database["studenti"]:
        print("Studente non trovato!")
        return

    studente = database["studenti"][matricola]
    valutazioni = studente["valutazioni"]

    print(f"\n -- Valutazione del studente: {studente['nome']} {studente['cognome']} --")
    if not valutazioni:
        print("Non esistono valutazioni")
        return

    for indice, elemento in enumerate(valutazioni, 1):
        print(f"\n{indice}. Compito: {elemento['titolo_compito']} (ID: {elemento['id_compito']})")
        print(f"   Voto: {elemento['voto']}")
        print(f"   Data: {elemento['data']}")

#STATISTICHE
    print("\n -- Valutazione Statistica per Studente -- ")
def statistiche_studenti():
    if not database["studenti"]:
        print("\n Nessuno studente presente")
        return

#CALCOLO TOTALE COMPITI ASSEGNATI
    num_compiti_assegnati = len(database["compiti"])


    lista_media = []

    for matricola, studente in database ["studenti"].items():
        valutazioni = studente["valutazioni"]

        print(f"\n {studente['nome']} {studente['cognome']} (Matr.N.{matricola})")

        if not valutazioni:
            print(" Valutazioni inesistenti")
            continue


# 1-MEDIA VOTI PER ALUNNO
        voti = []
        for v in valutazioni:
            voti.append(v["voto"])

        media = sum(voti) / len(voti)
        lista_media.append(media)

# 2-NUMERO COMPITI COMPLETATI
        num_completati = len(valutazioni)

# 3-VOTO MASSIMO E MINIMO
        voto_min = min(voti)
        voto_max = max(voti)

# 4-PROGRESSIONE VOTI NEL TEMPO
        valutazioni_ordinate = sorted(valutazioni, key=lambda x: x["data"])

        print(f"\n  STATISTICHE GENERALI:")
        print(f"     Media voti: {media:.2f}/30")
        print(f"     Voto minimo: {voto_min}")
        print(f"     Voto massimo: {voto_max}")
        print(f"     Compiti assegnati: {num_compiti_assegnati}")
        print(f"     Compiti completati: {num_completati}")
        
        if num_compiti_assegnati > 0:
            percentuale = (num_completati / num_compiti_assegnati) * 100
            print(f"     • Tasso completamento: {percentuale:.1f}%")

# PROGRESSIONE VOTI NEL TEMPO
        print(f"\n  PROGRESSIONE VOTI NEL TEMPO:")
        for i, val in enumerate(valutazioni_ordinate, 1):
            # Indicatore trend
            if i > 1:
                voto_precedente = valutazioni_ordinate[i-2]["voto"]
                if val["voto"] > voto_precedente:
                    trend = "++"
                elif val["voto"] < voto_precedente:
                    trend = "--"
                else:
                    trend = "=="
            else:
                trend = "nuovo"

            print(f"     {i}. [{val['data'][:10]}] {val['titolo_compito']}: {val['voto']}/30 {trend}")

# STATISTICHE GENERALI CLASSE
    if lista_media:
        print(f"\n{'='*60}")
        print("STATISTICHE GENERALI CLASSE")
        print(f"\n  Media generale di tutti gli studenti: {sum(lista_media) / len(lista_media):.2f}/30")
        print(f"  Numero studenti con valutazioni: {len(lista_media)}/{len(database['studenti'])}")
        print(f"  Media più alta: {max(lista_media):.2f}")
        print(f"  Media più bassa: {min(lista_media):.2f}")

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


