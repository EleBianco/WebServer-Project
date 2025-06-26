# Relazione Tecnica: Web Server Minimale in Python

## 1. Introduzione

Questo documento descrive lo sviluppo di un server HTTP minimale in Python, realizzato esclusivamente con la libreria standard `socket`. Il server gestisce richieste HTTP di base e serve un sito statico dedicato alla pallavolo, composto da file HTML, CSS e immagini.

## 2. Architettura del Server

### 2.1 Panoramica

Il server è progettato per gestire più connessioni contemporaneamente tramite un’architettura multi-thread. I principali componenti sono:

- **Socket Server**: Gestisce le connessioni TCP
- **HTTP Request Handler**: Analizza le richieste HTTP e genera risposte
- **File System Handler**: Recupera i file dalla directory www e li invia al client
- **Logger**: Registra tutte le attività e le richieste del server

### 2.2 Flusso di Esecuzione

1. Il server inizializza un socket TCP e si mette in ascolto sulla porta 8080.
2. Per ogni nuova connessione, viene creato un thread dedicato.
3. Il thread analizza la richiesta HTTP ricevuta.
4. Se la richiesta è valida, il server cerca il file richiesto nella directory `www/`.
5. Il server invia una risposta HTTP con il file richiesto o una pagina di errore 404.
6. La connessione viene chiusa e il thread termina.

## 3. Implementazione

### 3.1 Inizializzazione del Server

Il server viene inizializzato nella funzione `main()`, che:

- Inizializza i tipi MIME supportati.
- Verifica l’esistenza della directory dei documenti `www/`.
- Crea il file di log se non esiste.
- Configura il socket del server.
- Avvia il ciclo principale che accetta le connessioni.

### 3.2 Gestione delle Connessioni

La funzione `handle_request()` gestisce ogni client:

- Riceve e decodifica la richiesta HTTP.
- Analizza la prima riga per metodo, percorso e versione.
- Gestisce solo richieste GET.
- Reindirizza le richieste alla radice `/` verso `index.html`.
- Verifica che il file richiesto esista e sia nella directory consentita.
- Legge il file e determina il tipo MIME.
- Costruisce e invia la risposta HTTP.

### 3.3 Gestione degli Errori

Il server implementa una robusta gestione degli errori:

- **Errore 404 (Not Found)**: Se il file non esiste.
- **Errore 500 (Internal Server Error)**: In caso di errori interni.
- **Validazione del percorso**: Previene attacchi di directory traversal.

### 3.4 Logging

Tutte le richieste vengono registrate in `server.log`, con:

- Timestamp
- Indirizzo IP e porta del client
- Riga della richiesta
- Codice di stato HTTP

### 3.5 Supporto MIME Types

Il server riconosce automaticamente il tipo di file richiesto (HTML, CSS, immagini) tramite il modulo `mimetypes`, inviando l’header `Content-Type` corretto.

## 4. Il Sito Web Demo

### 4.1 Struttura del Sito

Il sito web dimostrativo è composto da:

- **index.html**: Homepage con introduzione
- **storia.html**: Pagina informativa sulla storia della pallavolo
- **regole.html**: Pagina informativa sulle regole dello sport
- **style.css**: Foglio di stile condiviso
- **logo.png**: Logo del sito

### 4.2 Caratteristiche dell'Interfaccia

- **Design Responsive**: Layout adattivo per desktop e mobile
- **Navigazione**: Menu intuitivo
- **Animazioni CSS**: Effetti per una migliore esperienza utente
- **Immagini**: Logo e icone a tema pallavolo.


### 4.3 Best Practices Implementate

- **CSS Modulare**: Stili organizzati per componenti
- **Markup Semantico**: Utilizzo appropriato di tag HTML5
- **Progressive Enhancement**: Funzionalità base accessibili anche senza JavaScript
- **Compatibilità Cross-Browser**: Stile e funzionalità consistenti su diversi browser

## 5. Estensioni Implementate

### 5.1 Supporto MIME Types

Il server è stato configurato per riconoscere e servire correttamente diversi tipi di file statici, fondamentali per un sito web moderno.

- HTML (text/html)
- CSS (text/css)
- JavaScript (text/javascript)
- Immagini (image/jpeg, image/png, ecc.)
- Altri tipi comuni di file

### 5.2 Sistema di Logging

Il sistema di logging salva:

- Data e ora della richiesta
- Indirizzo IP e porta del client
- Dettagli della richiesta HTTP (metodo, percorso, versione)
- Codice di stato della risposta (ad esempio 200, 404)
- Eventuali errori riscontrati

### 5.3 Design Responsivo e Animazioni

Il sito servito dal server è stato progettato con attenzione all’esperienza utente:

- **Layout responsivo**: Il sito si adatta automaticamente a schermi di diverse dimensioni, risultando fruibile sia da desktop che da dispositivi mobili.
- **Animazioni CSS**: Sono stati implementati effetti di transizione e animazione per rendere la navigazione più piacevole e moderna.
- **Transizioni fluide**: Gli elementi dell’interfaccia presentano movimenti e cambiamenti di stato graduali, migliorando la percezione di qualità del sito.

## 6. Sicurezza

### 6.1 Misure Implementate

Per garantire la sicurezza sono state adottate alcune precauzioni:

- **Validazione dei percorsi**: Il server verifica che ogni richiesta sia limitata alla directory `www/`, prevenendo attacchi di tipo directory traversal.
- **Limitazione dei metodi HTTP**: Vengono accettate solo richieste GET, escludendo altri metodi potenzialmente pericolosi.
- **Controllo degli accessi**: Solo i file presenti nella directory `www/` possono essere serviti.

### 6.2 Limitazioni

Essendo un server dimostrativo, sono presenti alcune limitazioni:

- Non supporta HTTPS
- Non implementa autenticazione o autorizzazione degli utenti
- Non offre protezione avanzata contro attacchi DDoS o altre minacce tipiche dei server di produzione

## 7. Istruzioni per l'Uso

### 7.1 Requisiti

- Python 3.6 o superiore

### 7.2 Esecuzione del Server

1. Posiziona il file `server.py` e la cartella `www/` nella stessa directory
2. Avvia il server con: `python server.py`
3. Accedi al sito tramite un browser all'indirizzo: `http://localhost:8080`

### 7.3 Personalizzazione

Per modificare le impostazioni del server (ad esempio porta, indirizzo o directory dei file), puoi cambiare i parametri all’inizio del file `server.py`:

- `HOST`: L'indirizzo su cui il server risponde (default: localhost)
- `PORT`: La porta di ascolto (default: 8080)
- `DOCUMENT_ROOT`: La directory dei file statici (default: www)

## 8. Conclusioni

Questo progetto dimostra come sia possibile realizzare un server HTTP minimale in Python, capace di servire un sito statico tematico (in questo caso sulla pallavolo) con funzionalità di base ma complete.

Il server è pensato per scopi didattici e per comprendere i principi fondamentali della programmazione di rete e del protocollo HTTP.

Per applicazioni reali o in produzione, si consiglia di utilizzare server più avanzati come Nginx, Apache o framework Python come Flask o Django.
