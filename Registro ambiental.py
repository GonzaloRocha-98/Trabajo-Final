#!/usr/bin/python3
# -*- coding: utf-8 -*-
import Adafruit_DHT
import time
import PySimpleGUI as sg
import json

"""
Conección One-Wire:
Resistencia 10K entre VCC y DATA
1er pin del sensor al VCC 3,3V
2do pin del sensor DATA al BCM 17( pin numero 11 de la raspberry)
4to pin del sensor al GND de la raspberry
"""

class Temperatura:
    """Clase del sensor de temperatura y humedad con sus configuraciones"""
    def __init__(self, pin=17, sensor=Adafruit_DHT.DHT11):
        # Usamos el DHT11 que es compatible con el DHT12 
        self._sensor = sensor 
        self._data_pin = pin

    def datos_sensor(self):
      """ Devuelve un diccionario con la temperatura y humedad """
      humedad, temperatura = Adafruit_DHT.read_retry(self._sensor, self._data_pin)
      return {'temp': temperatura, 'humedad': humedad, "fecha": time.strftime("%a %d %b, %y")}

"""--------------------------------------------------------------------------Progrma Principal--------------------------------------------------------------------------"""


def guardar_datos(ofi, datos):
    try:
        with open("datos-oficinas.json") as arch:
            dato = json.load(arch)
        if ofi in dato:
            dato[ofi].append(datos)
        else:
            dato.update({ofi:[datos]})
        with open("datos-oficinas.json", "w") as arch:
            json.dump(dato, arch)
    except FileNotFoundError:
        dic = {ofi:datos}
        with open("datos-oficinas.json", "w") as arch:
            json.dump(dic, arch)
    

if __name__ == "__main__":

    temp = Temperatura()
    ofi = sg.PopupGetText("Ingrese la oficina donde se encuentra el sensor")
    while True:
        datos = temp.datos_sensor()
        guardar_datos(ofi, datos)
        # Imprime en la consola las variables temperatura y humedad con un decimal
        print('Temperatura = {0:0.1f}°C  Humedad = {1:0.1f}%'.format(datos['temp'], datos['humedad']))
        time.sleep(60)
