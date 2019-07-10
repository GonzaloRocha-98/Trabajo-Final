import time
import RPi.GPIO as GPIO
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
import Adafruit_DHT

class Temperatura:

    def __init__(self, pin=17, sensor=Adafruit_DHT.DHT11):
        self._sensor = sensor 
        self._data_pin = pin

    def datos_sensor(self):
      """ Devuelve un diccionario con la temperatura y humedad """
      humedad, temperatura = Adafruit_DHT.read_retry(self._sensor, self._data_pin)
      return {'temperatura': temperatura, 'humedad': humedad}

class Matriz:
    def __init__(self, numero_matrices=2, orientacion=0, rotacion=0, ancho=16, alto=8):
        self.font = [CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT]
        self.serial = spi(port=0, device=0, gpio=noop())
        self.device = max7219(self.serial, width=ancho, height=alto, cascaded=numero_matrices, rotate=rotacion)
    
    def mostrar_mensaje(self, msg, delay=0.1, font=1):
        show_message(self.device, msg, fill="white", font=proportional(self.font[font]),scroll_delay=delay)

class Sonido:
    
    def __init__(self, canal=22):
        self._canal = canal
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self._canal, GPIO.IN)
        GPIO.setwarnings(False)
        GPIO.add_event_detect(self._canal, GPIO.RISING)
        
    def evento_detectado(self, funcion):
        if GPIO.event_detected(self._canal):
            funcion()

# Conexión de los sensores en sus respectivos pines
# Matriz --> vcc: 2, gnd: 6, din: 19, cs: 24, clk: 23
# Sonido --> a0: 7, gnd: 9, vc: 3, d0: 15
# Temperatura --> vcc: 1, sda: 11, gnd: 14

# Activamos los sensores que vamos a usar
# matriz = Matriz(numero_matrices=2, ancho=16)
matriz = Matriz()
sonido = Sonido()
temperatura = Temperatura()

def acciones():
    print ("Sonido Detectado!")
    temp_data = temperatura.datos_sensor()
    temp_formateada = 'Temperatura = {0:0.1f}°C  Humedad = {1:0.1f}%'.format(temp_data['temperatura'], temp_data['humedad'])
    matriz.mostrar_mensaje(temp_formateada, delay=0.08, font=2)
            
if __name__ == "__main__":
    while True:
        time.sleep(0.1)
        sonido.evento_detectado(acciones)
