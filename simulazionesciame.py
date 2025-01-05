import numpy as np
import pandas as pd
import argparse
import sciame as sa
import matplotlib.pyplot  as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import ScalarFormatter
from tqdm.auto import tqdm
import time

tqdm.pandas()

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "serif",
    "font.serif": ["Latin Modern Roman"],
    "font.size": 12,
    "axes.titlesize": 16,  
    "axes.labelsize": 12,
    "xtick.labelsize": 10, 
    "ytick.labelsize": 10, 
}) 

def parse_arguments():

    parser = argparse.ArgumentParser(description='Scelta analisi dati',
                                     usage      ='python3 sciame.py  --option')
    parser.add_argument('--hisen',   action='store_true',    help='istogramma energia ad angoli fissati')
    parser.add_argument('--hisang',  action='store_true',    help='istogramma angoli ad energie fissate')
    parser.add_argument('--treD', action='store_true',    help='grafico 3D energia-angoli-numero particelle')
    
    return  parser.parse_args()

#colori da usare nei grafici
colori=['deeppink', 'darkgreen',  'sandybrown', 'darkviolet','navy', 'crimson','maroon', 'coral', 'orange']

def analisi_sciame():
    """
    funzione che simula lo sciame per varie configurazioni di energia-angolo e ne rappresenta graficamente le proprietà.

    - grafico num particelle rivelate in funzione dell'energia per 4 angoli differenti
    - grafico num particelle rivelate in funzione dell'angolo per 4 valori di energia differenti

    """

    args=parse_arguments()

    E_min = 1e6  # Energia minima (1 TeV =1e6 MeV)
    E_max = 1e8  # Energia massima (100 TeV = 1e8 MeV)
    ang_max=45 #(°)
    ang_min=0 #(°)

    if args.hisen == True:

        n=int(input('Scegliere il numero di valori di energia con cui fare la simulazione per ognuno degli angoli considerati: [0°,15°,30°,45°]. \n(I valori di energia e di angolo sono uniformemente spaziati tra i valori massimi e minimi considerati)') )
        energie = np.linspace(E_min, E_max, n)
        angoli = [ang_min, 15, 30, ang_max]#4 valori tra 0 e 45 gradi

        

        s = float(input('inserire il valore del passo (s) in frazioni di X0 (valore compreso tra 0 e 1)'))
        if not (s>=0 and s>=1):
            print('inserire un valore di s compreso tra 0 e 1')

        print(f'simulazione effettuata per {n} valori di energia E (MeV), {E_min}<E<{E_max} e 4 valori di angoli (°) compresi tra {ang_min} e {ang_max}, con passo {s}')
        #creo il dataframe per contenere i risultati della simulazione
        df_risultati = pd.DataFrame(index=pd.MultiIndex.from_product([energie, angoli], names=['energia', 'angolo'])).reset_index()
        
        #per ogni coppia energia-angolo riempio il dataframe con il numero di particelle rivelate e la quota minima raggiunta
        df_risultati[['num particelle rivelate', 'quotamin']] = pd.DataFrame(df_risultati.progress_apply(lambda x: sa.simulazione_sciame(x['energia'], s, x['angolo']), axis=1).tolist())

        
        print('il numero di particelle rivelate e la quota minima raggiunta per ogni coppia energia-angolo è:')
        for _,row in df_risultati.iterrows():
            print(f"Energia iniziale {row['energia']}, Angolo: {row['angolo']}, numero particelle rivelate: {row['num particelle rivelate']}, quota minima: {row['quotamin']}")

        #istogramma 3D e 2D
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,6), subplot_kw={'projection':'3d'})

        for i, angolo in enumerate(angoli):
            ang = df_risultati.loc[df_risultati['angolo']== angolo] #dataframe per i valori relativi a quell'angolo
            ax1.bar3d(ang['energia'], [angolo] * len(ang['energia']), np.zeros(len(ang['energia'])),
                dx=np.full(len(ang['energia']),750), dy=np.full(len(ang['angolo']), 4),
                    dz=ang['num particelle rivelate'], color=colori[i], alpha=0.6)
            
            ax2.hist (ang['energia'], bins=20, weights = ang['num particelle rivelate'], range=(1e3 -5, 100e3 +5), color=colori[i], alpha=0.5, label=f'Angolo={angolo}°' )

        ax1.set_xlabel('Energia (MeV)')
        ax1.set_ylabel('angoli (°)')
        ax1.set_zlabel('numero particelle rivelate')
        ax1.set_title('Risposta del rivelatore in funzione dell\'energia per diversi angoli rispetto alla verticale ')
        ax1.set_yticks(angoli)
        # Formattazione dell'asse X (energia) con notazione scientifica
        ax1.xaxis.set_major_formatter(ScalarFormatter())
        ax1.xaxis.get_major_formatter().set_powerlimits((0, 1)) # Usa notazione scientifica per valori grandi
   
        ax2.set_xlabel('Energia (MeV)')
        ax2.set_ylabel('Numero particelle rivelate')
        ax2.set_title('Risposta del rivelatore in funzione dell\'energia per diversi angoli rispetto alla verticale ')
        ax2.legend()
        plt.show()

        #plot quota-energia
        for i, angolo in enumerate(angoli):
            ang = df_risultati.loc[df_risultati['angolo']== angolo]
            plt.plot(ang['energia'], ang['quotamin'], color=colori[i], label=f'Angolo={angolo}°' )
        plt.xlabel('Energia (MeV)')
        plt.ylabel('quota minima (cm)')
        plt.title('Quota raggiunta in funzione dell\'energia iniziale per diversi angoli rispetto alla verticale')
        plt.legend()
        plt.show()
   
    if args.hisang == True:
        n=int(input('Scegliere il numero di angoli con cui fare la simulazione per ognuno dei 4 valori di energia. \n(I valori di energia e di angolo sono uniformemente spaziati nell\'intervallo tra valore minimo e massimo considerato)') )
        angoli= np.linspace(ang_min, ang_max, n)
        energie=np.linspace(E_min, E_max, 4)
        

        s = float(input('inserire il valore del passo (s) in frazioni di X0 (valore compreso tra 0 e 1)'))
        if not (s>=0 and s>=1):
            print('inserire un valore di s compreso tra 0 e 1')

        print(f'simulazione effettuata per {n}6 angoli(°) compresi tra {ang_min} e {ang_max} e 4 valori di energia E (MeV), {E_min}<E<{E_max}, con passo {s}')
        #creo il dataframe per contenere i risultati della simulazione
        df_risultati = pd.DataFrame(index=pd.MultiIndex.from_product([energie, angoli], names=['energia', 'angolo'])).reset_index()
        
        #per ogni coppia energia-angolo riempio il dataframe con il numero di particelle rivelate e la quota minima raggiunta
        df_risultati[['num particelle rivelate', 'quotamin']] = pd.DataFrame(df_risultati.progress_apply(lambda x: sa.simulazione_sciame(x['energia'], s, x['angolo']), axis=1).tolist())

        print('il numero di particelle rivelate e la quota minima raggiunta per ogni coppia angolo-energia è:')
        for _, row in df_risultati.iterrows():
            print(f"Angolo {row['angolo']}, Energia: {row['energia']}, numero particelle rivelate: {row['num particelle rivelate']}, quota minima: {row['quotamin']}")
        
        #istogramma 3D e 2D
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12,6), subplot_kw={'projection':'3d'})

        for i, energia in enumerate(energie):
            en = df_risultati.loc[df_risultati['energia']== energia] #dataframe per i valori relativi a quell'angolo
            ax1.bar3d(en['angolo'], [energia] * len(ang['angolo']), np.zeros(len(en['angolo'])),
                dx=np.full(len(en['angolo']),10), dy=np.full(len(en['energia']), 750),
                    dz=en['num particelle rivelate'], color=colori[i], alpha=0.6)
            
            ax2.hist (en['angolo'], bins=5, weights = ang['num particelle rivelate'], range=(-2, 47), color=colori[i], alpha=0.5, label=f'Energia={energia}MeV' )

        ax1.set_xlabel('Angolo (°)')
        ax1.set_ylabel('Energia (MeV)')
        ax1.set_zlabel('numero particelle rivelate')
        ax1.set_title('Risposta del rivelatore in funzione dell\'angolo rispetto alla verticale per diversi valori di energia  ')
        ax1.set_yticks(angoli)
        # Formattazione dell'asse X (energia) con notazione scientifica
        ax1.xaxis.set_major_formatter(ScalarFormatter())
        ax1.xaxis.get_major_formatter().set_powerlimits((0, 1)) # Usa notazione scientifica per valori grandi
   
        ax2.set_xlabel('Angolo (°)')
        ax2.set_ylabel('Numero particelle rivelate')
        ax2.set_title('Risposta del rivelatore in funzione dell\'angolo rispetto alla verticale per diversi valori di energia  ')
        ax2.legend()
        plt.show()

        #plot quota minima-angolo
        for i, energia in enumerate(energie):
            en = df_risultati.loc[df_risultati['energia']== energia]
            plt.plot(en['angolo'], en['quotamin'], color=colori[i], label=f'Energia={energia}MeV' )
        plt.xlabel('Angolo (°)')
        plt.ylabel('Quota minima (cm)')
        plt.title('Quota raggiunta in funzione dell\'angolo rispetto alla verticale per diversi valori di energia')
        plt.legend()
        plt.show()

    if args.treD == True:
        n=int(input('scegliere il numero di valori di energia e angolo da considerare nella simulazione. \n(I valori di energia e di angolo sono uniformemente spaziati nell\'intervallo tra valore minimo e massimo considerato)'))
        angoli = np.linspace(ang_min, ang_max, n)      
        energie = np.linspace(E_min, E_max, n)

        s = float(input('inserire il valore del passo (s) in frazioni di X0 (valore compreso tra 0 e 1)'))
        if not (s>=0 and s>=1):
            print('inserire un valore di s compreso tra 0 e 1')

        print(f'simulazione effettuata per {n} valori di energia E(MeV), {E_min}<E{E_max} e angolo (°) compresi tra {ang_min} e {ang_max}, con passo {s}')
        #creo il dataframe per contenere i risultati della simulazione
        df_risultati = pd.DataFrame(index=pd.MultiIndex.from_product([energie, angoli], names=['energia', 'angolo'])).reset_index()
        
        #per ogni coppia energia-angolo riempio il dataframe con il numero di particelle rivelate e la quota minima raggiunta
        df_risultati[['num particelle rivelate', 'quotamin']] = pd.DataFrame(df_risultati.progress_apply(lambda x: sa.simulazione_sciame(x['energia'], angolo=x['angolo']), axis=1).tolist())

        print('il numero di particelle rivelate e la quota minima raggiunta per ogni coppia angolo-energia è:')
        for index, row in df_risultati.iterrows():
            print(f"Angolo {row['angolo']}, Energia: {row['energia']}, numero particelle rivelate: {row['num particelle rivelate']}, quota minima: {row['quotamin']}")
        

        sc=plt.scatter(df_risultati['energia'], df_risultati['angolo'], marker='o', c=df_risultati['num particelle rivelate'], cmap='viridis')
        plt.xlabel('Energia (MeV)')
        plt.ylabel('Angolo (°)')
        plt.title('Numero di particelle rivelate in funzione dell\'energia e dell\'angolo')
        cbar = plt.colorbar(sc)
        cbar.set_label('Numero di particelle rivelate')
        plt.show()

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        sc= ax.scatter(df_risultati['energia'], df_risultati['angolo'], df_risultati['quota'], c=df_risultati['num particelle rivelate'], cmap='plasma', s=30)
        ax.set_xlabel('Energia (MeV)')
        ax.set_ylabel('Angolo (°)')
        ax.set_zlabel('Quota (cm)')
        ax.set_title('Quota e numero di particelle in funzione di energia e angolo')
        ax.xaxis.set_major_formatter(ScalarFormatter())
        ax.xaxis.get_major_formatter().set_powerlimits((0, 1)) 
        cbar = plt.colorbar(sc)
        cbar.set_label('Numero di Particelle')
        plt.show()


if __name__ == "__main__":

    analisi_sciame()


