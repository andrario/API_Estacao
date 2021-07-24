'''
Configuração deste programa
Conectar BMP280 nos pinos BOARD 3 e 5
Conectar DHT11 no pino BOARD 7
Conectar Pluviometro no pino BOARD 11
'''
'''
Bibliotecas 
'''
import bme280
from Adafruit_ADS1x15 import ADS1115
import Adafruit_DHT as DHT
import RPi.GPIO as GPIO
import digitalio
import board
import struct
import time

mmChuva = 0.0

class Sensores(object):

    GPIO_PLUVIOMETRO = 17
    GPIO_DHT = 4

    ADS = ADS1115()
    ADS_LSB = {
        1:0.0001875,
        2:0.0001250,
        3:0.0000625,
        4:0.00003125,
        5:0.000015625,
        6:0.0000078125,
    }
    raio = 0.07 # 7cm
    GPIO.setup(GPIO_PLUVIOMETRO, GPIO.IN)
    

    def read_bme280(self):
        temperature,pressure = bme280.readBME280All()
        return temperature,pressure
    
    def read_ads1115(self, channel, gain=1):
        read = self.ADS.read_adc(channel)
        if read < 0:
            return 0
        else:
            read = read*self.ADS_LSB[gain]
            return read
    
    def read_dht11(self):
        humidity,temperature = DHT.read_retry(DHT.DHT11, self.GPIO_DHT, 5)
        return humidity,temperature
    
    def callback_pluviometro(self, channel=None):
        global mmChuva
        mmChuva += 0.2
        print(f'Chuva acumulada: {mmChuva}')
    GPIO.add_event_detect(GPIO_PLUVIOMETRO, GPIO.RISING, callback=callback_pluviometro, bouncetime=300)
    def read_pluviometro(self):
        global mmChuva
        return mmChuva
    def zera_pluviometro():
        global mmChuva
        mmChuva = 0.0
    
    def read_all_pretty(self):
        umid,temp1 = self.read_dht11()
        temp2,pressure = self.read_bme280()
        temp_a = (temp1+temp2)/2
        global mmChuva
        print(f'Umidade: {umid} %')
        print(f'Pressão atm: {pressure:3g} hPa')
        print(f'Temperatura Ambiente: {temp_a:3g} °C')
        print(f'Precipitação: {mmChuva:3g} mm')

        return True
    
    # def read_speed():
    #     timeout = 10
    #     intervalo = 0
    #     start = False
    #     while intervalo < timeout * 1000000000:
    #         parado = 0
    #         if GPIO.input(7) and not start:
    #             start = time.time_ns()
    #             while GPIO.input(7) and parado < 10:
    #                 parado += 0.5
    #                 time.sleep(0.5)
    #         elif GPIO.input(7) and start:
    #             end = time.time_ns()
    #         else:
    #             end
    #         intervalo = 0


def main():
    print(Sensores().read_all_pretty())
    
if __name__=="__main__":
   main()