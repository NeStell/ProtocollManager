# Protocollazione automatica PDF

Questo programma protocolla automaticamente file PDF presenti in
specifiche cartelle, aggiungendo al documento il numero di protocollo,
la data e il tipo di documento.\
Ogni file protocollato viene salvato con un nuovo nome contenente il
numero progressivo e con un'intestazione scritta direttamente nel PDF.

## Funzionalità

-   Scansione automatica delle cartelle:

    -   `acquisti_da_protocollare`
    -   `vendite_da_protocollare`

-   Gestione delle sottocartelle:

    -   `fattura_normale`
    -   `fattura_elettronica`
    -   `ordine`

-   Aggiunta di:

    -   Numero di protocollo
    -   Data di protocollazione
    -   Tipo documento (Acquisto/Vendita + descrizione)

-   Numerazione progressiva distinta per ogni categoria e sottocartella.

-   Sistema di salvataggio degli ultimi numeri di protocollo tramite
    file di testo:

        last_protocol_number_<main>_<sub>.txt

-   Evita doppioni: se un PDF è già stato protocollato, viene ignorato.

## Struttura cartelle richiesta

    acquisti_da_protocollare/
    │   ├─ fattura_normale/
    │   ├─ fattura_elettronica/
    │   └─ ordine/
    vendite_da_protocollare/
    │   ├─ fattura_normale/
    │   ├─ fattura_elettronica/
    │   └─ ordine/

Lo script creerà automaticamente le cartelle di output:

    acquisti_protocollate/
    vendite_protocollate/

## Installazione

### 1. Scarica python

    vai su microsoft store e trova Python 3.13

### 2. Scarica il programma

    scarica il programma cliccando il code e dopo installa .zip


### 3. Installa i requisiti

    pip install -r requirements.txt

## Come avviare

1.  Inserisci i PDF da protocollare nelle cartelle previste.\
2.  Avvia lo script:

    python main.py

Lo script:

-   protocollerà tutti i PDF trovati;
-   creerà nelle cartelle di output file del tipo:

    001_nomefile.pdf

-   scriverà dentro il PDF una riga come:

    Protocollo N° 1 | Data: 25/11/2025 | Acquisto - Fattura Normale

-   salverà gli ultimi numeri di protocollo utilizzati per continuare la
    numerazione nelle esecuzioni successive.

-   dentro cartelle hai i file che si chiamono .gitignore gli puoi eliminare senza i problemi(non servono per il programma)

## Requirements

    PyPDF2
    reportlab

## Note

-   Lo script elabora solo file `.pdf`.
-   I file già protocollati non vengono elaborati nuovamente.
-   Ogni tipo di documento può avere una posizione del testo diversa nel
    PDF.
