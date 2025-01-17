# Progetto-Metodi-Computazionali
Progetto per l'esame di Metodi computazionali per la fisica - Campionamento Sciami Atmosferici ad Alta Quota

Il progetto si struttura in due script python: sciame.py - simulazionesciame.py.

1) Il primo script (sciame.py) presenta le funzioni usate nella simulazione dello sciame elettromagnetico. Le funzioni in esso sviluppate 
sono poi richiamate nel secondo script attraverso l'importazione di sciame.py in simulazionesciame.py
2) Nel secondo script (simulazionesciame.py) viene importato il primo, così da poter rappresentare graficamente i risultati medi ottenuti dalla simulazione dello sciame per varie
 configurazioni di energia iniziale e angolo rispetto alla verticale. 
Questo secondo script è diviso in tre parti, nella prima si realizzano in un'unica figura un istogramma 3D rappresentante il numero medio di particelle rivelate in funzione dell'energia 
iniziale per 4 angoli e un grafico scatter rappresentante il numero medio di particelle rivelate in funzione dell'energia per vari angoli con i relativi errori calcolati con la deviazione standard della media
, nella seconda in un'unica figura due grafici analoghi ma questa volta del numero medio di particelle rivelate in funzione dell'angolo rispetto alla verticale per 4 valori di energia, 
nella terza in un'unica immagine un grafico scatter e un  grafico contourf rappresentanti  il numero medio di particelle per  varie coppie energia-angolo usando una colorbar.
Per selezionare il primo bisogna digitare python3 simulazionesciame.py --hisen, per il secondo python3 simulazionesciame.py --hisang, per il terzo python3 simulazionesciame.py --color

Successivamente per il primo grafico il programma richiede di inserire in ordine:
- il numero di valori di energia da considerare (uniformemente spaziati tra 1 TeV e 100 TeV) per ognuno dei 4 angoli (anche essi uniformemente spaziati tra 0° e 45°)
- il numero di simulazioni da fare per ogni coppia energia-angolo
- il passo di avanzamento s in frazioni di X0 (il valore deve essere compreso tra 0 e 1 e il programma lo richiede fino a che il valore inserito sia in questo intervallo)
- se salvare l'immagine ottenuta o meno (va digitato Yes o No e il programma lo richiede fino a che la stringa inserita sia Yes o No)
- se si decide di salvare l'immagine, il pathname di quest'ultima

Per il secondo il programma richiede:
- il numero di angoli da considerare (uniformemente spaziati tra 0° e 45°) per ognuno dei 4 valori di energia (anche essi uniformemente spaziati tra 1 TeV e 100 TeV)
- il numero di simulazioni da fare per ogni coppia energia-angolo
- il passo di avanzamento s  in frazioni di X0 (il valore deve essere compreso tra 0 e 1 e il programma lo richiede fino a che il valore inserito sia in questo intervallo)
- se salvare l'immagine ottenuta o meno (va digitato Yes o No e il programma lo richiede fino a che la stringa inserita sia Yes o No)
- se si decide di salvare l'immagine, il pathname di quest'ultima

Per il terzo il programma richiede:
- il numero di valori di energia (uniformemente spaziati tra 1 TeV e 100 TeV) e di angolo (anche essi uniformemente spaziati tra 0° e 45°) da considerare (il numero è lo stesso per le due
grandezze).
- se si decide di salvare l'immagine, il pathname di quest'ultima
- il passo di avanzamento  s in frazioni di X0 (il valore deve essere compreso tra 0 e 1 e il programma lo richiede fino a che il valore inserito sia in questo intervallo)
- se salvare l'immagine ottenuta o meno (va digitato Yes o No e il programma lo richiede fino a che la stringa inserita sia Yes o No)
- se si decide di salvare l'immagine, il pathname di quest'ultima

Successivamente avviene la simulazione dello sciame usando le funzioni definite in sciame.py e i risultati vengono rappresentati nel grafico scelto.

L'avanzamento della simulazione è rappresentato  dalla barra tqdm.
