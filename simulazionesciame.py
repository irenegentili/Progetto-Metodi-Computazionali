import numpy as np
import pandas as pd
import argparse
import sciame as sa
import matplotlib.pyplot  as plt
#from mpl_toolkits.mplot3d import Axes3D
from matplotlib.ticker import ScalarFormatter
from tqdm.auto import tqdm
from scipy.interpolate import griddata

tqdm.pandas()


def parse_arguments():

    parser = argparse.ArgumentParser(description='Scelta analisi dati',
                                     usage      ='python3 sciame.py  --option')
    parser.add_argument('--hisen',   action='store_true',    help='istogramma numero particelle - energia ad angoli fissati')
    parser.add_argument('--hisang',  action='store_true',    help='istogramma numero di particelle - angoli ad energie fissate')
    parser.add_argument('--color', action='store_true',    help='grafico con gradiente di colore energia-angoli-numero particelle')
    
    return  parser.parse_args()

#colori da usare nei grafici
colori=['deeppink', 'darkgreen',  'navy', 'maroon']

def analisi_sciame():
    """
    funzione che simula lo sciame per varie configurazioni di energia-angolo e ne rappresenta graficamente i risultati.

    --hisen: istogramma num particelle rivelate- energia per 4 angoli 
    --hisang: istogramma num particelle rivelate - angolo per 4 energie
    --color: grafico scatter e contourf numero di particelle per le varie coppie energia-angolo

    """

    args=parse_arguments()

    E_min = 1.0e6  # Energia minima (1 TeV =1e6 MeV)
    E_max = 1.0e8  # Energia massima (100 TeV = 1e8 MeV)
    ang_max=45 #(°)
    ang_min=0 #(°)



    if args.hisen == True:

        #simulazione e raccolta dati
        print(f'Simulazione sciame in funzione dell\'energia iniziale E e dell\'angolo rispetto alla verticale θ con {E_min:.1e} MeV<E<{E_max:.1e} MeV e {ang_min}°<θ<{ang_max}°')

        n=int(input('Scegliere il numero di valori di E da considerare per ognuno dei 4 valori di θ considerati. (I valori sono uniformemente spaziati tra i valori massimi e minimi considerati)  ' ))
        
        energie = np.linspace(E_min, E_max, n)
        angoli = np.linspace(ang_min, ang_max, 4)

        s = float(input('Inserire il valore del passo di avanzamento (s) in frazioni di X0 (valore compreso tra 0 e 1)  '))
        while not (s>=0 and s<=1):
            s= float(input('Inserire un valore di s compreso tra 0 e 1  '))
        
        save= input('Prima di iniziare la simulazione scegliere se salvare o meno il grafico prodotto (Yes or No) ')
        while save != 'Yes' and save !='No':
            save= input('Scegliere se salvare o meno il grafico prodotto digitando Yes or No ')   

        print(f'Inizio simulazione per {n} valori di E per ogni θ con passo {s}')

        #creo il dataframe per contenere i risultati della simulazione
        df_risultati = pd.DataFrame(index=pd.MultiIndex.from_product([energie, angoli], names=['energia', 'angolo'])).reset_index()
        
        #per ogni coppia energia-angolo riempio il dataframe con una colonna con il numero di particelle rivelate
        df_risultati['num particelle rivelate'] = pd.DataFrame(df_risultati.progress_apply(lambda x: sa.simulazione_sciame(x['energia'], s, x['angolo']), axis=1))

        
        print('il numero di particelle rivelate per ogni coppia E-θ è:')

        print(f"{'E (MeV)':<10}{'θ (°)':<6}{'Numero particelle rivelate':<30}")
        for _,row in df_risultati.iterrows():
            print(f"{int(row['energia']):<.2e}  {int(row['angolo']):<6} {int(row['num particelle rivelate']):<30}")
        
        fig1 = plt.figure(figsize=plt.figaspect(0.5))
        ax1 = fig1.add_subplot(1, 2, 1, projection='3d')
        ax2 = fig1.add_subplot(1, 2, 2)
        fig1.subplots_adjust(wspace=0.5)
 
        for i, angolo in enumerate(angoli):
            ang = df_risultati.loc[df_risultati['angolo']== angolo] #dataframe per i valori relativi a quell'angolo

            ax1.bar3d(ang['energia'], [angolo] * len(ang['energia']), np.zeros(len(ang['energia'])), dx=np.full(len(ang['energia']),550), dy=np.full(len(ang['angolo']), 3),
                    dz=ang['num particelle rivelate'], color=colori[i], alpha=0.6)
            
            ax2.hist (ang['energia'], bins=25, weights = ang['num particelle rivelate'], range=(1e6-5, 1e8 +5), color= colori[i], alpha=0.5, label=fr'$\theta$={angolo}°' )

        ax1.set_xlabel('E (MeV)')
        ax1.set_ylabel(r'$\theta$ (°)')
        ax1.set_zlabel('numero\nparticelle rivelate', labelpad=20)
        ax1.set_yticks(angoli)
        ax1.xaxis.set_major_formatter(ScalarFormatter())
        ax1.xaxis.get_major_formatter().set_powerlimits((0, 1))
        #ax1.zaxis.set_major_formatter(ScalarFormatter()) 
        #ax1.zaxis.get_major_formatter().set_powerlimits((0, 1))
   
        ax2.set_xlabel('E (MeV)')
        ax2.set_ylabel('Numero particelle rivelate')
        ax2.yaxis.set_label_position('right')
        ax2.yaxis.tick_right()
        ax2.xaxis.set_major_formatter(ScalarFormatter())
        ax2.xaxis.get_major_formatter().set_powerlimits((0, 1))
        ax2.yaxis.set_major_formatter(ScalarFormatter())
        ax2.yaxis.get_major_formatter().set_powerlimits((0, 1))
        ax2.legend(loc='upper right', bbox_to_anchor=(1,1))


        fig1.suptitle(r"Numero di particelle rivelate in funzione dell'energia (E) e per vari angoli ($\theta$)", fontsize=16)

        if save == 'Yes':
            fig1.savefig('energia.png')

        plt.show()



    if args.hisang == True:
        
        #simulazione e raccolta dati
        print(f'Simulazione sciame in funzione dell\'energia E e dell\'angolo rispetto alla verticale θ con {E_min:.1e} MeV<E<{E_max:.1e} MeV e {ang_min}°<θ<{ang_max}°')

        n=int(input('Scegliere il numero di valori di θ da considerare per ognuno dei 4 valori di E considerati. (I valori sono uniformemente spaziati tra i valori massimi e minimi considerati)  ' ))
        
        energie = np.linspace(E_min, E_max, 4)
        angoli = np.linspace(ang_min, ang_max, n)

        s = float(input('Inserire il valore del passo di avanzamento (s) in frazioni di X0 (valore compreso tra 0 e 1)  '))
        while not (s>=0 and s<=1):
            s= float(input('Inserire un valore di s compreso tra 0 e 1  '))

        save= input('Prima di iniziare la simulazione scegliere se salvare o meno il grafico prodotto (Yes or No) ')
        while save != 'Yes' and save !='No':
            save= input('Scegliere se salvare o meno il grafico prodotto digitando Yes or No ')   

        print(f'Inizio simulazione per {n} valori di θ per ogni E con passo {s}')

        #creo il dataframe per contenere i risultati della simulazione
        df_risultati = pd.DataFrame(index=pd.MultiIndex.from_product([energie, angoli], names=['energia', 'angolo'])).reset_index()
        
        #per ogni coppia energia-angolo riempio il dataframe con una colonna con il numero di particelle rivelate
        df_risultati['num particelle rivelate'] = pd.DataFrame(df_risultati.progress_apply(lambda x: sa.simulazione_sciame(x['energia'], s, x['angolo']), axis=1))

        
        print('il numero di particelle rivelate per ogni coppia E-θ è:')

        print(f"{'E (MeV)':<10}{'θ (°)':<6}{'Numero particelle rivelate':<30}")
        for _,row in df_risultati.iterrows():
            print(f"{int(row['energia']):<.2e}  {int(row['angolo']):<6} {int(row['num particelle rivelate']):<30}")
        
    
        fig2 = plt.figure(figsize=plt.figaspect(0.5))
        axs1 = fig2.add_subplot(1, 2, 1, projection='3d')
        axs2 = fig2.add_subplot(1, 2, 2)
        fig2.subplots_adjust(wspace=0.5)

        for i, energia in enumerate(energie):
            en = df_risultati.loc[df_risultati['energia']== energia] #dataframe per i valori relativi a quell'energia
            axs2.hist (en['angolo'], bins=20, weights = en['num particelle rivelate'], range=(-2, 47), color=colori[i], alpha=0.5, label=f'E={energia:.2e}MeV' )
            
            axs1.bar3d(en['angolo'], [energia] * len(en['angolo']), np.zeros(len(en['angolo'])), dx=np.full(len(en['angolo']),3), dy=np.full(len(en['energia']), 200),
                    dz=en['num particelle rivelate'], color=colori[i], alpha=0.6)
        

        axs2.set_xlabel(r'$\theta$ (°)')
        axs2.set_ylabel('Numero particelle rivelate')
        axs2.yaxis.tick_right()
        axs2.yaxis.set_label_position('right')
        axs2.yaxis.set_major_formatter(ScalarFormatter())
        axs2.yaxis.get_major_formatter().set_powerlimits((0, 1))
        axs2.legend(loc='upper right', bbox_to_anchor=(1, 1)) 

        axs1.set_xlabel(r'$\theta$ (°)')
        axs1.set_ylabel('E (MeV)')
        axs1.set_zlabel('Numero\nparticelle rivelate', labelpad=20)
        axs1.set_yticks(energie)
        axs1.yaxis.set_major_formatter(ScalarFormatter()) 
        axs1.yaxis.get_major_formatter().set_powerlimits((0, 1))
        axs1.zaxis.set_major_formatter(ScalarFormatter()) 
        axs1.zaxis.get_major_formatter().set_powerlimits((0, 1))

        fig2.suptitle(r"Numero di particelle rivelate in funzione dell'angolo ($\theta$) e per vari valori di energia (E) ", fontsize=16)

        if save == 'Yes':
            fig2.savefig('angolo.png')

        plt.show


    if args.color == True:

                
        #simulazione e raccolta dati
        print(f'Simulazione sciame in funzione dell\'energia E e dell\'angolo rispetto alla verticale θ con {E_min:.1e} MeV<E<{E_max:.1e} MeV e {ang_min}°<θ<{ang_max}°')

        n=int(input('Scegliere il numero di valori di θ e di E da considerare. (I valori sono uniformemente spaziati tra i valori massimi e minimi considerati)  ' ))
        
        energie = np.linspace(E_min, E_max, n)
        angoli = np.linspace(ang_min, ang_max, n)

        s = float(input('Inserire il valore del passo di avanzamento (s) in frazioni di X0 (valore compreso tra 0 e 1)  '))
        while not (s>=0 and s<=1):
            s= float(input('Inserire un valore di s compreso tra 0 e 1  '))
        
        save= input('Prima di iniziare la simulazione scegliere se salvare o meno il grafico prodotto (Yes or No) ')
        while save != 'Yes' and save !='No':
            save= input('Scegliere se salvare o meno il grafico prodotto digitando Yes or No ')   

        print(f'Inizio simulazione per {n} valori di E e di θ con passo {s}')

        #creo il dataframe per contenere i risultati della simulazione
        df_risultati = pd.DataFrame(index=pd.MultiIndex.from_product([energie, angoli], names=['energia', 'angolo'])).reset_index()
        
        #per ogni coppia energia-angolo riempio il dataframe con una colonna con il numero di particelle rivelate
        df_risultati['num particelle rivelate'] = pd.DataFrame(df_risultati.progress_apply(lambda x: sa.simulazione_sciame(x['energia'], s, x['angolo']), axis=1))

        
        print('il numero di particelle rivelate per ogni coppia E-θ è:')

        print(f"{'E (MeV)':<10}{'θ (°)':<6}{'Numero particelle rivelate':<30}")
        for _,row in df_risultati.iterrows():
            print(f"{int(row['energia']):<.2e}  {int(row['angolo']):<6} {int(row['num particelle rivelate']):<30}")
        
    
        
        #grafico scatter e contourf
        fig, axs = plt.subplots(1, 2, figsize=(14, 6), constrained_layout=True)
        sc=axs[0].scatter(df_risultati['energia'], df_risultati['angolo'], marker='o', c=df_risultati['num particelle rivelate'], cmap='plasma')
        axs[0].set_xlabel('E (MeV)')
        axs[0].set_ylabel(r'$\theta$ (°)')
        axs[0].xaxis.set_major_formatter(ScalarFormatter())
        axs[0].xaxis.get_major_formatter().set_powerlimits((0, 1))

        E, A = np.meshgrid(np.unique(df_risultati['energia']), np.unique(df_risultati['angolo']))
        # Interpolazione per riempire la griglia
        Z = griddata((df_risultati['energia'], df_risultati['angolo']),df_risultati['num particelle rivelate'],(E, A),method='cubic')

        axs[1].contourf(E, A, Z, levels=20, cmap='plasma')
        axs[1].set_xlabel("E (MeV)")
        axs[1].set_ylabel(r"$\theta$ (°)")
        axs[1].xaxis.set_major_formatter(ScalarFormatter())
        axs[1].xaxis.get_major_formatter().set_powerlimits((0, 1))

        cbar = fig.colorbar(sc, ax=axs, orientation='vertical', shrink=0.9)
        cbar.set_label('Numero di particelle rivelate')
        cbar.formatter.set_powerlimits((0, 1))
        cbar.ax.tick_params(axis='y', labelsize=10)
        cbar.ax.yaxis.set_major_formatter(ScalarFormatter())

        plt.suptitle(r"Numero di particelle rivelate in funzione dell'energia (E) e dell'angolo ($\theta$)", fontsize=16)

        if save == 'Yes':
            fig.savefig('angolo_en.png')

        plt.show()
        


if __name__ == "__main__":

    analisi_sciame()


