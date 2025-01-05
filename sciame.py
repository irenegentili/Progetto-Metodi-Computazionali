import numpy as np
import pandas as pd

#definizione costanti usate 

X0 = 7e4 # lunghezza di radiazione (cm)
quotainiz = 2e6 # quota iniziale sciame (cm)
quotariv = 4e5 # quota rivelatore (cm)
Ec_elet = 87.92 # energia critica elettroni (MeV)
Ec_pos = 85.97 # energia critica positroni (MeV)
c = 3e10 # (cm/s)
m_e = 0.51/c**2 #(MeV(c**2)
en_coppia = 2*m_e*c**2 # energia legata alla produzione di coppie (MeV)
min_ioniz = 2.187e-3 # minimo di ionizzazione (MeV/cm)


#definizioni funzioni usate
def prob_brems(s):
    """
    funzione prob_brems(s) per determinare la probabilità che l'elettrone o il positrone
    interagisca per Bremsstrahlung  
    s: passo di avanzamento della simulazione in frazioni di X0 (compreso tra 0 e 1)

    probabilità= 1-np.exp(-s)

    return probabilità: valore della probabilità del processo
    """   
    probabilità = 1-np.exp(-s)
    return probabilità

def prob_coppia(s):

    """
    funzione prob_coppia(s) per determinare la probabilità della produzione di coppie 
    del fotone
    s: passo di avanzamento della simulazione in frazioni di X0 (compreso tra 0 e 1)

   probabilità= 1-np.exp(-7*s/9)

    return probabilità: valore della probabilità del processo
    """
    probabilità = 1-np.exp(-7*s/9)
    
    return probabilità

def perdita_ionizzazione(index, df, s):
    """
    funzione perdita_ionizzazione(s,E) per determinare l'energia residua 
    dopo il processo di ionizzazione di e+ o e-
    index: indice della particella
    df: dataframe con le particelle dello sciame
    s: passo di avanzamento della simulazione in frazioni di X0 (compreso tra 0 e 1)
    """
    df.loc[index, 'energia'] = float(df.loc[index, 'energia']) - min_ioniz * s * X0
    return df

def aggiungi_part(df, dict):
    """
    funzione per aggiungere una nuova particella al dataframe dello sciame
    df: dataframe
    dict: lista di dizionari contenente le nuove particelle

    return dataframe con le particelle aggiornate
    """
    new_df = pd.DataFrame(dict)  # Creo un DataFrame dai dizionari
    return pd.merge(df, new_df, how='outer')

def genera_particella_iniziale(E0):
    """
    funzione che genera in modo casuale la particella iniziale, scegliendo tra 
    elettrone, positrone, fotone.

    return particella: un dizionario dove si specifica il tipo e l'energia della particella iniziale
    """
    tipo= np.random.choice(['elettrone', 'positrone', 'fotone'])
    particella = {'tipo':tipo,'energia': E0 }
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

    sciame = pd.DataFrame( columns=['tipo', 'energia'])
    primapart = genera_particella_iniziale(E0) #genero casualmente la particella iniziale
    sciame= aggiungi_part(sciame, [primapart])

    while quota > quotariv and len(sciame)!=0:

        #creo una lista per memorizzare le particelle ottenute dai vari processi
        new_particelle= [] 

        #creo una lista di particelle da eliminare
        drop_particelle=[]

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
                    print(f"Elimino {tipo} con energia {E:.2f} MeV perchè E<E_min *s*X0 con E_min pari all'energia di Minimum ionization (MeV/cm) ")
                    drop_particelle.append(index)

                if np.random.uniform() < prob_brems(s) and E>Ec:
                    sciame.loc[index, 'energia'] = float(sciame.loc[index, 'energia'])/2
                    new_particelle.append({'tipo': 'fotone', 'energia': E/2})


            
            if tipo == 'fotone':
                if E > en_coppia:
                    if np.random.uniform() < prob_coppia(s):
                        drop_particelle.append(index)
                        new_particelle.append({'tipo': 'positrone', 'energia': float(E)/2})
                        new_particelle.append({'tipo': 'elettrone', 'energia': float(E)/2})
                else:
                    print(f"Elimino {tipo} con energia {E:.2f} MeV perchè  E < 2*m_e *c^2")
                    drop_particelle.append(index)
        sciame = sciame.drop(drop_particelle, axis=0)
        if new_particelle:
            sciame= aggiungi_part(sciame, new_particelle)
        print(sciame)
        
        quota=float(quota) - spost_vert

    particelle_rivelate = len(sciame)
    return particelle_rivelate



            
            




            

              
            
            
  

   

