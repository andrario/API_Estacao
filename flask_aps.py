from flask import Flask
from flask_apscheduler import APScheduler
from flask import jsonify
from flask import request
from flask import render_template
from static.logic.Sensores import Sensores
from static.logic.plots import Plots
import time
import datetime
import os
from pymongo import MongoClient


app = Flask(__name__)
scheduler = APScheduler()
sensores = Sensores()


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
    nome_arquivo = f'./Data/{nome_arquivo}.txt'
    if not os.path.isfile(nome_arquivo):
        with open(nome_arquivo, 'w') as file:
            file.writelines(f"Data;Pressao;Umidade;Temperatura1;Temperatura2;Precipitaçao\n")
    with open(nome_arquivo, 'a+') as file:
        file.writelines(f"{data};{pressure};{umid};{temp1};{temp2};{precipitacao}\n")
    print('Leitura realizada')

def leitura_db():
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
        pressure = 0
        umid = 0
        temp1 = 0
        temp2 = 0
    data = datetime.datetime.now()
    nome_collection = data.strftime('%Y_%m_%d')
    with MongoClient('localhost', 27017) as cliente:
        db = cliente['Estacao']
        collection = db[nome_collection]
        entrada = {
            "Data":data,
            "Pressao":pressure,
            "Umidade":umid,
            "Temperatura1":temp1,
            "Temperatura2":temp2,
            "Precipitaçao":precipitacao
        }
        collection.insert_one(entrada)
    print('Leitura realizada db')

scheduler.init_app(app)
scheduler.add_job(func=leitura, trigger='interval', minutes=15, id='leitura_periodica')
scheduler.add_job(func=leitura_db, trigger='interval', minutes=15, id='leitura_periodica_db')
leitura()
leitura_db()
scheduler.start()

@app.route('/')
def root():
    return render_template('home.html')

@app.route('/api')
def api():
    return 'API Estação Meteorológica v 0.1', 200

@app.route('/now')
def now():
    try:
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
        leitura = {'Pressao':pressure, 'Temperatura':temp2, 'Umidade':umid, 'Precipitacao':precipitacao}
        return leitura, 200
    except:
        return 'Erro', 503

@app.route('/media_semanal')
def media_semanal():
    try:
        hora, pressao, umidade, temperatura, data = Plots.get_medias(dias=8)
        return render_template('plot_barra.html', plot_name=f'Médias dos ultimos 7 dias', varx=hora, pressao=pressao, umidade=umidade, temperatura=temperatura), 200
    except:
        return 'Algo deu errado', 503

@app.route('/media_mensal')
def media_mensal():
    try:
        hora, pressao, umidade, temperatura, data = Plots.get_medias(dias=31)
        return render_template('plot_barra.html', plot_name=f'Médias dos ultimos 31 dias', varx=hora, pressao=pressao, umidade=umidade, temperatura=temperatura), 200
    except:
        return 'Algo deu errado', 503

@app.route('/evolucao_semanal')
def evolucao_semanal():
    try:
        hora, pressao, umidade, temperatura = Plots.get_evolucao_semanal()
        return render_template('plot_linha.html', plot_name=f'Evolução dos ultimos 7 dias', varx=hora, pressao=pressao, umidade=umidade, temperatura=temperatura), 200
    except:
        return 'Algo deu errados', 503

@app.route('/evolucao_mensal')
def evolucao_mensal():
    try:
        hora, pressao, umidade, temperatura = Plots.get_evolucao_mensal(dias=31)
        return render_template('plot_linha.html', plot_name=f'Evolução dos ultimos 30 dias', varx=hora, pressao=pressao, umidade=umidade, temperatura=temperatura), 200
    except:
        return 'Algo deu errados', 503

@app.route('/evolucaop')
def evolucaop():
    try:
        data = datetime.datetime.now().strftime('%d/%m/%Y')
        return render_template('plot.html', plot_name=f'Evolução Diária: {data}', plot_url=Plots.get_evolucao()), 200
    except:
        return 'Algo deu errado', 503

@app.route('/evolucao')
def evolucao():
    try:
        if request.args.get('data'):
            data = request.args.get('data')
            ano = data.split('-')[0]
            mes = data.split('-')[1]
            dia = data.split('-')[2]
        else:
            ano = request.args.get('ano')
            mes = request.args.get('mes')
            dia = request.args.get('dia')
        hora, pressao, umidade, temperatura, data = Plots.get_evolucao(ano, mes, dia)
        return render_template('plot_linha.html', plot_name=data, varx=hora, pressao=pressao, umidade=umidade, temperatura=temperatura), 200
    except:
        return 'Algo deu errado', 503

@app.route('/testedb')
def testedb():
    try:
        hora, pressao, umidade, temperatura = Plots.get_db()
        leituras = {
            'hora':hora,
            'pressao':pressao,
            'umidade':umidade,
            'temperatura':temperatura,
        }
        return leituras, 200
    except:
        return 'Algo deu errado', 503

@app.route('/args')
def args():
    try:
        if request.args.get('data'):
            data = request.args.get('data')
            return f'ok - {data}'
        else:
            data = request.args.get('data')
            return f'else - {data}'
    except:
        return 'Algo deu errado', 503

app.run(host='0.0.0.0', port=80, debug=True)
