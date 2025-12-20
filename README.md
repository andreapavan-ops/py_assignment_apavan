# Gestionale Alunni e Compiti

Sistema di gestione studenti e compiti sviluppato in Python.

## Requisiti

- Python 3.x

## Avvio del programma

```bash
python sistema_alunni_ITS.py
```

## Funzionalita'

### Gestione Studenti

| Opzione | Funzione | Descrizione |
|---------|----------|-------------|
| 1 | Inserisci nuovo studente | Aggiunge un alunno con nome, cognome ed email |
| 2 | Visualizza studenti | Mostra tutti gli alunni attivi |
| 3 | Modifica dati studente | Modifica nome, cognome o email di un alunno |
| 4 | Archivia studente | Archivia un alunno (soft delete) |
| 5 | Cerca studente | Ricerca per nome, cognome o matricola |
| 6 | Visualizza archiviati | Mostra gli alunni archiviati |
| 7 | Ripristina studente | Riattiva un alunno archiviato |

### Gestione Compiti

| Opzione | Funzione | Descrizione |
|---------|----------|-------------|
| 8 | Assegna compito | Crea un nuovo compito e lo assegna a uno studente |
| 9 | Registra valutazione | Assegna un voto (0-10) a un compito |
| 10 | Visualizza compiti studente | Mostra i compiti di un singolo alunno |
| 11 | Visualizza tutti i compiti | Mostra l'elenco completo dei compiti |

### Statistiche e Report

| Opzione | Funzione | Descrizione |
|---------|----------|-------------|
| 12 | Statistiche generali | Totale alunni, compiti e media voti |
| 13 | Statistiche studente | Dettaglio voti e progressione di uno studente |
| 14 | Classifica per media | Ranking studenti per media voti |
| 15 | Report compiti non completati | Elenco compiti ancora da valutare |

### Gestione Dati

| Opzione | Funzione | Descrizione |
|---------|----------|-------------|
| 16 | Salva backup | Crea file di backup con timestamp |
| 17 | Carica backup | Ripristina dati da file di backup |
| 18 | Esporta CSV | Esporta studenti, compiti o report in CSV |
| 19 | Importa CSV | Importa studenti da file CSV |

### Altro

| Opzione | Funzione | Descrizione |
|---------|----------|-------------|
| M | Visualizza menu | Mostra nuovamente il menu completo |
| 0 | Esci | Chiude il programma (con conferma) |

## File di dati

Il programma utilizza due file JSON per la persistenza:

- `dati_alunni.json` - Dati degli studenti
- `lista_compiti.json` - Dati dei compiti e valutazioni

## Formato CSV per importazione

Per importare studenti, creare un file CSV con questo formato:

```
Nome,Cognome,Email
Mario,Rossi,mario.rossi@email.com
Giulia,Bianchi,giulia.bianchi@email.com
```

## Validazioni

- **Email**: deve essere in formato valido (es. nome@dominio.com)
- **Voto**: deve essere un numero intero tra 0 e 10
- **Campi obbligatori**: nome, cognome ed email per gli studenti

## Autore

Progetto sviluppato per il corso ITS.
