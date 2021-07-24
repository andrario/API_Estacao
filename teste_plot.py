import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.dates as md
import datetime
import sys

def gera_figura():
    try:
        nome = sys.argv[1].replace('.txt','')
        df = pd.read_csv(sys.argv[1], sep=';')
        df['Data'] = df['Data'].astype('datetime64[ns]')
        data = df['Data'][1].strftime('%d/%m/%Y')
        df['Hora'] = df['Data'].dt.strftime('%H:%M:%S')
        df.head()

        dt_fmt = md.DateFormatter('%H:%M:%S')
        fig, ax = plt.subplots(3,1,figsize=(16,9), gridspec_kw={'height_ratios': [1,1,1]})
        ax[0].set(ylabel='Pressão (hPa)',title=f'Clima {data}')
        ax[0].set_xticklabels([])
        ax[0].xaxis.grid()
        ax[1].set(ylabel='Umidade (%)')
        ax[1].set_xticklabels([])
        ax[1].xaxis.grid()
        ax[2].set(xlabel='Hora',ylabel='Temperatura (ºC)')
        ax[2].xaxis.grid()
        press, = ax[0].plot(df['Data'], df['Pressao'])
        umid, = ax[1].plot(df['Data'], df['Umidade'])
        temp, = ax[2].plot(df['Data'], df['Temperatura2'])
        ax[2].xaxis.set_major_formatter(dt_fmt)
        for tick in ax[2].get_xticklabels():
            tick.set_rotation(45)
        plt.savefig(f'clima_{nome}.png')
        print(f'clima_{nome}.png')
    except:
        print('Provavelmente voce errou o nome do arquivo, seu nóia')

if __name__ == "__main__":
    gera_figura()