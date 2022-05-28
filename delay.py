# Eurêka
import websocket
import RPi.GPIO as GPIO
import time
from utils.protocol import ProtocolDecodeur, ProtocolGenerator

class Eureka:

    def __init__(self, name : str) -> None:
        self.name = name
        
    def start(self,ws):
        self.initName(ws)

    def initName(self, ws):
        data = ProtocolGenerator("name", self.name)
        ws.send(data.create())

erk = Eureka("eureka")

def decodeData(data : str) -> list[str]:
        dataTr = ProtocolDecodeur(data)
        return dataTr.getKeyValue()

def on_message(ws, message):
    [key, val] = decodeData(message)
    delay = int(val)
    time.sleep(delay)
    print("Send after delay")
    data = ProtocolGenerator(erk.name, key[1:])
    print("Delai de ", val, " second pour le state : ", key[1:])
    ws.send(data.create())

def on_error(ws, error):
    print(error)

def on_close(ws, close_status_code, close_msg):
    print("### closed ###")

def on_open(ws):
    erk.start(ws)

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8000", on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)

    ws.run_forever() 

    
    
