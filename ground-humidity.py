import RPi.GPIO as GPIO
import time
from websocket import create_connection
from utils.protocol import ProtocolGenerator

class GroudHumiditySensor:
        SENSOR_PIN = 20

        def __init__(self, name : str, data : str):
                self.name = name
                self.data = data
                self.ws = create_connection("ws://localhost:8000")
                time.sleep(3)
                self.setupHardware()
                self.initName()
        
        def initName(self):
                data = ProtocolGenerator("name", self.name)
                self.ws.send(data.create())
        
        def start(self):
                while True:
                        print(self.name , " is working !")
                        time.sleep(60)
        
        def setupHardware(self):
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.SENSOR_PIN, GPIO.IN)
                GPIO.add_event_detect(self.SENSOR_PIN, GPIO.BOTH, bouncetime=300)  # let us know when the pin goes HIGH or LOW
                GPIO.add_event_callback(self.SENSOR_PIN, callback=self.sensor_callback)  # assign function to GPIO PIN, Run function on change

        def sensor_callback(self,channel):
                data = ProtocolGenerator(self.name, self.data)
                rdyToSend = data.create()
                if GPIO.input(channel):
                        print("Water Detected!")
                        self.ws.send(rdyToSend)
                else:
                        print("Water Detected!")
                        self.ws.send(rdyToSend)


GrndHum = GroudHumiditySensor("humidityground", "1")
GrndHum.start()