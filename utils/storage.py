import subprocess
from utils.connectionManager import ConnectionManager
from utils.fileManager import FileManager
from utils.protocol import DbLineDecodeur
import json
from utils.speak import Speak

class PlantsTypeManager:
    plantsFilePath = "./db/plants.json"
    plantsList = []

    def __init__(self, storage, plantIndex : int):
        self.storage = storage
        self.plantIndex = plantIndex

    def decodeFilePlant(self):
        f = open(self.plantsFilePath, "r")
        data = json.load(f)
        self.plantsList = data

class Storage:
    store : dict[str, str] = {}
    notStored = ["eureka", "button", "process"]
    fileManager = FileManager('./db/db.txt')
    plantsFilePath = "./db/plants.json"
    plantCarac = {}

    def __init__(self, connectionManager : ConnectionManager):
        self.connectionManager = connectionManager
        self.plantsList = self.decodeFilePlant()

    def initStorage(self):
        self.changePlantIndexOnStore(0)
        self.createFile()
        self.createStore()
        self.initValueStore()
        self.setupPlantCarac()

    def initValueStore(self):
        lines = self.fileManager.getLines()
        for line in lines:
            l = DbLineDecodeur(line)
            [key, val] = l.getKeyValue()
            self.store[key] = val
        print(self.store)
        
    def createStore(self):
        cl = self.connectionManager.clients
        for key, value in cl.items():
            if value in self.notStored:
                pass
            else:
                self.store[value] = ""
        print(self.store)

    def createFile(self):
        self.fileManager.createFile()

    def saveOnFile(self, key:str, data:str):
        self.fileManager.addValue(key, data)

    def saveOnStore(self, key:str, data:str):
        self.store[key] = data

    def changePlantIndexOnStore(self, index : int):
        self.store["plantIndex"] = str(index)

    def decodeFilePlant(self):
        f = open(self.plantsFilePath, "r")
        data = json.load(f)
        return data
    
    def setupPlantCarac(self):
        self.plantCarac = self.plantsList[int(self.store["plantIndex"])]
        self.savePlantOnFile()

    def savePlantOnFile(self):
        self.saveOnFile("plantIndex", self.store["plantIndex"])

    def changePlantRight(self):
        currentIndex = int(self.store["plantIndex"])
        newIndex = currentIndex + 1
        if newIndex < len(self.plantsList):
            self.changePlantIndexOnStore(newIndex)
            self.setupPlantCarac()
        Speak.speak(self.plantCarac["name"])


    def changePlantLeft(self):
        currentIndex = int(self.store["plantIndex"])
        newIndex = currentIndex - 1
        if newIndex >= 0:
            self.changePlantIndexOnStore(newIndex)
            self.setupPlantCarac()
        Speak.speak(self.plantCarac["name"])