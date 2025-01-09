import numpy as np
import pandas as pd

#definizione costanti usate 

X0 = 7e4 # lunghezza di radiazione (cm)
quotainiz = 2.0e6 # quota iniziale sciame (cm)
quotariv = 4.0e5 # quota rivelatore (cm)
Ec_elet = 87.92 # energia critica elettroni (MeV)
Ec_pos = 85.97 # energia critica positroni (MeV)
c = 3.0e10 # (cm/s)
Er= 0.51 #( energia a riposo elettrone e positrone MeV)
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

def perdita_ionizzazione(index, df, s):
    """
    funzione perdita_ionizzazione(s,E) per determinare l'energia residua 
    dopo il processo di ionizzazione di e+ o e-
    index: indice della particella nel dataframe
    df: dataframe con le particelle dello sciame
    s: passo di avanzamento della simulazione in frazioni di X0 (compreso tra 0 e 1)
    """
    df.loc[index, 'energia'] = df.loc[index, 'energia'] - min_ioniz * s * X0
    return df

def aggiungi_part(df, dict):
    """
    funzione per aggiungere una nuova particella al dataframe dello sciame
    df: dataframe
    dict: lista di dizionari contenente le nuove particelle

    return dataframe con le particelle aggiornate
    """
    new_df = pd.DataFrame(dict)  # Creo un DataFrame dalla lista di dizionari
    return pd.merge(df, new_df, how='outer')

def genera_particella_iniziale(E0):
    """
    funzione che genera in modo casuale la particella iniziale, scegliendo tra 
    elettrone, positrone, fotone.

    E0: energia iniziale della particella

    return particella: un dizionario dove si specifica il tipo e l'energia della particella iniziale
    """
    tipo= np.random.choice(['elettrone', 'positrone', 'fotone'])
    particella = {'tipo':tipo,'energia': E0}
    return particella


def simulazione_sciame(E0, s=0.1, angolo=0):
    """
    Funzione che simula uno sciame di particelle

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

        #creo una lista per memorizzare le particelle nuove ottenute dai vari processi
        new_particelle= [] 

        sciame = sciame.reset_index(drop=True)

        for index, particella in sciame.iterrows():
            E = particella['energia']
            tipo = particella['tipo']

            if tipo in ['elettrone', 'positrone']:                
                if tipo =='elettrone':
                    #associo la corrispondente energia critica
                    Ec=Ec_elet
                else:
                    #associo la corrispondente energia critica
                    Ec=Ec_pos

                if E > min_ioniz*s*X0 :
                    sciame= perdita_ionizzazione(index, sciame, s)
                else:
                    sciame.loc[index, 'energia'] = 0

                if np.random.uniform() < prob_brems(s) and E>Ec:
                    sciame.loc[index, 'energia'] = sciame.loc[index, 'energia']/2
                    new_particelle.append({'tipo': 'fotone', 'energia': E/2})


            
            if tipo == 'fotone':
                if E > en_coppia:
                    if np.random.uniform() < prob_coppia(s):
                        sciame.loc[index, 'energia'] = 0 
                        new_particelle.append({'tipo': 'positrone', 'energia': E/2})
                        new_particelle.append({'tipo': 'elettrone', 'energia': E/2})
                else:
                    sciame.loc[index, 'energia'] = 0 

        sciame = sciame.loc[sciame['energia'] > 0]

        if new_particelle:
            sciame= aggiungi_part(sciame, new_particelle)
        
        quota-= spost_vert

    particelle_rivelate = len(sciame)

    return particelle_rivelate



            
            




            

              
            
            
  

   

