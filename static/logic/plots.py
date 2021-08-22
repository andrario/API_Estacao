import pandas as pd
# from matplotlib import pyplot as plt
# import matplotlib.dates as md
import datetime
import glob
from io import BytesIO
import base64


class Plots():

    def test_plot():
        plt.plot([1,2,3,4,5,6,7,8,9])
        plt.rcParams["figure.figsize"] = (10,5)
        buf = BytesIO()
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        buffer = b''.join(buf)
        buffer = base64.b64encode(buffer)
        buffer = buffer.decode('utf-8')
        return buffer

    def get_medias(dias=8):
        # ano = '*' if ano=='' or ano==None else ano
        # mes = '*' if mes=='' or mes==None else f'{int(mes):02d}'
        # dia = '*' if dia=='' or dia==None else f'{int(dia):02d}'
        # data = f'{dia}/{mes}/{ano}'
        # arquivos = glob.glob(f'./Data/{ano}_{mes}_{dia}.txt')
        arquivos = glob.glob(f'./Data/*.txt')
        arquivos.sort()
        arquivos = arquivos[-dias:]
        
        df_week = pd.DataFrame(columns=['Data','Media_Pressao','Media_Temperatura','Media_Umidade'])

        for arquivo in arquivos:
            df = pd.read_csv(arquivo, sep=';')
            dados = {
                'Data':df.loc[1,'Data'],
                'Media_Pressao':df['Pressao'].mean(),
                'Media_Umidade':df['Umidade'].mean(),
                'Media_Temperatura':df['Temperatura2'].mean()
                }
            df_week = df_week.append([dados], ignore_index=True)
        df_week['Data'] = df_week['Data'].astype('datetime64[ns]')
        data = df_week.loc[1,'Data'].strftime("%d/%m/%Y")
        hora = df_week['Data'].dt.strftime('%d/%m')
        return hora.to_list(), df_week['Media_Pressao'].to_list(), df_week['Media_Umidade'].to_list(), df_week['Media_Temperatura'].to_list(), data

    def get_evolucaop(ano='*', mes='*', dia='*'):
        buf = BytesIO()
        mes = f'{int(mes):02d}'
        dia = f'{int(dia):02d}'
        arquivo = glob.glob(f'./Data/{ano}_{mes}_{dia}.txt')[-1]
        df = pd.read_csv(arquivo, sep=';')
        df['Data'] = df['Data'].astype('datetime64[ns]')
        data = df['Data'][1].strftime('%d/%m/%Y')
        df['Hora'] = df['Data'].dt.strftime('%H:%M:%S')

        dt_fmt = md.DateFormatter('%H:%M:%S')
        fig, ax = plt.subplots(3,1,figsize=(10,5.5), gridspec_kw={'height_ratios': [1,1,1]})
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
        plt.savefig(buf, format='png')
        plt.close()
        buf.seek(0)
        buffer = b''.join(buf)
        buffer = base64.b64encode(buffer)
        buffer = buffer.decode('utf-8')
        return buffer

    def get_evolucao(ano='', mes='', dia=''):
        ano = '*' if ano=='' or ano==None else ano
        mes = '*' if mes=='' or mes==None else f'{int(mes):02d}'
        dia = '*' if dia=='' or dia==None else f'{int(dia):02d}'
        data = f'{dia}/{mes}/{ano}'
        arquivo = glob.glob(f'./Data/{ano}_{mes}_{dia}.txt')
        arquivo.sort()
        arquivo = arquivo[-1]
        df = pd.read_csv(arquivo, sep=';')
        df['Data'] = df['Data'].astype('datetime64[ns]')
        data = df.loc[5,'Data'].strftime("%d/%m/%Y")
        hora = [x.strftime("%H:%M") for x in df['Data'].to_list()]
        return hora, df['Pressao'].to_list(), df['Umidade'].to_list(), df['Temperatura2'].to_list(), data

    def get_evolucao_semanal():
        arquivos = glob.glob(f'./Data/*.txt')
        arquivos.sort()
        arquivos = arquivos[-8:]
        
        df_week = pd.DataFrame(columns=['Data','Pressao','Umidade','Temperatura1','Temperatura2','Precipitaçao'])

        for arquivo in arquivos:
            df = pd.read_csv(arquivo, sep=';')
            df_week = df_week.append(df, ignore_index=True)
        df_week['Data'] = df_week['Data'].astype('datetime64[ns]')
        hora = df_week['Data'].dt.strftime('%d/%m')
        print(hora)
        return hora.to_list(), df_week['Pressao'].to_list(), df_week['Umidade'].to_list(), df_week['Temperatura2'].to_list()

    def get_evolucao_mensal(dias=8): # Quantidade de dias +1
        arquivos = glob.glob(f'./Data/*.txt')
        arquivos.sort()
        arquivos = arquivos[-dias:]
        
        df_week = pd.DataFrame(columns=['Data','Pressao','Umidade','Temperatura1','Temperatura2','Precipitaçao'])

        for arquivo in arquivos:
            df = pd.read_csv(arquivo, sep=';')
            df_week = df_week.append(df, ignore_index=True)
        df_week['Data'] = df_week['Data'].astype('datetime64[ns]')
        hora = df_week['Data'].dt.strftime('%d/%m')
        print(hora)
        return hora.to_list(), df_week['Pressao'].to_list(), df_week['Umidade'].to_list(), df_week['Temperatura2'].to_list()