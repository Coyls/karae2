import RPi.GPIO as GPIO
import time
from websocket import create_connection
from utils.protocol import ProtocolGenerator

class ProximitySensor:
    SENSOR_PIN = 23

    def __init__(self, name : str, data : str) -> None:
        self.name = name
        self.data = data
        self.ws = create_connection("ws://localhost:8000")
        time.sleep(3)
        self.setupHardware()
        self.initName()
    
    def start(self):
        try:
            while True:
                print(self.name , " is working !")
                time.sleep(60)
        except KeyboardInterrupt:
                print(self.name , " shutdown !")
                GPIO.cleanup()

    def initName(self):
        data = ProtocolGenerator("name", self.name)
        self.ws.send(data.create())

    def setupHardware(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SENSOR_PIN, GPIO.IN)
        GPIO.add_event_detect(self.SENSOR_PIN , GPIO.RISING, callback=self.sensor_callback)

    def sensor_callback(self,channel):
        data = ProtocolGenerator(self.name, self.data)
        self.ws.send(data.create())
        print('There was a movement!')

prx = ProximitySensor("proximity", "1")
prx.start()