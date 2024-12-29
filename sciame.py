import numpy as np
import pandas as pd
import argparse

#definizione costanti usate 

X0 = 7e2 # lunghezza di radiazione (m)
quotainiz = 2e4 # quota iniziale sciame (m)
quotariv = 4e3 # quota rivelatore (m)
Ec_elet = 87.92 # energia critica elettroni (MeV)
Ec_pos = 85.97 # energia critica positroni (MeV)
m_e = 0.51 # (MeV/c**2)
c = 3e8 # (m/s)
en_coppia = 2*m_e*c**2 # energia legata alla produzione di coppie (MeV)
min_ioniz = 2.187e-1 # minimo di ionizzazione (MeV/m)


#definizioni funzioni usate
def parse_arguments():

    parser = argparse.ArgumentParser(description='Scelta particella iniziale',
                                     usage      ='python3 sciame.py  --option')
    parser.add_argument('--fotone',   action='store_true',    help='particella iniziale fotone')
    parser.add_argument('--positrone',  action='store_true',    help='particella iniziale positrone')
    parser.add_argument('--elettrone', action='store_true',    help='particella iniziale elettrone')
    
    return  parser.parse_args()

def prob_bremsel(s):
    """
    funzione prob_bremsel(s) per determinare la probabilità che l'elettrone
    interagisca per Bremsstrahlung  
    s: passo di avanzamento della simulazione in frazioni di X0 (compreso tra 0 e 1)

    probabilità= 1-np.exp(-s)

    return probabilità: valore della probabilità del processo
    """   
    probabilità = 1-np.exp(-s)
    return probabilità

def prob_bremspos(s):
    """
    funzione prob_bremspos(s) per determinare la probabilità che il positrone
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

def perdita_ionizzazione(s, E):
    """
    funzione perdita_ionizzazione(s,E) per determinare l'energia residua 
    dopo il processo di ionizzazione di e+ o e-
    s: passo di avanzamento della simulazione in frazioni di X0 (compreso tra 0 e 1)
    E: energia della particella prima del processo
    en_residua=E-min_ioniz*s 

    return en_residua: energia della particella dopo il processo
    """
    en_residua = E - min_ioniz*s
    return en_residua

def aggiungi_part(df, t, E):
    """
    funzione per aggiungere una nuova particella al dataframe dello sciame
    df: dataframe
    t: tipo di particelle (elettrone, positrone, fotone)
    E: energia della particella

    return part: dataframe part con le particelle aggiornate
    """
    nuova_particella = pd.Series({'tipo': t, 'energia': E})

    df = df.append(nuova_particella, ignore_index=True)
    return df

def genera_particella_iniziale():
    """
    funzione che genera in modo casuale la particella iniziale, scegliendo tra 
    elettrone, positrone, fotone
    """
    return np.random.choice(['elettrone', 'positrone', 'fotone'])


def simulazione_sciame(E0, s, angolo):
    """
    Funzione che simula uno sciame di particelle

    E0: energia iniziale particella (MeV)
    s: passo di avanzamento della simulazione in frazione di X0 (compreso tra 0 e 1)
    """

    quota = quotainiz
    spost_vert = s*np.cos(np.deg2rad(angolo))

    sciame = pd.DataFrame( columns=['tipo', 'energia'])
    primapart = genera_particella_iniziale() #genero casualmente la particella iniziale
    aggiungi_part(sciame, primapart, E0)

    while quota > quotariv and len(sciame)!=0:
        for index, particella in sciame.iterrows():
            E = particella['energia']
            tipo = particella['tipo']

            if tipo in ['elettrone', 'positrone']:                
                if tipo =='elettrone':
                    Ec=Ec_elet
                else:
                    Ec=Ec_pos

                if np.random.uniform() < prob_bremsel and E>Ec:
                    E=E/2
                    aggiungi_part(sciame,'fotone',E)
                
                if E > min_ioniz*s :
                    E= perdita_ionizzazione(s, E)
                else:
                    print('Elimino la particella con le seguenti caratteristiche:\n{:s} - {:d} MeV\nperchè non rispetta i requisiti energetici'.format(particella['tipo'], particella['energia']))
                    sciame = sciame.drop(index)
            
            if tipo == 'fotone':
                if E > en_coppia:
                    if np.random.uniform() < prob_coppia(s):
                        aggiungi_part(sciame, 'elettrone', E/2)
                        aggiungi_part(sciame, 'positrone', E/2)
                else:
                    print('Elimino il fotone con energia di {:d} MeV,  perchè non rispetta i requisiti energetici'.format(particella['energia']))
                    sciame = sciame.drop(index)
            
        quota-= spost_vert

    particelle_rivelate = len(sciame)



            
            




            

              
            
            
  

   

