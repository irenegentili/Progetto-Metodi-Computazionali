import numpy as np
import pandas as pd
import argparse
import sciame as sa
import matplotlib.pyplot  as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import ScalarFormatter
import tqdm 
import time

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

    args=parse_arguments()

    E_min = 1e3  # Energia minima (1 TeV =1e3 MeV)
    E_max = 100e3  # Energia massima (100 TeV = 100e3 MeV)
    ang_max=45
    ang_min=0

    if args.hisen == True:
        energie = np.linspace(E_min, E_max, 25)
        angoli = [0, 5, 10, 30, 45]#5 valori tra 0 e 45 gradi

        df_risultati = pd.DataFrame([(e, a) for e in energie for a in angoli], columns=['energia', 'angolo'])
        df_risultati['num particelle rivelate'] = df_risultati.apply(lambda x: sa.simulazione_sciame(x['energia'], angolo=x['angolo']), axis=1)
        
        print(df_risultati['num particelle rivelate'])

        fig =plt.figure()
        ax= fig.add_subplot(projection ='3d')

        for i, angolo in enumerate(angoli):
            ang = df_risultati.loc[df_risultati['angolo']== angolo] #dataframe per i valori relativi a quell'angolo
            ax.bar3d(ang['energia'], [angolo] * len(ang['energia']), np.zeros(len(ang['energia'])),
                dx=np.full(len(ang['energia']),750), dy=np.full(len(ang['angolo']), 4),
                    dz=ang['num particelle rivelate'], color=colori[i], alpha=0.6)
        ax.set_xlabel('Energia (MeV)')
        ax.set_ylabel('angoli (°)')
        ax.set_zlabel('numero particelle rivelate')
        ax.set_title('Risposta del rivelatore in funzione dell\'energia per diversi angoli')
        ax.set_yticks(angoli)
        # Formattazione dell'asse X (energia) con notazione scientifica
        ax.xaxis.set_major_formatter(ScalarFormatter())
        ax.xaxis.get_major_formatter().set_powerlimits((0, 1)) # Usa notazione scientifica per valori grandi
        plt.show() 

        for i, angolo in enumerate(angoli):
            ang = df_risultati.loc[df_risultati['angolo']== angolo]
            n,_, _= plt.hist (ang['energia'], bins=20, weights = ang['num particelle rivelate'], range=(1e3 -5, 100e3 +5), color=colori[i], alpha=0.5, label=f'Angolo={angolo}°' )
        plt.xlabel('Energia (MeV)')
        plt.ylabel('Numero particelle rivelate')
        plt.title('Risposta del rivelatore in funzione dell\'energia per diversi angoli')
        plt.legend()
        plt.show()

   
    if args.hisang == True:
        angoli= np.linspace(ang_min, ang_max, 25)
        energie=np.linspace(E_min, E_max, 5)

        df_risultati = pd.DataFrame([(a,e) for a in angoli for e in energie], columns=['angolo', 'energia'])
        df_risultati['num particelle rivelate'] = df_risultati.apply(lambda x: sa.simulazione_sciame(x['energia'], angolo=x['angolo']), axis=1)
        
        print(df_risultati['num particelle rivelate'])

        fig =plt.figure()
        ax= fig.add_subplot(projection ='3d')

        for i, energia in enumerate(energie):
            en = df_risultati.loc[df_risultati['energia']== energia] #dataframe per i valori relativi a quell'energia
            ax.bar3d(en['angolo'], [energia] * len(en['angolo']), np.zeros(len(en['angolo'])),
                dx=np.full(len(en['angolo']), 5), dy=np.full(len(en['energia']),3),
                    dz=en['num particelle rivelate'], color=colori[i], alpha=0.6)
        ax.set_xlabel('Angoli (°)')
        ax.set_ylabel('Energia (MeV)')
        ax.set_zlabel('numero particelle rivelate')
        ax.set_title('Risposta del rivelatore in funzione dell\'angolo per diversi valori di energia')
        ax.set_yticks(energie)
        # Formattazione dell'asse y (energia) con notazione scientifica
        ax.yaxis.set_major_formatter(ScalarFormatter())
        ax.yaxis.get_major_formatter().set_powerlimits((0, 1)) # Usa notazione scientifica per valori grandi
        plt.show() 

        for i, energia in enumerate(energie):
            en = df_risultati.loc[df_risultati['energia']== energia] #dataframe per i valori relativi a quell'energia
            n,_, _= plt.hist (en['angolo'], bins=30, weights = en['num particelle rivelate'], range=(-2,47), color=colori[i], alpha=0.5, label=f'Energia={energia} MeV' )
        plt.xlabel('Angoli (°)')
        plt.ylabel('Numero particelle rivelate')
        plt.title('Risposta del rivelatore in funzione dell\'angolo per diversi valori di energia')
        plt.legend()
        plt.show()

    
    if args.treD == True:
        angoli = np.linspace(ang_min, ang_max, 10)      
        energie = np.linspace(E_min, E_max, 10)


        df_risultati = pd.DataFrame([(a, e) for a in angoli for e in energie], columns=['angolo', 'energia'])
        df_risultati['num particelle rivelate'] = df_risultati.apply(lambda x: sa.simulazione_sciame(x['energia'], angolo=x['angolo']), axis=1)   
        print(df_risultati['num particelle rivelate'])


        sc=plt.scatter(df_risultati['energia'], df_risultati['angolo'], marker='o', c=df_risultati['num particelle rivelate'], cmap='viridis')
        plt.xlabel('Energia (MeV)')
        plt.ylabel('Angolo (°)')
        plt.title('Numero di particelle rivelate in funzione dell\'energia e dell\'angolo')
        cbar = plt.colorbar(sc)
        cbar.set_label('Numero di particelle rivelate')
        plt.show()


    

if __name__ == "__main__":

    analisi_sciame()


