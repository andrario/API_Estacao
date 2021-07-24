import schedule
import time
import os
import datetime
from Sensores import Sensores

sensores = Sensores()
a = True

def leitura():
    umid = None
    temp1 = None
    temp2 = None
    pressure = None
    precipitacao = None
    try:
        while umid == None and temp1 == None:
            umid,temp1 = sensores.read_dht11()
        while pressure == None and temp2 == None:
            temp2,pressure = sensores.read_bme280()
        precipitacao = sensores.read_pluviometro()
    except:
        pressure = 'ERRO'
        umid = 'ERRO'
        temp1 = 'ERRO'
        temp2 = 'ERRO'
    data = datetime.datetime.now()
    nome_arquivo = data.strftime('%Y_%m_%d')
    if not os.path.isfile(f'{nome_arquivo}.txt'):
        with open(f'{nome_arquivo}.txt', 'w') as file:
            file.writelines(f"Data;Pressao;Umidade;Temperatura1;Temperatura2;Precipitaçao\n")
    with open(f'{nome_arquivo}.txt', 'a+') as file:
        file.writelines(f"{data};{pressure};{umid};{temp1};{temp2};{precipitacao}\n")
    print('Leitura realizada')

schedule.every(10).minutes.do(leitura)
leitura()
print('Scheduler iniciado')
while True:
    schedule.run_pending()
    # if a:
    #     print('tick')
    #     a = False
    # else:
    #     print('tock')
    #     a = True
    time.sleep(15)