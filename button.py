from websocket import create_connection
import RPi.GPIO as GPIO
import time
from utils.protocol import ProtocolGenerator
from utils.types import BtnType

class Button:
    SENSOR_PIN_1 = 12
    SENSOR_PIN_2 = 21
    SENSOR_PIN_3 = 19
    

    def __init__(self, name : str) -> None:
        self.name = name
        self.ws = create_connection("ws://localhost:8000")
        time.sleep(3)
        self.setupHardware()
        self.initName()
    
    def start(self):
        while True:
            print(self.name , " is working !")
            time.sleep(60)

    def initName(self):
        data = ProtocolGenerator("name", self.name)
        self.ws.send(data.create())

    def setupHardware(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.SENSOR_PIN_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.SENSOR_PIN_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.SENSOR_PIN_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.SENSOR_PIN_1, GPIO.RISING, callback=self.sensor_callback_1, bouncetime=300)
        GPIO.add_event_detect(self.SENSOR_PIN_2, GPIO.RISING, callback=self.sensor_callback_2, bouncetime=300)
        GPIO.add_event_detect(self.SENSOR_PIN_3, GPIO.RISING, callback=self.sensor_callback_3, bouncetime=300)

    def sensor_callback_1(self,channel):
        print("Button LEFT")
        type = BtnType.LEFT
        data = ProtocolGenerator(self.name, type.value)
        self.ws.send(data.create())
        
    def sensor_callback_2(self,channel):
        print("Button OK")
        type = BtnType.OK
        data = ProtocolGenerator(self.name, type.value)
        self.ws.send(data.create())

    def sensor_callback_3(self,channel):
        print("Button RIGHT")
        type = BtnType.RIGHT
        data = ProtocolGenerator(self.name, type.value)
        self.ws.send(data.create())
        


btn = Button("button")
btn.start()


