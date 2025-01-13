# Progetto-Metodi-Computazionali
Progetto per l'esame di Metodi computazionali per la fisica

Il progetto si struttura in due script python: sciame.py - simulazionesciame.py.

1) Il primo script (sciame.py) presenta le funzioni usate nella simulazione dello sciame elettromagnetico. Questo non va necessariamente eseguito, poichè le funzioni in esso sviluppate 
sono poi richiamate nel secondo script attraverso l'importazione di sciame.py in simulazionesciame.py
2) Nel secondo script (simulazionesciame.py) viene importato il primo, così da poter rappresentare graficamente i risultati ottenuti dalla simulazione dello sciame per varie
 configurazioni di energia iniziale e angolo rispetto alla verticale. 
Questo secondo script è diviso in tre parti, nella prima si realizzano in un'unica figura due istogrammi rappresentanti il numero di particelle rivelate in funzione dell'energia 
iniziale per 4 angoli, nella seconda due istogrammi in un'unica figura del numeri di particelle rivelate in funzione dell'angolo rispetto alla verticale per 4 valori di energia, 
nella terza un grafico contourf rappresentante il numero di particelle per le varie coppie energia-angolo.
Per selezionare il primo bisogna digitare --hisen, per il secondo --hisang, per il terzo --color.
Successivamente per il primo grafico il programma richiede di inserire in ordine:
- il numero di valori di energia da considerare (uniformemente spaziati tra 1 TeV e 100 TeV) per ognuno dei 4 angoli (anche essi uniformemente spaziati tra 0° e 45°)
- il passo s in frazioni di X0 (il valore deve essere compreso tra 0 e 1 e il programma lo richiede fino a che il valore inserito sia in questo intervallo)
- se salvare l'immagine ottenuta o meno (va digitato Yes o No e il programma lo richiede fino a che la stringa insirita sia Yes o No)

Per il secondo il programma richiede:
- il numero di angoli da considerare (uniformemente spaziati tra 0° e 45°) per ognuno dei 4 valori di energia (anche essi uniformemente spaziati tra 1 TeV e 100 TeV)
- il passo s in frazioni di X0 (il valore deve essere compreso tra 0 e 1 e il programma lo richiede fino a che il valore inserito sia in questo intervallo)
- se salvare l'immagine ottenuta o meno (va digitato Yes o No e il programma lo richiede fino a che la stringa insirita sia Yes o No)

Per il terzo il programma richiede:
- il numero di valori di energia (uniformemente spaziati tra 1 TeV e 100 TeV) e di angolo (anche essi uniformemente spaziati tra 0° e 45°) da considerare (il numero è lo stesso per le due
grandezze).
- il passo s in frazioni di X0 (il valore deve essere compreso tra 0 e 1 e il programma lo richiede fino a che il valore inserito sia in questo intervallo)
- se salvare l'immagine ottenuta o meno (va digitato Yes o No e il programma lo richiede fino a che la stringa inserita sia Yes o No)

Successivamente avviene la simulazione dello sciame usando le funzioni definite in sciame.py e i risultati vengono rappresentati nel grafico scelto. Se si sceglie di salvare i grafici,
questi vengono salvati nella cartella contenente lo script.


I tempi di esecuzione sono molto lunghi (sui 20 minuti per 16 simulazioni dello sciame) e l'avanzamento della simulazione è rappresentati dalla barra tqdm.
