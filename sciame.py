import numpy as np
import pandas as pd

#definizione costanti usate 

X0 = 7e4 # lunghezza di radiazione (cm)
quotainiz = 2.0e6 # quota iniziale sciame (cm)
quotariv = 4.0e5 # quota rivelatore (cm)
Ec_elet = 87.92 # energia critica elettroni (MeV)
Ec_pos = 85.97 # energia critica positroni (MeV)
c = 3.0e10 # (cm/s)
Er= 0.511 #energia a riposo elettrone e positrone (MeV)
en_coppia = 2*Er # energia legata alla produzione di coppie (MeV)
min_ioniz = 2.187e-3 # minimo di ionizzazione (MeV/cm)


#definizioni funzioni usate
def prob_brems(s):
    """
    funzione prob_brems(s) per determinare la probabilità che l'elettrone o il positrone
    interagisca per Bremsstrahlung  
    s: passo di avanzamento della simulazione in frazioni di X0 (compreso tra 0 e 1)

    probabilita= 1-np.exp(-s)

    return probabilita: valore della probabilità del processo
    """   
    probabilita = 1-np.exp(-s)
    return probabilita

def prob_coppia(s):

    """
    funzione prob_coppia(s) per determinare la probabilità della produzione di coppie 
    del fotone
    s: passo di avanzamento della simulazione in frazioni di X0 (compreso tra 0 e 1)

    probabilita= 1-np.exp(-7*s/9)

    return probabilita: valore della probabilità del processo
    """
    probabilita = 1-np.exp(-7*s/9)
    
    return probabilita


def aggiungi_part(df, lista):
    """
    funzione aggiungi_part(df,lista) per aggiungere nuove particelle al dataframe dello sciame
    df: dataframe
    lista: lista di tuple con dati delle nuove particelle

    return pd.concat([df,df_new], ingnore_index=True) dataframe dato dall'unione del dataframe precedente
    e di quello contenente le nuove particelle
    """
    #se la lista è vuota restituisce df
    if not lista: 
        return df
    
    #creo un dataframe a partire dalla lista
    df_new = pd.DataFrame(lista, columns=['tipo', 'energia'])

    #controllo i due dataframe per un corretto funzionamento di concat
    df_new = df_new.dropna(how='all') #elimino le righe contenenti NaN
    df_new = df_new.dropna(axis=1, how='all') #elimino le colonne contenenti NaN
    df = df.dropna(how='all') #elimino le righe contenenti NaN
    df = df.dropna(axis=1, how='all') #elimino le colonne contenenti NaN

    return pd.concat([df, df_new], ignore_index=True)

def genera_particella_iniziale(E0):
    """
    funzione genera_particella_iniziale(E0) che genera in modo casuale la particella iniziale, scegliendo tra 
    elettrone, positrone, fotone.

    E0: energia iniziale della particella

    return particella: una tupla dove si specifica il tipo e l'energia della particella iniziale
    """
    tipo= np.random.choice(['elettrone', 'positrone', 'fotone'])
    particella = (tipo, E0)
    return particella


def simulazione_sciame(E0, s=0.1, angolo=0):
    """
    Funzione simulazione_sciame(E0, s=0.1, angolo=0) che simula uno sciame di particelle

    E0: energia iniziale particella (MeV)
    s=0.1: passo di avanzamento della simulazione in frazione di X0 (compreso tra 0 e 1), 0.1 è il valore di default
    angolo=0: angolo di inclinazione rispetto alla verticale della particella iniziale (si ritiene lo stesso anche per le particelle secondarie). 
    0 gradi è il valore di default

    return particelle_rivelate: numero di particelle rivelate dal rivelatore
    """

    quota = quotainiz
    spost_vert = s*np.cos(np.deg2rad(angolo))*X0

    sciame = pd.DataFrame( columns=['tipo', 'energia']) #creo il df contenente lo sciame
    primapart = genera_particella_iniziale(E0) #genero casualmente la particella iniziale
    sciame= aggiungi_part(sciame, [primapart]) #aggiungo la prima particella allo sciame
    
    while quota > quotariv and len(sciame)!=0:

        #inizializzo una lista per memorizzare le tuple contenenti le particelle nuove ottenute dai vari processi
        new_particelle = []

        #resetto l'indice per sicurezza all'inizio di ogni iterazione del ciclo while
        sciame = sciame.reset_index(drop=True)
        #creo una lista per memorizzare le tuple (indice,nuovi valori energie delle particelle)
        new_energie= [] 
        #ciclo for sulle righe del dataframe sciame come se fossero tuple
        for particella in sciame.itertuples():
            index = particella.Index  # Indice della riga
            energy = particella.energia  # Energia della particella
            tipo = particella.tipo   # Tipo della particella

            if tipo in ['elettrone', 'positrone']:                
                if tipo =='elettrone':
                    #associo la corrispondente energia critica
                    Ec=Ec_elet
                else:
                    #associo la corrispondente energia critica
                    Ec=Ec_pos
                
                if energy > min_ioniz*s*X0 :
                    en_dimin= energy - min_ioniz * s * X0
                    E_fin = en_dimin #introduco questa variabile per tenere conto dei cambiamenti dell'energia
                else:
                    #pongo E_fin=0 così da usare questa condizione per eliminare la particella alla fine
                    E_fin=0
                    

                if np.random.uniform() < prob_brems(s) and E_fin>Ec:
                    E_fin=E_fin/2
                    new_particelle.append(("fotone", E_fin))

                new_energie.append((index, E_fin))
            
            if tipo == 'fotone':
                if energy > en_coppia:
                    if np.random.uniform() < prob_coppia(s):
                        #pongo energy=0 così da usare questa condizione per eliminare il fotone alla fine
                        new_energie.append((index, 0))
                        new_particelle.append(("elettrone", energy/2)) 
                        new_particelle.append(("positrone", energy/2))     
                else:
                    new_energie.append((index, 0))
        
        #associo i nuovi valori delle energie
        for i, en in new_energie:
            sciame.at[i, 'energia'] = en

        #elimino le particelle con energia=0
        sciame.drop(sciame[sciame['energia'] == 0].index, inplace=True)

        #aggiungo le nuove particelle
        sciame= aggiungi_part(sciame, new_particelle)
        
        #diminuisco la quota 
        quota-= spost_vert

    #determino il numero delle particelle rivelate
    particelle_rivelate = len(sciame)

    return particelle_rivelate



            
            




            

              
            
            
  

   

